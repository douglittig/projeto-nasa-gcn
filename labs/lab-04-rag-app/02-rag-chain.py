# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 4.2: Building a RAG Chain for Astronomical Q&A
# MAGIC
# MAGIC Este notebook constrói uma chain RAG completa para responder perguntas sobre eventos astronômicos.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Criar prompt template para astronomia
# MAGIC 2. Integrar retriever com LLM
# MAGIC 3. Implementar RAG chain com citações
# MAGIC 4. Testar com diferentes tipos de perguntas
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 3: Application Development (30%)
# MAGIC - Build RAG chain using LangChain
# MAGIC - Implement prompt templates for structured output
# MAGIC - Configure Foundation Model API calls

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install databricks-vectorsearch langchain langchain-community mlflow -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.chat_models import ChatDatabricks
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.schema import Document
import mlflow

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
print(f"   VS Index: {VS_INDEX}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Configurar Retriever

# COMMAND ----------

# DBTITLE 1,Criar retriever
vsc = VectorSearchClient()

# Verificar índice
index_info = vsc.get_index(VS_ENDPOINT, VS_INDEX)
print(f"📊 Index status: {index_info.get('status', {}).get('ready', False)}")

# Configurar Vector Search
dvs = DatabricksVectorSearch(
    endpoint=VS_ENDPOINT,
    index_name=VS_INDEX,
    text_column="chunk_text",
    columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"]
)

# Criar retriever
retriever = dvs.as_retriever(search_kwargs={"k": 5})

print("✅ Retriever configurado")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Configurar LLM

# COMMAND ----------

# DBTITLE 1,Configurar ChatDatabricks
# Usar Llama 3.1 70B como LLM
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.1,  # Baixa temperatura para respostas mais factuais
    max_tokens=1024
)

print("✅ LLM configurado: databricks-meta-llama-3-1-70b-instruct")

# Teste rápido
test_response = llm.invoke("What is a gamma-ray burst? Answer in one sentence.")
print(f"🧪 Teste: {test_response.content}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Criar Prompt Template

# COMMAND ----------

# DBTITLE 1,Prompt template para astronomia
# Template específico para eventos astronômicos
SYSTEM_PROMPT = """You are an expert astrophysics assistant specializing in transient astronomical events.
Your role is to answer questions about gamma-ray bursts (GRBs), gravitational waves (GW), neutrino detections,
and other astronomical transients using ONLY the provided GCN Circulars context.

Guidelines:
1. Base your answers ONLY on the provided context from GCN Circulars
2. If the context doesn't contain enough information, say "I don't have sufficient information in the available GCN Circulars"
3. Always cite the source event_id when referencing specific observations
4. Be precise with coordinates, times, and measurements
5. Use standard astronomical notation (RA/Dec, magnitudes, UTC times)
6. If multiple observations are available, synthesize them coherently

Context from GCN Circulars:
{context}
"""

USER_PROMPT = """Question: {question}

Please provide a detailed answer based on the GCN Circulars context above. Include relevant event IDs as citations."""

# Criar prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", USER_PROMPT)
])

print("✅ Prompt template criado")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Funções Auxiliares

# COMMAND ----------

# DBTITLE 1,Formatar documentos com metadados
def format_docs_with_metadata(docs: list) -> str:
    """
    Formata documentos com metadados para contexto rico.

    Args:
        docs: Lista de documentos do retriever

    Returns:
        String formatada com todos os documentos
    """
    formatted = []

    for i, doc in enumerate(docs, 1):
        event_id = doc.metadata.get("event_id", "Unknown")
        subject = doc.metadata.get("subject", "No subject")
        content = doc.page_content

        formatted.append(f"""
--- GCN Circular {i} ---
Event: {event_id}
Subject: {subject}
Content:
{content}
""")

    return "\n".join(formatted)


def extract_citations(docs: list) -> list:
    """
    Extrai citações únicas dos documentos.

    Args:
        docs: Lista de documentos

    Returns:
        Lista de event_ids únicos
    """
    event_ids = set()
    for doc in docs:
        event_id = doc.metadata.get("event_id")
        if event_id:
            event_ids.add(event_id)
    return sorted(list(event_ids))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Construir RAG Chain

# COMMAND ----------

