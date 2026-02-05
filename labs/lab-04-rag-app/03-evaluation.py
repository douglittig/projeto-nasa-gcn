# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 4.3: RAG Evaluation with MLflow
# MAGIC
# MAGIC Este notebook avalia a qualidade do sistema RAG usando MLflow e métricas específicas.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Definir métricas de avaliação para RAG
# MAGIC 2. Avaliar qualidade do retrieval
# MAGIC 3. Avaliar qualidade da geração
# MAGIC 4. Logar resultados com MLflow
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 4: Evaluation and Monitoring (18%)
# MAGIC - Apply model evaluation with RAG-specific metrics
# MAGIC - Log evaluation results with MLflow
# MAGIC - Compare model configurations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install databricks-vectorsearch langchain langchain-community mlflow evaluate rouge-score -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.chat_models import ChatDatabricks
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import mlflow
from mlflow.metrics.genai import relevance, faithfulness
import pandas as pd
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Carregar config
config_df = spark.table("rag_config").collect()
config = {row.key: row.value for row in config_df}

VS_ENDPOINT = config.get("VS_ENDPOINT")
VS_INDEX = config.get("VS_INDEX")

print(f"✅ Configuração carregada")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Configurar RAG Chain

# COMMAND ----------

# DBTITLE 1,Recriar RAG chain para avaliação
# Setup Vector Search
vsc = VectorSearchClient()
dvs = DatabricksVectorSearch(
    endpoint=VS_ENDPOINT,
    index_name=VS_INDEX,
    text_column="chunk_text",
    columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"]
)

retriever = dvs.as_retriever(search_kwargs={"k": 5})

# Setup LLM
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.1,
    max_tokens=1024
)

# Prompt
SYSTEM_PROMPT = """You are an expert astrophysics assistant. Answer questions about astronomical events
using ONLY the provided GCN Circulars context.

Context from GCN Circulars:
{context}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])


def format_docs(docs):
    """Formata documentos para contexto."""
    formatted = []
    for doc in docs:
        event_id = doc.metadata.get("event_id", "Unknown")
        formatted.append(f"[{event_id}]: {doc.page_content}")
    return "\n\n".join(formatted)


# RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("✅ RAG Chain configurada para avaliação")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar Dataset de Avaliação

# COMMAND ----------

# DBTITLE 1,Dataset de avaliação
# Carregar perguntas de teste do notebook anterior
test_questions_df = spark.table("rag_test_questions")
test_questions = [row.asDict() for row in test_questions_df.collect()]

print(f"📊 {len(test_questions)} perguntas de teste carregadas")

# Adicionar ground truth (respostas esperadas)
# Em produção, isso seria criado por especialistas
EVAL_DATASET = [
    {
        "question": "What observations were made for gamma-ray bursts detected by Fermi GBM?",
        "ground_truth": "Fermi GBM detected multiple gamma-ray bursts with various trigger times, durations (T90), and sky positions reported in GCN Circulars.",
        "expected_keywords": ["Fermi", "GBM", "trigger", "T90", "position"]
    },
    {
        "question": "What high-energy neutrino events were detected by IceCube?",
        "ground_truth": "IceCube detected high-energy neutrino events with estimated energies and sky positions, triggering multi-messenger follow-up observations.",
        "expected_keywords": ["IceCube", "neutrino", "energy", "position", "alert"]
    },
    {
        "question": "What optical telescopes conducted follow-up observations?",
        "ground_truth": "Various optical telescopes including NOT, VLT, Gemini, and others conducted follow-up observations reporting magnitudes and positions of transient sources.",
        "expected_keywords": ["optical", "telescope", "magnitude", "observation"]
    },
    {
        "question": "What X-ray afterglows were detected by Swift XRT?",
        "ground_truth": "Swift XRT detected X-ray afterglows of gamma-ray bursts, providing refined positions and flux measurements.",
        "expected_keywords": ["Swift", "XRT", "X-ray", "afterglow", "position"]
    },
    {
        "question": "What is the typical duration of short gamma-ray bursts?",
        "ground_truth": "Short gamma-ray bursts typically have T90 durations less than 2 seconds, while long GRBs have durations greater than 2 seconds.",
        "expected_keywords": ["short", "duration", "T90", "seconds"]
    }
]

# Converter para DataFrame
eval_df = pd.DataFrame(EVAL_DATASET)
print(f"\n📋 Dataset de avaliação:")
print(eval_df[["question", "expected_keywords"]].to_string())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Gerar Respostas do RAG

# COMMAND ----------

# DBTITLE 1,Gerar respostas para avaliação
def generate_rag_responses(eval_data: list) -> list:
    """
    Gera respostas do RAG para cada pergunta.

    Args:
        eval_data: Lista de dicts com question e ground_truth

    Returns:
        Lista com respostas adicionadas
    """
    results = []

    for i, item in enumerate(eval_data):
        question = item["question"]
        print(f"  [{i+1}/{len(eval_data)}] Processando: {question[:50]}...")

        # Recuperar documentos
        docs = retriever.invoke(question)
        context = format_docs(docs)

        # Gerar resposta
        response = rag_chain.invoke(question)

        results.append({
            **item,
            "response": response,
            "context": context,
            "num_docs": len(docs)
        })

    return results


print("🔄 Gerando respostas do RAG...")
eval_results = generate_rag_responses(EVAL_DATASET)
print(f"✅ {len(eval_results)} respostas geradas")

# COMMAND ----------

# DBTITLE 1,Visualizar respostas
# Mostrar exemplo
print("📝 Exemplo de resposta gerada:")
print("=" * 60)
example = eval_results[0]
print(f"Question: {example['question']}")
print(f"\nGround Truth: {example['ground_truth']}")
print(f"\nRAG Response: {example['response'][:500]}...")
print(f"\nDocs used: {example['num_docs']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Métricas de Retrieval

# COMMAND ----------

# DBTITLE 1,Keyword Precision
def calculate_keyword_precision(response: str, expected_keywords: list) -> float:
    """
    Calcula a precisão de keywords na resposta.

    Args:
        response: Resposta gerada
        expected_keywords: Lista de keywords esperadas

    Returns:
        Proporção de keywords encontradas
    """
    response_lower = response.lower()
    found = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
    return found / len(expected_keywords) if expected_keywords else 0.0


# Calcular para todas as respostas
for result in eval_results:
    result["keyword_precision"] = calculate_keyword_precision(
        result["response"],
        result["expected_keywords"]
    )

# Mostrar resultados
print("📊 Keyword Precision por pergunta:")
print("-" * 60)
for r in eval_results:
    print(f"Q: {r['question'][:40]}...")
    print(f"   Precision: {r['keyword_precision']:.2%}")
    print()

avg_precision = sum(r["keyword_precision"] for r in eval_results) / len(eval_results)
print(f"📈 Média: {avg_precision:.2%}")

# COMMAND ----------

# DBTITLE 1,Context Relevance Score
def calculate_context_relevance(context: str, question: str, llm) -> float:
    """
    Usa LLM para avaliar relevância do contexto.

    Args:
        context: Contexto recuperado
        question: Pergunta original
        llm: Modelo de linguagem

    Returns:
        Score de 0 a 1
    """
    eval_prompt = f"""Rate how relevant the following context is for answering the question.
