# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 4.1: Building a Retriever with Vector Search
# MAGIC
# MAGIC Este notebook configura o retriever usando o índice Vector Search criado no Lab 3.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Conectar ao índice Vector Search existente
# MAGIC 2. Criar retriever com LangChain
# MAGIC 3. Testar diferentes estratégias de retrieval
# MAGIC 4. Implementar filtros por tipo de evento
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 3: Application Development (30%)
# MAGIC - Query Vector Search index for similar documents
# MAGIC - Design retrieval system using LangChain

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install databricks-vectorsearch langchain langchain-community mlflow -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports e configuração
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.embeddings import DatabricksEmbeddings
from langchain.schema import Document
import mlflow

# Carregar configuração do Lab 3
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Carregar configurações salvas
config_df = spark.table("rag_config").collect()
config = {row.key: row.value for row in config_df}

VS_ENDPOINT = config.get("VS_ENDPOINT", "nasa_gcn_vs_endpoint")
VS_INDEX = config.get("VS_INDEX", f"{CATALOG}.{SCHEMA}.gcn_chunks_vs_index")
EMBEDDING_MODEL = config.get("EMBEDDING_MODEL", "databricks-bge-large-en")

print(f"""
⚙️ Configuração carregada:
  - VS Endpoint: {VS_ENDPOINT}
  - VS Index: {VS_INDEX}
  - Embedding Model: {EMBEDDING_MODEL}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Conectar ao Vector Search

# COMMAND ----------

# DBTITLE 1,Verificar status do índice
vsc = VectorSearchClient()

# Verificar índice
index_info = vsc.get_index(VS_ENDPOINT, VS_INDEX)
status = index_info.get("status", {})

print(f"""
📊 Status do Índice:
  - Ready: {status.get('ready', False)}
  - State: {status.get('detailed_state', 'UNKNOWN')}
  - Indexed rows: {status.get('indexed_row_count', 'N/A')}
""")

if not status.get('ready', False):
    print("⚠️ Índice ainda não está pronto. Aguarde a sincronização.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar Retriever com LangChain

# COMMAND ----------

# DBTITLE 1,Configurar DatabricksVectorSearch
# Criar instância do Vector Search para LangChain
dvs = DatabricksVectorSearch(
    endpoint=VS_ENDPOINT,
    index_name=VS_INDEX,
    text_column="chunk_text",  # Coluna com o texto
    columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"]  # Colunas a retornar
)

# Converter para retriever
retriever = dvs.as_retriever(
    search_kwargs={
        "k": 5  # Número de documentos a retornar
    }
)

print("✅ Retriever configurado")
print(f"   - Top K: 5")
print(f"   - Text column: chunk_text")

# COMMAND ----------

# DBTITLE 1,Testar retriever básico
# Testar com uma query simples
query = "What observations were made for gamma-ray bursts?"

print(f"🔍 Query: '{query}'")
print("-" * 60)

docs = retriever.invoke(query)

for i, doc in enumerate(docs):
    print(f"\n📄 Documento {i+1}:")
    print(f"   Event ID: {doc.metadata.get('event_id', 'N/A')}")
    print(f"   Subject: {doc.metadata.get('subject', 'N/A')[:60]}...")
    print(f"   Content: {doc.page_content[:150]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Retriever com Filtros

# COMMAND ----------

# DBTITLE 1,Retriever com filtro por tipo de evento
def create_filtered_retriever(event_type_prefix: str = None, k: int = 5):
    """
    Cria um retriever com filtro opcional por tipo de evento.

    Args:
        event_type_prefix: Prefixo do event_id (ex: "GRB", "GW", "IceCube")
        k: Número de documentos a retornar

    Returns:
        Retriever configurado
    """
    search_kwargs = {"k": k}

    if event_type_prefix:
        # Filtro por prefixo do event_id
        search_kwargs["filters"] = {
            "event_id LIKE": f"{event_type_prefix}%"
        }

    return dvs.as_retriever(search_kwargs=search_kwargs)

# Exemplo: Retriever apenas para GRBs
grb_retriever = create_filtered_retriever("GRB", k=3)

print("🎯 Testando retriever filtrado para GRBs:")
grb_docs = grb_retriever.invoke("optical afterglow observation")

for doc in grb_docs:
    print(f"   - {doc.metadata.get('event_id')}: {doc.page_content[:100]}...")

# COMMAND ----------

# DBTITLE 1,Retriever para ondas gravitacionais
# Retriever para eventos de ondas gravitacionais
gw_retriever = create_filtered_retriever("S", k=3)  # S190425z, etc.

print("🌊 Testando retriever filtrado para GW (S*):")
gw_docs = gw_retriever.invoke("binary neutron star merger")

for doc in gw_docs:
    print(f"   - {doc.metadata.get('event_id')}: {doc.page_content[:100]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Retriever Avançado: Multi-Query

# COMMAND ----------

# DBTITLE 1,Multi-Query Retriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.chat_models import ChatDatabricks

# LLM para gerar queries alternativas
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.1
)

# Multi-Query Retriever gera múltiplas versões da query
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

print("✅ Multi-Query Retriever configurado")
print("   Este retriever gera várias versões da pergunta para melhor cobertura")

# COMMAND ----------

# DBTITLE 1,Testar Multi-Query Retriever
# Testar com query que pode ter múltiplas interpretações
query = "neutrino detection from astrophysical source"

print(f"🔍 Query original: '{query}'")
print("-" * 60)

# O multi-query retriever vai gerar variações da pergunta
multi_docs = multi_retriever.invoke(query)

print(f"\n📊 Total de documentos únicos recuperados: {len(multi_docs)}")
for i, doc in enumerate(multi_docs[:5]):
    print(f"\n📄 Documento {i+1}:")
    print(f"   Event: {doc.metadata.get('event_id', 'N/A')}")
    print(f"   Content: {doc.page_content[:120]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Contextual Compression

# COMMAND ----------

# DBTITLE 1,Compression Retriever para respostas mais focadas
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Compressor extrai apenas partes relevantes do documento
compressor = LLMChainExtractor.from_llm(llm)

# Compression retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

print("✅ Compression Retriever configurado")
print("   Este retriever extrai apenas as partes relevantes de cada documento")

# COMMAND ----------

# DBTITLE 1,Testar Compression Retriever
query = "What telescope observed the optical counterpart?"

print(f"🔍 Query: '{query}'")
print("-" * 60)

compressed_docs = compression_retriever.invoke(query)

print(f"\n📊 Documentos comprimidos: {len(compressed_docs)}")
for i, doc in enumerate(compressed_docs[:3]):
    print(f"\n📄 Documento {i+1} (comprimido):")
    print(f"   Event: {doc.metadata.get('event_id', 'N/A')}")
    print(f"   Extracted content: {doc.page_content}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Comparação de Estratégias

# COMMAND ----------

# DBTITLE 1,Benchmark das estratégias
import time

test_queries = [
    "Fermi GBM triggered on gamma-ray burst",
    "IceCube high energy neutrino alert",
    "optical follow-up observation magnitude",
    "Swift XRT X-ray afterglow position"
]

results = []

for query in test_queries:
    # Basic retriever
    start = time.time()
    basic_docs = retriever.invoke(query)
    basic_time = time.time() - start

    # Multi-query (skip for speed in demo)
    # multi_docs = multi_retriever.invoke(query)

    results.append({
        "query": query[:40],
        "basic_docs": len(basic_docs),
        "basic_time_ms": basic_time * 1000
    })

# Mostrar resultados
print("📊 Comparação de Estratégias de Retrieval:")
print("-" * 70)
print(f"{'Query':<45} {'Docs':>8} {'Time(ms)':>10}")
print("-" * 70)

for r in results:
    print(f"{r['query']:<45} {r['basic_docs']:>8} {r['basic_time_ms']:>10.1f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Salvar Retriever para Próximo Notebook

# COMMAND ----------

# DBTITLE 1,Função de retrieval para reutilização
def get_nasa_gcn_retriever(
    k: int = 5,
    event_filter: str = None,
    use_compression: bool = False
):
    """
    Factory function para criar retriever configurado.

    Args:
        k: Número de documentos a retornar
        event_filter: Prefixo do event_id para filtrar (ex: "GRB")
        use_compression: Se True, usa compression retriever

    Returns:
        Retriever configurado
    """
    vsc = VectorSearchClient()

    dvs = DatabricksVectorSearch(
        endpoint=VS_ENDPOINT,
        index_name=VS_INDEX,
        text_column="chunk_text",
        columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"]
    )

    search_kwargs = {"k": k}
    if event_filter:
        search_kwargs["filters"] = {"event_id LIKE": f"{event_filter}%"}

    base_retriever = dvs.as_retriever(search_kwargs=search_kwargs)

    if use_compression:
        llm = ChatDatabricks(
            endpoint="databricks-meta-llama-3-1-70b-instruct",
            temperature=0.1
        )
        compressor = LLMChainExtractor.from_llm(llm)
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

    return base_retriever

# Salvar configuração
print("""
✅ Retriever factory function definida: get_nasa_gcn_retriever()

Uso no próximo notebook:
  retriever = get_nasa_gcn_retriever(k=5)
  retriever = get_nasa_gcn_retriever(k=3, event_filter="GRB")
  retriever = get_nasa_gcn_retriever(k=5, use_compression=True)
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo e Próximos Passos
# MAGIC
# MAGIC ### O que foi implementado:
# MAGIC
# MAGIC | Retriever | Descrição | Uso Recomendado |
# MAGIC |-----------|-----------|-----------------|
# MAGIC | **Basic** | Busca vetorial simples | Queries diretas |
# MAGIC | **Filtered** | Filtro por tipo de evento | Queries específicas (GRB, GW) |
# MAGIC | **Multi-Query** | Gera variações da pergunta | Queries ambíguas |
# MAGIC | **Compression** | Extrai partes relevantes | Respostas precisas |
# MAGIC
# MAGIC ### Próximo Notebook: 02-rag-chain.py
# MAGIC
# MAGIC No próximo notebook, construiremos a chain RAG completa:
# MAGIC 1. Integrar retriever com LLM
# MAGIC 2. Criar prompt template para astronomia
# MAGIC 3. Implementar RAG chain com LangChain
# MAGIC 4. Adicionar citações de fontes

