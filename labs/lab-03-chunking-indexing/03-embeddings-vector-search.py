# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 3.3: Embeddings & Vector Search
# MAGIC
# MAGIC Este notebook gera embeddings e cria um índice Vector Search para os chunks dos GCN Circulars.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Gerar embeddings usando databricks-bge-large-en
# MAGIC 2. Criar índice Vector Search com Delta Sync
# MAGIC 3. Testar retrieval semântico
# MAGIC 4. Avaliar qualidade do retrieval
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 3: Application Development (30%)
# MAGIC - Create and query Vector Search index
# MAGIC - Select best embedding model based on requirements

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install databricks-vectorsearch mlflow -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports e configuração
from databricks.vector_search.client import VectorSearchClient
from pyspark.sql.functions import col, lit
import mlflow

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"
SOURCE_TABLE = f"{CATALOG}.{SCHEMA}.gcn_circulars_chunks"

# Vector Search config
VS_ENDPOINT = "nasa_gcn_vs_endpoint"  # Nome do endpoint
VS_INDEX = f"{CATALOG}.{SCHEMA}.gcn_chunks_vs_index"  # Nome do índice

# Embedding model
EMBEDDING_MODEL = "databricks-bge-large-en"  # 1024 dimensions

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print(f"""
⚙️ Configuração:
  - Source Table: {SOURCE_TABLE}
  - VS Endpoint: {VS_ENDPOINT}
  - VS Index: {VS_INDEX}
  - Embedding Model: {EMBEDDING_MODEL}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Preparar Tabela Source com Primary Key

# COMMAND ----------

# DBTITLE 1,Verificar tabela source
# Verificar estrutura da tabela de chunks
df_chunks = spark.table(SOURCE_TABLE)
print("📋 Schema da tabela de chunks:")
df_chunks.printSchema()

print(f"\n📊 Total de chunks: {df_chunks.count():,}")

# COMMAND ----------

# DBTITLE 1,Habilitar Change Data Feed (necessário para Delta Sync)
# Delta Sync requer Change Data Feed habilitado
spark.sql(f"""
ALTER TABLE {SOURCE_TABLE}
SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

print(f"✅ Change Data Feed habilitado para {SOURCE_TABLE}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar Vector Search Endpoint
# MAGIC
# MAGIC O endpoint é o compute resource que hospeda os índices.

# COMMAND ----------

# DBTITLE 1,Criar ou conectar ao endpoint
vsc = VectorSearchClient()

# Listar endpoints existentes
existing_endpoints = vsc.list_endpoints()
endpoint_names = [ep.get("name") for ep in existing_endpoints.get("endpoints", [])]

if VS_ENDPOINT in endpoint_names:
    print(f"✅ Endpoint '{VS_ENDPOINT}' já existe")
else:
    print(f"🔄 Criando endpoint '{VS_ENDPOINT}'...")
    vsc.create_endpoint(
        name=VS_ENDPOINT,
        endpoint_type="STANDARD"  # STANDARD para prod, STARTER para dev
    )
    print(f"✅ Endpoint '{VS_ENDPOINT}' criado")

# Verificar status
endpoint_info = vsc.get_endpoint(VS_ENDPOINT)
print(f"📍 Status: {endpoint_info.get('endpoint_status', {}).get('state', 'UNKNOWN')}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Criar Vector Search Index com Delta Sync
# MAGIC
# MAGIC Delta Sync mantém o índice automaticamente sincronizado com a tabela source.

# COMMAND ----------

# DBTITLE 1,Criar índice
# Verificar se índice já existe
try:
    existing_index = vsc.get_index(VS_ENDPOINT, VS_INDEX)
    print(f"✅ Índice '{VS_INDEX}' já existe")
    print(f"   Status: {existing_index.get('status', {}).get('ready', False)}")
except Exception as e:
    if "NOT_FOUND" in str(e) or "does not exist" in str(e).lower():
        print(f"🔄 Criando índice '{VS_INDEX}'...")

        # Criar índice com Delta Sync
        vsc.create_delta_sync_index(
            endpoint_name=VS_ENDPOINT,
            index_name=VS_INDEX,
            source_table_name=SOURCE_TABLE,
            primary_key="chunk_id",  # Chave única para cada chunk
            embedding_source_column="document_for_embedding",  # Coluna para gerar embeddings
            embedding_model_endpoint_name=EMBEDDING_MODEL,  # Modelo de embedding
            pipeline_type="TRIGGERED"  # TRIGGERED ou CONTINUOUS
        )

        print(f"✅ Índice '{VS_INDEX}' criado!")
        print("⏳ Aguardando sincronização inicial (pode levar alguns minutos)...")
    else:
        raise e

# COMMAND ----------

# DBTITLE 1,Monitorar status do índice
import time

def wait_for_index_ready(vsc, endpoint, index_name, timeout_minutes=30):
    """Aguarda o índice ficar pronto."""
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    while True:
        try:
            index_info = vsc.get_index(endpoint, index_name)
            status = index_info.get("status", {})
            ready = status.get("ready", False)
            state = status.get("detailed_state", "UNKNOWN")

            elapsed = time.time() - start_time
            print(f"  [{elapsed/60:.1f}min] Status: {state}, Ready: {ready}")

            if ready:
                return True

            if elapsed > timeout_seconds:
                print("⏰ Timeout atingido")
                return False

            time.sleep(30)  # Checar a cada 30 segundos
        except Exception as e:
            print(f"  Erro: {e}")
            time.sleep(30)

# Aguardar índice
print("⏳ Aguardando índice ficar pronto...")
is_ready = wait_for_index_ready(vsc, VS_ENDPOINT, VS_INDEX, timeout_minutes=15)

if is_ready:
    print("✅ Índice pronto para uso!")
else:
    print("⚠️ Índice ainda não está pronto. Continue mais tarde.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Testar Retrieval

# COMMAND ----------

# DBTITLE 1,Função de busca
def search_similar_chunks(query: str, num_results: int = 5, filters: dict = None):
    """
    Busca chunks similares usando Vector Search.

    Args:
        query: Texto da query
        num_results: Número de resultados
        filters: Filtros adicionais (ex: {"event_id": "GRB 251208B"})

    Returns:
        Lista de resultados com scores
    """
    index = vsc.get_index(VS_ENDPOINT, VS_INDEX)

    results = index.similarity_search(
        query_text=query,
        columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"],
        num_results=num_results,
        filters=filters
    )

    return results

# COMMAND ----------

# DBTITLE 1,Teste 1: Busca geral
# Buscar informações sobre GRBs
query1 = "What observations were made for gamma-ray bursts?"

print(f"🔍 Query: '{query1}'")
print("-" * 60)

results1 = search_similar_chunks(query1, num_results=5)

for i, row in enumerate(results1.get("result", {}).get("data_array", [])):
    chunk_id, event_id, subject, chunk_text, chunk_idx = row[:5]
    score = row[-1] if len(row) > 5 else "N/A"
    print(f"\n📄 Resultado {i+1} (score: {score}):")
    print(f"   Event: {event_id}")
    print(f"   Subject: {subject[:60]}...")
    print(f"   Chunk: {chunk_text[:150]}...")

# COMMAND ----------

# DBTITLE 1,Teste 2: Busca sobre neutrinos
query2 = "IceCube neutrino detection high energy event"

print(f"🔍 Query: '{query2}'")
print("-" * 60)

results2 = search_similar_chunks(query2, num_results=3)

for i, row in enumerate(results2.get("result", {}).get("data_array", [])):
    chunk_id, event_id, subject, chunk_text, chunk_idx = row[:5]
    print(f"\n📄 Resultado {i+1}:")
    print(f"   Event: {event_id}")
    print(f"   Text: {chunk_text[:200]}...")

# COMMAND ----------

# DBTITLE 1,Teste 3: Busca sobre ondas gravitacionais
query3 = "gravitational wave binary neutron star merger"

print(f"🔍 Query: '{query3}'")
print("-" * 60)

results3 = search_similar_chunks(query3, num_results=3)

for i, row in enumerate(results3.get("result", {}).get("data_array", [])):
    chunk_id, event_id, subject, chunk_text, chunk_idx = row[:5]
    print(f"\n📄 Resultado {i+1}:")
    print(f"   Event: {event_id}")
    print(f"   Text: {chunk_text[:200]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Avaliar Qualidade do Retrieval

# COMMAND ----------

# DBTITLE 1,Criar dataset de avaliação
# Queries de teste com resultados esperados
eval_queries = [
    {
        "query": "Fermi GBM observation of gamma-ray burst",
        "expected_keywords": ["Fermi", "GBM", "GRB", "burst"],
        "expected_event_prefix": "GRB"
    },
    {
        "query": "optical counterpart follow-up observation",
        "expected_keywords": ["optical", "magnitude", "telescope"],
        "expected_event_prefix": None
    },
    {
        "query": "X-ray afterglow Swift XRT detection",
        "expected_keywords": ["Swift", "XRT", "X-ray", "afterglow"],
        "expected_event_prefix": None
    }
]

# COMMAND ----------

# DBTITLE 1,Avaliar retrieval
def evaluate_retrieval(eval_data: list, k: int = 5):
    """Avalia qualidade do retrieval."""
    results = []

    for item in eval_data:
        query = item["query"]
        expected_keywords = item["expected_keywords"]

        search_results = search_similar_chunks(query, num_results=k)
        data_array = search_results.get("result", {}).get("data_array", [])

        # Calcular métricas
        keyword_hits = 0
        total_checks = 0

        for row in data_array:
            chunk_text = row[3].lower() if len(row) > 3 else ""
            for keyword in expected_keywords:
                total_checks += 1
                if keyword.lower() in chunk_text:
                    keyword_hits += 1

        precision = keyword_hits / total_checks if total_checks > 0 else 0

        results.append({
            "query": query[:50],
            "num_results": len(data_array),
            "keyword_precision": precision
        })

    return results

# Avaliar
eval_results = evaluate_retrieval(eval_queries, k=5)

print("📊 Resultados da Avaliação:")
print("-" * 60)
for r in eval_results:
    print(f"Query: {r['query']}...")
    print(f"  Resultados: {r['num_results']}, Keyword Precision: {r['keyword_precision']:.2%}")
    print()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Informações do Índice

# COMMAND ----------

# DBTITLE 1,Estatísticas do índice
# Obter informações do índice
index_info = vsc.get_index(VS_ENDPOINT, VS_INDEX)

print(f"""
📊 Informações do Índice:
─────────────────────────
Nome:           {VS_INDEX}
Endpoint:       {VS_ENDPOINT}
Status:         {index_info.get('status', {}).get('detailed_state', 'UNKNOWN')}
Ready:          {index_info.get('status', {}).get('ready', False)}

Configuração:
  - Source Table:     {SOURCE_TABLE}
  - Primary Key:      chunk_id
  - Embedding Column: document_for_embedding
  - Embedding Model:  {EMBEDDING_MODEL}
  - Pipeline Type:    TRIGGERED

📍 Para sincronizar manualmente:
   vsc.get_index("{VS_ENDPOINT}", "{VS_INDEX}").sync()
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Salvar Configuração para Próximos Labs

# COMMAND ----------

# DBTITLE 1,Salvar configuração em tabela
# Criar tabela de configuração para referência nos próximos labs
config_data = [
    ("VS_ENDPOINT", VS_ENDPOINT),
    ("VS_INDEX", VS_INDEX),
    ("SOURCE_TABLE", SOURCE_TABLE),
    ("EMBEDDING_MODEL", EMBEDDING_MODEL),
    ("CATALOG", CATALOG),
    ("SCHEMA", SCHEMA)
]

df_config = spark.createDataFrame(config_data, ["key", "value"])
df_config.write.mode("overwrite").saveAsTable("rag_config")

print("✅ Configuração salva em rag_config")
spark.table("rag_config").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo e Próximos Passos
# MAGIC
# MAGIC ### O que foi criado:
# MAGIC
# MAGIC | Recurso | Nome | Descrição |
# MAGIC |---------|------|-----------|
# MAGIC | Tabela de Chunks | `gcn_circulars_chunks` | Chunks dos circulars com texto formatado |
# MAGIC | VS Endpoint | `nasa_gcn_vs_endpoint` | Compute para Vector Search |
# MAGIC | VS Index | `gcn_chunks_vs_index` | Índice vetorial com Delta Sync |
# MAGIC | Config Table | `rag_config` | Configurações para próximos labs |
# MAGIC
# MAGIC ### Próximo Lab: 04-rag-app
# MAGIC
# MAGIC No próximo lab, usaremos este índice para:
# MAGIC 1. Criar um retriever com LangChain
# MAGIC 2. Construir uma chain RAG
# MAGIC 3. Responder perguntas sobre eventos astronômicos
# MAGIC
# MAGIC ```python
# MAGIC # Preview do próximo lab
# MAGIC from langchain.vectorstores import DatabricksVectorSearch
# MAGIC
# MAGIC retriever = DatabricksVectorSearch(
# MAGIC     endpoint=VS_ENDPOINT,
# MAGIC     index_name=VS_INDEX
# MAGIC ).as_retriever()
# MAGIC
# MAGIC # RAG Chain
# MAGIC chain = create_retrieval_chain(retriever, llm)
# MAGIC response = chain.invoke({"input": "What caused GRB 251208B?"})
# MAGIC ```