Return ONLY a number from 0 to 10.

Question: {question}

Context:
{context[:2000]}

Relevance score (0-10):"""

    try:
        response = llm.invoke(eval_prompt)
        score_text = response.content.strip()
        # Extrair número
        score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
        return min(score / 10, 1.0)
    except:
        return 0.5  # Default


# Calcular para uma amostra (limitado por custo)
print("🔄 Calculando relevância do contexto (amostra)...")
for i, result in enumerate(eval_results[:3]):
    result["context_relevance"] = calculate_context_relevance(
        result["context"],
        result["question"],
        llm
    )
    print(f"   [{i+1}] Relevance: {result['context_relevance']:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Métricas de Geração (LLM-as-Judge)

# COMMAND ----------

# DBTITLE 1,Faithfulness Score
def calculate_faithfulness(response: str, context: str, llm) -> float:
    """
    Avalia se a resposta é fiel ao contexto (não alucina).

    Args:
        response: Resposta gerada
        context: Contexto usado
        llm: Modelo de linguagem

    Returns:
        Score de 0 a 1
    """
    eval_prompt = f"""Evaluate if the response is faithful to the context (no hallucinations).
Rate from 0 (completely unfaithful/hallucinated) to 10 (completely faithful to context).

Context:
{context[:2000]}

Response:
{response}

Faithfulness score (0-10):"""

    try:
        response = llm.invoke(eval_prompt)
        score_text = response.content.strip()
        score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
        return min(score / 10, 1.0)
    except:
        return 0.5


# Calcular para amostra
print("🔄 Calculando faithfulness (amostra)...")
for i, result in enumerate(eval_results[:3]):
    result["faithfulness"] = calculate_faithfulness(
        result["response"],
        result["context"],
        llm
    )
    print(f"   [{i+1}] Faithfulness: {result['faithfulness']:.2f}")

# COMMAND ----------

# DBTITLE 1,Answer Relevance
def calculate_answer_relevance(response: str, question: str, llm) -> float:
    """
    Avalia se a resposta é relevante para a pergunta.

    Args:
        response: Resposta gerada
        question: Pergunta original
        llm: Modelo de linguagem

    Returns:
        Score de 0 a 1
    """
    eval_prompt = f"""Evaluate if the response directly and completely answers the question.