# DBTITLE 1,RAG Chain básica
# Chain RAG básica
rag_chain = (
    {
        "context": retriever | format_docs_with_metadata,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

print("✅ RAG Chain básica criada")

# COMMAND ----------

# DBTITLE 1,Testar RAG Chain básica
# Teste 1: Pergunta sobre GRB
question1 = "What observations were made for gamma-ray bursts detected by Fermi GBM?"

print(f"🔍 Pergunta: {question1}")
print("-" * 60)

response1 = rag_chain.invoke(question1)
print(f"\n📝 Resposta:\n{response1}")

# COMMAND ----------

# DBTITLE 1,Testar com outros tipos de eventos
# Teste 2: Neutrinos
question2 = "What high-energy neutrino events were detected by IceCube?"

print(f"🔍 Pergunta: {question2}")
print("-" * 60)

response2 = rag_chain.invoke(question2)
print(f"\n📝 Resposta:\n{response2}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. RAG Chain com Citações

# COMMAND ----------

# DBTITLE 1,Chain avançada com citações
def rag_with_citations(question: str) -> dict:
    """
    RAG chain que retorna resposta com citações.

    Args:
        question: Pergunta do usuário

    Returns:
        Dict com answer, sources, e context_used
    """
    # Recuperar documentos
    docs = retriever.invoke(question)

    # Formatar contexto
    context = format_docs_with_metadata(docs)

    # Extrair citações
    citations = extract_citations(docs)

    # Gerar resposta
    messages = prompt.format_messages(context=context, question=question)
    response = llm.invoke(messages)

    return {
        "question": question,
        "answer": response.content,
        "sources": citations,
        "num_docs_used": len(docs),
        "context_preview": context[:500] + "..." if len(context) > 500 else context
    }

# Testar
result = rag_with_citations("What optical telescopes observed gamma-ray burst afterglows?")

print(f"❓ Question: {result['question']}")
print(f"\n📝 Answer:\n{result['answer']}")
print(f"\n📚 Sources ({len(result['sources'])}): {', '.join(result['sources'])}")
print(f"\n📊 Documents used: {result['num_docs_used']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Conversational RAG (com Histórico)

# COMMAND ----------

# DBTITLE 1,Prompt com histórico de conversa
CONVERSATIONAL_SYSTEM_PROMPT = """You are an expert astrophysics assistant specializing in transient astronomical events.
You are having a conversation about GCN Circulars and astronomical observations.

Use the conversation history to understand context and provide consistent answers.
Base your answers ONLY on the provided GCN Circulars context.

Context from GCN Circulars:
{context}
"""

conversational_prompt = ChatPromptTemplate.from_messages([
    ("system", CONVERSATIONAL_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

print("✅ Conversational prompt criado")

# COMMAND ----------

# DBTITLE 1,Classe para RAG conversacional
from langchain_core.messages import HumanMessage, AIMessage

class ConversationalRAG:
    """RAG com memória de conversa."""

    def __init__(self, retriever, llm, prompt):
        self.retriever = retriever
        self.llm = llm
        self.prompt = prompt
        self.chat_history = []

    def ask(self, question: str) -> str:
        """
        Faz uma pergunta mantendo contexto da conversa.

        Args:
            question: Pergunta do usuário

        Returns:
            Resposta do assistente
        """
        # Recuperar documentos
        docs = self.retriever.invoke(question)
        context = format_docs_with_metadata(docs)

        # Formatar prompt com histórico
        messages = self.prompt.format_messages(
            context=context,
            chat_history=self.chat_history,
            question=question
        )

        # Gerar resposta
        response = self.llm.invoke(messages)
        answer = response.content

        # Atualizar histórico
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer))

        return answer

    def clear_history(self):
        """Limpa o histórico de conversa."""
        self.chat_history = []


# Criar instância
conv_rag = ConversationalRAG(retriever, llm, conversational_prompt)

print("✅ Conversational RAG criado")

# COMMAND ----------

# DBTITLE 1,Testar conversa multi-turno
# Conversa sobre GRBs
print("🗣️ Iniciando conversa sobre GRBs...")
print("=" * 60)

# Turno 1
q1 = "What are the main characteristics of gamma-ray bursts?"
print(f"\n👤 User: {q1}")
a1 = conv_rag.ask(q1)
print(f"\n🤖 Assistant: {a1[:500]}...")

# Turno 2 (referência ao contexto anterior)
q2 = "Which instruments detected them?"
print(f"\n👤 User: {q2}")
a2 = conv_rag.ask(q2)
print(f"\n🤖 Assistant: {a2[:500]}...")

# Turno 3
q3 = "Were there any optical follow-up observations?"
print(f"\n👤 User: {q3}")
a3 = conv_rag.ask(q3)
print(f"\n🤖 Assistant: {a3[:500]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Salvar Chain para Próximo Lab

# COMMAND ----------

# DBTITLE 1,Função factory para criar RAG chain
def create_nasa_gcn_rag_chain(
    k: int = 5,
    temperature: float = 0.1,
    max_tokens: int = 1024,
    with_citations: bool = True
):
    """
    Factory function para criar RAG chain configurável.

    Args:
        k: Número de documentos a recuperar
        temperature: Temperatura do LLM
        max_tokens: Máximo de tokens na resposta
        with_citations: Se True, retorna citações

    Returns:
        Função callable que processa perguntas
    """
    # Setup
    vsc = VectorSearchClient()
    dvs = DatabricksVectorSearch(
        endpoint=VS_ENDPOINT,
        index_name=VS_INDEX,
        text_column="chunk_text",
        columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"]
    )
    retriever = dvs.as_retriever(search_kwargs={"k": k})

    llm = ChatDatabricks(
        endpoint="databricks-meta-llama-3-1-70b-instruct",
        temperature=temperature,
        max_tokens=max_tokens
    )

    if with_citations:
        def rag_fn(question: str) -> dict:
            docs = retriever.invoke(question)
            context = format_docs_with_metadata(docs)
            citations = extract_citations(docs)

            messages = prompt.format_messages(context=context, question=question)
            response = llm.invoke(messages)

            return {
                "question": question,
                "answer": response.content,
                "sources": citations
            }
        return rag_fn
    else:
        chain = (
            {"context": retriever | format_docs_with_metadata, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain.invoke


print("""
✅ Factory function criada: create_nasa_gcn_rag_chain()

Uso no próximo notebook (evaluation):
  rag = create_nasa_gcn_rag_chain(k=5, with_citations=True)
  result = rag("What caused GRB 251208B?")
  print(result["answer"])
  print(result["sources"])
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Exemplo de Perguntas para Teste

# COMMAND ----------

# DBTITLE 1,Banco de perguntas de teste
# Perguntas de exemplo para avaliação
TEST_QUESTIONS = [
    # GRB Questions
    {
        "question": "What observations were made for gamma-ray bursts detected by Fermi GBM?",
        "expected_topics": ["Fermi", "GBM", "trigger", "duration", "position"],
        "event_type": "GRB"
    },
    {
        "question": "What are the coordinates and position errors for recent GRB detections?",
        "expected_topics": ["RA", "Dec", "position", "error", "localization"],
        "event_type": "GRB"
    },

    # Neutrino Questions
    {
        "question": "What high-energy neutrino events were detected by IceCube?",
        "expected_topics": ["IceCube", "neutrino", "energy", "alert"],
        "event_type": "IceCube"
    },

    # Follow-up Questions
    {
        "question": "What optical telescopes conducted follow-up observations?",
        "expected_topics": ["optical", "telescope", "magnitude", "follow-up"],
        "event_type": None
    },

    # X-ray Questions
    {
        "question": "What X-ray afterglows were detected by Swift XRT?",
        "expected_topics": ["Swift", "XRT", "X-ray", "afterglow", "position"],
        "event_type": "GRB"
    }
]

# Salvar para próximo notebook
spark.createDataFrame(TEST_QUESTIONS).write.mode("overwrite").saveAsTable("rag_test_questions")

print(f"✅ {len(TEST_QUESTIONS)} perguntas de teste salvas em 'rag_test_questions'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo e Próximos Passos
# MAGIC
# MAGIC ### O que foi implementado:
# MAGIC
# MAGIC | Componente | Descrição |
# MAGIC |------------|-----------|
# MAGIC | **Prompt Template** | Template especializado para astronomia com citações |
# MAGIC | **RAG Chain** | Chain básica com retriever + LLM |
# MAGIC | **RAG com Citações** | Retorna resposta + fontes (event_ids) |
# MAGIC | **Conversational RAG** | Mantém histórico de conversa |
# MAGIC | **Test Questions** | Banco de perguntas para avaliação |
# MAGIC
# MAGIC ### Próximo Notebook: 03-evaluation.py
# MAGIC
# MAGIC No próximo notebook, avaliaremos a qualidade do RAG:
# MAGIC 1. Métricas de retrieval (precision, recall)
# MAGIC 2. Métricas de geração (faithfulness, relevance)
# MAGIC 3. Comparação de configurações
# MAGIC 4. Logging com MLflow

