# Lab 4: Building a RAG Application

Este lab constrói uma aplicação RAG (Retrieval-Augmented Generation) para responder perguntas sobre eventos astronômicos usando os GCN Circulars.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Configurar retrievers** com DatabricksVectorSearch e LangChain
2. **Construir RAG chains** com prompts especializados
3. **Implementar RAG conversacional** com histórico de mensagens
4. **Avaliar qualidade do RAG** com métricas específicas
5. **Logar experimentos** com MLflow

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 3: Application Development** | 30% | RAG chain, retrievers, prompts, LangChain |
| **Section 4: Evaluation and Monitoring** | 18% | RAG metrics, MLflow logging, LLM-as-judge |

## Pré-requisitos

- **Lab 3 completo:** Vector Search index criado e sincronizado
- Tabela `rag_config` com configurações
- Acesso ao modelo `databricks-meta-llama-3-1-70b-instruct`

## Estrutura do Lab

```
lab-04-rag-app/
├── 01-retriever.py              # Configuração de retrievers
├── 02-rag-chain.py              # Construção da RAG chain
├── 03-evaluation.py             # Avaliação com MLflow
└── README.md                    # Este arquivo
```

## Notebooks

### 1. Retriever (`01-retriever.py`)

**O que você vai aprender:**
- Conectar ao Vector Search index via LangChain
- Criar retrievers básicos e filtrados
- Implementar Multi-Query Retriever
- Usar Contextual Compression

**Estratégias de Retrieval:**

| Estratégia | Uso | Vantagem |
|------------|-----|----------|
| **Basic** | Queries diretas | Simples e rápido |
| **Filtered** | Filtro por event_type | Resultados focados |
| **Multi-Query** | Queries ambíguas | Melhor cobertura |
| **Compression** | Respostas precisas | Contexto extraído |

### 2. RAG Chain (`02-rag-chain.py`)

**O que você vai aprender:**
- Criar prompt templates para astronomia
- Integrar retriever com LLM
- Implementar RAG com citações
- Construir RAG conversacional

**Componentes da Chain:**

```
Question → Retriever → Format Context → Prompt → LLM → Response
                                  ↓
                            Citations (event_ids)
```

**Exemplo de uso:**
```python
# RAG com citações
result = rag_with_citations("What caused the gamma-ray burst?")
print(result["answer"])
print(result["sources"])  # ['GRB 251208B', 'GRB 251207A']
```

### 3. Evaluation (`03-evaluation.py`)

**O que você vai aprender:**
- Definir métricas de avaliação RAG
- Implementar LLM-as-Judge
- Comparar configurações (diferentes K)
- Logar resultados com MLflow

**Métricas implementadas:**

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| **Keyword Precision** | Retrieval | % keywords esperadas na resposta |
| **Context Relevance** | Retrieval | Relevância do contexto (LLM judge) |
| **Faithfulness** | Generation | Resposta fiel ao contexto |
| **Answer Relevance** | Generation | Resposta relevante à pergunta |

## Perguntas de Exemplo

```python
# GRB Questions
"What observations were made for gamma-ray bursts detected by Fermi GBM?"
"What are the coordinates and position errors for recent GRB detections?"

# Neutrino Questions
"What high-energy neutrino events were detected by IceCube?"

# Follow-up Questions
"What optical telescopes conducted follow-up observations?"

# X-ray Questions
"What X-ray afterglows were detected by Swift XRT?"
```

## Recursos Criados

| Recurso | Nome Completo | Tipo |
|---------|---------------|------|
| Test Questions | `sandbox.nasa_gcn_dev.rag_test_questions` | Delta Table |
| Eval History | `sandbox.nasa_gcn_dev.rag_evaluation_history` | Delta Table |
| MLflow Experiment | `nasa_gcn_rag_evaluation` | MLflow |

## Comandos Úteis

### Testar retrieval
```python
from langchain_community.vectorstores import DatabricksVectorSearch

dvs = DatabricksVectorSearch(
    endpoint="nasa_gcn_vs_endpoint",
    index_name="sandbox.nasa_gcn_dev.gcn_chunks_vs_index",
    text_column="chunk_text"
)

retriever = dvs.as_retriever(search_kwargs={"k": 5})
docs = retriever.invoke("gamma-ray burst observation")
```

### Ver experimentos MLflow
```python
import mlflow

mlflow.set_experiment("/Users/.../nasa_gcn_rag_evaluation")
runs = mlflow.search_runs()
print(runs[["run_id", "metrics.avg_keyword_precision"]])
```

### RAG com filtro
```python
# Apenas GRBs
grb_retriever = dvs.as_retriever(
    search_kwargs={
        "k": 5,
        "filters": {"event_id LIKE": "GRB%"}
    }
)
```

## Arquitetura RAG

```
┌──────────────────────────────────────────────────────────────┐
│                     NASA GCN RAG System                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  User Question                                                │
│       │                                                       │
│       ▼                                                       │
│  ┌─────────────┐    ┌──────────────────┐                     │
│  │  Retriever  │───▶│  Vector Search   │                     │
│  │  (k=5)      │    │  Index           │                     │
│  └─────────────┘    └──────────────────┘                     │
│       │                                                       │
│       ▼                                                       │
│  ┌─────────────┐                                              │
│  │  Format     │  GCN Circulars context                      │
│  │  Context    │  with event_ids                             │
│  └─────────────┘                                              │
│       │                                                       │
│       ▼                                                       │
│  ┌─────────────┐    ┌──────────────────┐                     │
│  │  Prompt     │───▶│  System: Expert   │                     │
│  │  Template   │    │  astrophysicist   │                     │
│  └─────────────┘    └──────────────────┘                     │
│       │                                                       │
│       ▼                                                       │
│  ┌─────────────┐                                              │
│  │  LLM        │  Llama 3.1 70B                              │
│  │  (temp=0.1) │                                              │
│  └─────────────┘                                              │
│       │                                                       │
│       ▼                                                       │
│  Answer + Citations                                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Erro: "Index not ready"
```python
# Verificar status
vsc = VectorSearchClient()
index_info = vsc.get_index("nasa_gcn_vs_endpoint", "sandbox.nasa_gcn_dev.gcn_chunks_vs_index")
print(index_info.get("status"))

# Aguardar sincronização
import time
while not index_info.get("status", {}).get("ready"):
    time.sleep(30)
    index_info = vsc.get_index(...)
```

### Erro: "Model endpoint not found"
```python
# Verificar endpoints disponíveis
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
endpoints = w.serving_endpoints.list()
for e in endpoints:
    print(e.name)
```

### Respostas pobres
1. Aumentar K (mais contexto)
2. Verificar qualidade dos chunks (Lab 3)
3. Ajustar prompt template
4. Usar Compression Retriever

## Próximos Passos

Após completar este lab, continue para:

- **Lab 5: Deployment** - Deploy do modelo como endpoint
- **Lab 6: Model Management** - Versionamento e governance

## Referências

- [LangChain RAG Documentation](https://python.langchain.com/docs/use_cases/question_answering/)
- [Databricks Vector Search](https://docs.databricks.com/en/generative-ai/vector-search.html)
- [MLflow LLM Evaluate](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html)

---

*Última atualização: Fevereiro 2026*