Rate from 0 (irrelevant/doesn't answer) to 10 (perfectly relevant and complete).

Question: {question}

Response: {response}

Relevance score (0-10):"""

    try:
        response = llm.invoke(eval_prompt)
        score_text = response.content.strip()
        score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
        return min(score / 10, 1.0)
    except:
        return 0.5


# Calcular para amostra
print("🔄 Calculando answer relevance (amostra)...")
for i, result in enumerate(eval_results[:3]):
    result["answer_relevance"] = calculate_answer_relevance(
        result["response"],
        result["question"],
        llm
    )
    print(f"   [{i+1}] Answer Relevance: {result['answer_relevance']:.2f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Log com MLflow

# COMMAND ----------

# DBTITLE 1,Configurar experimento MLflow
# Configurar experimento
mlflow.set_experiment(f"/Users/{spark.sql('SELECT current_user()').collect()[0][0]}/nasa_gcn_rag_evaluation")

print("✅ MLflow experiment configurado")

# COMMAND ----------

# DBTITLE 1,Logar métricas e resultados
with mlflow.start_run(run_name="rag_evaluation_v1") as run:
    # Parâmetros do RAG
    mlflow.log_params({
        "retriever_k": 5,
        "llm_model": "databricks-meta-llama-3-1-70b-instruct",
        "llm_temperature": 0.1,
        "embedding_model": config.get("EMBEDDING_MODEL"),
        "vs_index": VS_INDEX,
        "eval_dataset_size": len(eval_results)
    })

    # Métricas agregadas
    avg_keyword_precision = sum(r.get("keyword_precision", 0) for r in eval_results) / len(eval_results)
    mlflow.log_metric("avg_keyword_precision", avg_keyword_precision)

    # Métricas de amostra (para os que calculamos)
    faithfulness_scores = [r.get("faithfulness", 0) for r in eval_results if "faithfulness" in r]
    if faithfulness_scores:
        mlflow.log_metric("avg_faithfulness", sum(faithfulness_scores) / len(faithfulness_scores))

    relevance_scores = [r.get("answer_relevance", 0) for r in eval_results if "answer_relevance" in r]
    if relevance_scores:
        mlflow.log_metric("avg_answer_relevance", sum(relevance_scores) / len(relevance_scores))

    context_scores = [r.get("context_relevance", 0) for r in eval_results if "context_relevance" in r]
    if context_scores:
        mlflow.log_metric("avg_context_relevance", sum(context_scores) / len(context_scores))

    # Salvar resultados detalhados como artifact
    results_df = pd.DataFrame([{
        "question": r["question"],
        "ground_truth": r["ground_truth"],
        "response": r["response"][:500],
        "keyword_precision": r.get("keyword_precision", None),
        "faithfulness": r.get("faithfulness", None),
        "answer_relevance": r.get("answer_relevance", None)
    } for r in eval_results])

    results_df.to_csv("/tmp/eval_results.csv", index=False)
    mlflow.log_artifact("/tmp/eval_results.csv")

    # Log do dataset de avaliação
    eval_df.to_csv("/tmp/eval_dataset.csv", index=False)
    mlflow.log_artifact("/tmp/eval_dataset.csv")

    run_id = run.info.run_id
    print(f"✅ Resultados logados no MLflow")
    print(f"   Run ID: {run_id}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Comparação de Configurações

# COMMAND ----------

# DBTITLE 1,Avaliar diferentes valores de K
def evaluate_k_values(k_values: list, sample_questions: list) -> list:
    """
    Compara diferentes valores de K para o retriever.

    Args:
        k_values: Lista de valores de K a testar
        sample_questions: Lista de perguntas para teste

    Returns:
        Lista de resultados por K
    """
    results = []

    for k in k_values:
        print(f"🔄 Testando K={k}...")

        # Criar retriever com K específico
        test_retriever = dvs.as_retriever(search_kwargs={"k": k})

        k_results = []
        for q in sample_questions:
            # Recuperar documentos
            docs = test_retriever.invoke(q["question"])
            context = format_docs(docs)

            # Calcular keyword precision no contexto
            precision = calculate_keyword_precision(context, q["expected_keywords"])
            k_results.append(precision)

        avg_precision = sum(k_results) / len(k_results)
        results.append({
            "k": k,
            "avg_context_precision": avg_precision,
            "num_questions": len(sample_questions)
        })
        print(f"   Avg precision: {avg_precision:.2%}")

    return results


# Testar
k_comparison = evaluate_k_values([3, 5, 7, 10], EVAL_DATASET[:3])

print("\n📊 Comparação de K:")
print("-" * 40)
for r in k_comparison:
    print(f"K={r['k']}: Precision = {r['avg_context_precision']:.2%}")

# COMMAND ----------

# DBTITLE 1,Logar comparação de K
with mlflow.start_run(run_name="k_comparison") as run:
    for r in k_comparison:
        mlflow.log_metric(f"precision_k{r['k']}", r["avg_context_precision"])

    # Encontrar melhor K
    best_k = max(k_comparison, key=lambda x: x["avg_context_precision"])
    mlflow.log_param("best_k", best_k["k"])

    print(f"✅ Melhor K: {best_k['k']} (precision: {best_k['avg_context_precision']:.2%})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Resumo da Avaliação

# COMMAND ----------

# DBTITLE 1,Dashboard de resultados
print("""
╔══════════════════════════════════════════════════════════════╗
║           NASA GCN RAG Evaluation Summary                    ║
╠══════════════════════════════════════════════════════════════╣
""")

print(f"  📊 Dataset size: {len(eval_results)} questions")
print(f"  📈 Avg Keyword Precision: {avg_keyword_precision:.2%}")

if faithfulness_scores:
    print(f"  🎯 Avg Faithfulness: {sum(faithfulness_scores)/len(faithfulness_scores):.2%}")
if relevance_scores:
    print(f"  📝 Avg Answer Relevance: {sum(relevance_scores)/len(relevance_scores):.2%}")
if context_scores:
    print(f"  📚 Avg Context Relevance: {sum(context_scores)/len(context_scores):.2%}")

print(f"\n  🏆 Best K value: {best_k['k']}")

print("""
╠══════════════════════════════════════════════════════════════╣
║  MLflow Experiment: nasa_gcn_rag_evaluation                  ║
╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# DBTITLE 1,Salvar métricas finais
# Salvar métricas em tabela para referência
final_metrics = {
    "eval_date": str(pd.Timestamp.now()),
    "dataset_size": len(eval_results),
    "avg_keyword_precision": avg_keyword_precision,
    "avg_faithfulness": sum(faithfulness_scores)/len(faithfulness_scores) if faithfulness_scores else None,
    "avg_answer_relevance": sum(relevance_scores)/len(relevance_scores) if relevance_scores else None,
    "best_k": best_k["k"],
    "mlflow_run_id": run_id
}

# Salvar como tabela
metrics_df = spark.createDataFrame([final_metrics])
metrics_df.write.mode("append").saveAsTable("rag_evaluation_history")

print("✅ Métricas salvas em 'rag_evaluation_history'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. MLflow Tracing para RAG Debugging
# MAGIC
# MAGIC ### Por que MLflow Tracing?
# MAGIC
# MAGIC **MLflow Tracing** permite visualizar e debuggar cada etapa do pipeline RAG:
# MAGIC - Tempo de execucao de cada componente
# MAGIC - Inputs/outputs de cada etapa
# MAGIC - Identificar gargalos de performance
# MAGIC - Debuggar problemas de retrieval ou geracao
# MAGIC
# MAGIC **Exam Tip:** MLflow Tracing e essencial para monitorar RAG em producao.

# COMMAND ----------

# DBTITLE 1,Habilitar MLflow Tracing
import mlflow

# Habilitar tracing automatico para LangChain
mlflow.langchain.autolog(
    log_input_examples=True,
    log_model_signatures=True,
    log_models=False,  # Nao logar modelo inteiro
    log_traces=True    # Habilitar tracing
)

print("MLflow Tracing habilitado para LangChain")

# COMMAND ----------

# DBTITLE 1,Executar RAG com Tracing
# Executar uma query com tracing ativo
with mlflow.start_run(run_name="rag_with_tracing") as run:
    test_query = "What gamma-ray bursts were detected by Fermi?"

    # A execucao sera automaticamente traced
    response = rag_chain.invoke(test_query)

    print(f"Query: {test_query}")
    print(f"\nResponse: {response[:300]}...")
    print(f"\nTrace disponivel no MLflow UI")
    print(f"Run ID: {run.info.run_id}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualizar Traces
# MAGIC
# MAGIC Para ver os traces:
# MAGIC 1. Abra o MLflow UI (Experiments no menu lateral)
# MAGIC 2. Selecione o experimento `nasa_gcn_rag_evaluation`
# MAGIC 3. Clique no run `rag_with_tracing`
# MAGIC 4. Navegue para a aba **Traces**
# MAGIC
# MAGIC ### O que voce vera no Trace:
# MAGIC
# MAGIC ```
# MAGIC rag_chain (total: 2.5s)
# MAGIC ├── retriever (0.3s)
# MAGIC │   ├── embed_query (0.1s)
# MAGIC │   └── similarity_search (0.2s)
# MAGIC ├── format_docs (0.01s)
# MAGIC ├── prompt (0.01s)
# MAGIC └── llm (2.1s)
# MAGIC     └── ChatDatabricks.invoke (2.1s)
# MAGIC ```
# MAGIC
# MAGIC ### Insights do Tracing:
# MAGIC
# MAGIC | Componente | Tempo Tipico | O que Otimizar |
# MAGIC |------------|--------------|----------------|
# MAGIC | **Retriever** | 200-500ms | Reduzir K, usar filtros |
# MAGIC | **LLM** | 1-3s | Reduzir max_tokens, cache |
# MAGIC | **Format** | <10ms | Geralmente OK |

# COMMAND ----------

# DBTITLE 1,Trace Manual para Debugging
from mlflow.tracking import MlflowClient

# Para debugging mais detalhado, podemos adicionar spans manuais
@mlflow.trace(name="custom_rag_pipeline")
def traced_rag_pipeline(question: str) -> dict:
    """RAG pipeline com tracing detalhado."""

    # Span para retrieval
    with mlflow.start_span(name="document_retrieval") as span:
        docs = retriever.invoke(question)
        span.set_inputs({"question": question, "k": 5})
        span.set_outputs({"num_docs": len(docs)})

    # Span para formatacao
    with mlflow.start_span(name="context_formatting") as span:
        context = format_docs(docs)
        span.set_inputs({"num_docs": len(docs)})
        span.set_outputs({"context_length": len(context)})

    # Span para geracao
    with mlflow.start_span(name="llm_generation") as span:
        response = rag_chain.invoke(question)
        span.set_inputs({"context_length": len(context)})
        span.set_outputs({"response_length": len(response)})

    return {
        "question": question,
        "response": response,
        "num_docs": len(docs),
        "context_length": len(context)
    }


# Executar com tracing manual
result = traced_rag_pipeline("What is the typical duration of gamma-ray bursts?")
print(f"Response: {result['response'][:200]}...")
print(f"Docs: {result['num_docs']}, Context: {result['context_length']} chars")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Exam Tips: MLflow Tracing
# MAGIC
# MAGIC 1. **Quando usar Tracing:**
# MAGIC    - Debugging de pipelines RAG complexos
# MAGIC    - Identificar gargalos de latencia
# MAGIC    - Monitorar comportamento em producao
# MAGIC
# MAGIC 2. **Metricas importantes:**
# MAGIC    - Latencia por componente
# MAGIC    - Tamanho do contexto vs qualidade
# MAGIC    - Taxa de cache hit (se implementado)
# MAGIC
# MAGIC 3. **Best Practices:**
# MAGIC    - Habilitar autolog para LangChain
# MAGIC    - Adicionar spans manuais para logica custom
# MAGIC    - Configurar alertas para latencia alta

# COMMAND ----------

# MAGIC %md
# MAGIC ## Proximos Passos
# MAGIC
# MAGIC ### O que foi avaliado:
# MAGIC
# MAGIC | Metrica | Descricao | Score |
# MAGIC |---------|-----------|-------|
# MAGIC | **Keyword Precision** | Keywords esperadas na resposta | Variavel |
# MAGIC | **Faithfulness** | Resposta fiel ao contexto | LLM-as-Judge |
# MAGIC | **Answer Relevance** | Resposta relevante a pergunta | LLM-as-Judge |
# MAGIC | **Context Relevance** | Contexto relevante a pergunta | LLM-as-Judge |
# MAGIC | **MLflow Tracing** | Debugging de pipeline | Habilitado |
# MAGIC
# MAGIC ### Proximo Lab: 05-deployment
# MAGIC
# MAGIC No proximo lab, faremos o deploy do RAG:
# MAGIC 1. Criar modelo PyFunc
# MAGIC 2. Registrar no Unity Catalog
# MAGIC 3. Deploy como Model Serving endpoint
# MAGIC 4. Testar endpoint via REST API

