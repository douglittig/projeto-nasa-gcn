# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 9.2: Vector Search Index Tuning
# MAGIC
# MAGIC Este notebook explora técnicas de otimização do índice Vector Search.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Entender configurações do índice
# MAGIC 2. Otimizar para latência vs precisão
# MAGIC 3. Implementar filtros eficientes
# MAGIC 4. Configurar Delta Sync
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 3: Application Development (30%)
# MAGIC - Configure Vector Search index parameters
# MAGIC - Optimize retrieval performance

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from databricks.vector_search.client import VectorSearchClient
import time
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Carregar config
config_df = spark.table("rag_config").collect()
config = {row.key: row.value for row in config_df}

VS_ENDPOINT = config.get("VS_ENDPOINT", "nasa_gcn_vs_endpoint")
VS_INDEX = config.get("VS_INDEX", f"{CATALOG}.{SCHEMA}.gcn_chunks_vs_index")

vsc = VectorSearchClient()

print(f"""
⚙️ Configuração:
  - Endpoint: {VS_ENDPOINT}
  - Index: {VS_INDEX}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Verificar Configuração Atual do Índice

# COMMAND ----------

# DBTITLE 1,Obter informações do índice
try:
    index_info = vsc.get_index(VS_ENDPOINT, VS_INDEX)

    print("📋 Configuração do Índice:")
    print(f"   Name: {VS_INDEX}")
    print(f"   Status: {index_info.get('status', {}).get('ready', 'Unknown')}")
    print(f"   Indexed rows: {index_info.get('status', {}).get('indexed_row_count', 'N/A')}")

    # Mostrar detalhes
    print("\n📊 Detalhes:")
    for key, value in index_info.items():
        if key != 'status':
            print(f"   {key}: {value}")

except Exception as e:
    print(f"⚠️ Erro ao obter informações do índice: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Tipos de Índice Vector Search

# COMMAND ----------

# DBTITLE 1,Comparação de tipos de índice
INDEX_TYPES = {
    "DELTA_SYNC": {
        "description": "Sincronização automática com tabela Delta",
        "pros": ["Atualização automática", "Fácil manutenção", "Ideal para dados que mudam"],
        "cons": ["Menos controle sobre refresh", "Pode ter lag de sincronização"],
        "use_case": "RAG com dados que são atualizados frequentemente"
    },
    "DIRECT_ACCESS": {
        "description": "Índice estático com embeddings pré-computados",
        "pros": ["Controle total", "Sem overhead de sync", "Embeddings customizados"],
        "cons": ["Atualização manual", "Mais trabalho de manutenção"],
        "use_case": "Dados estáticos ou quando precisa de embeddings customizados"
    }
}

print("📋 Tipos de Índice Vector Search:")
for index_type, info in INDEX_TYPES.items():
    print(f"\n  {index_type}:")
    print(f"    {info['description']}")
    print(f"    Pros: {', '.join(info['pros'])}")
    print(f"    Cons: {', '.join(info['cons'])}")
    print(f"    Use Case: {info['use_case']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Pipeline Types

# COMMAND ----------

# DBTITLE 1,TRIGGERED vs CONTINUOUS
PIPELINE_TYPES = {
    "TRIGGERED": {
        "description": "Sincronização sob demanda",
        "latency": "Minutos (quando triggerado)",
        "cost": "Baixo (paga apenas quando roda)",
        "use_case": "Dados atualizados em batch, updates menos frequentes"
    },
    "CONTINUOUS": {
        "description": "Sincronização em tempo real",
        "latency": "Segundos",
        "cost": "Alto (sempre rodando)",
        "use_case": "Dados que precisam estar atualizados em tempo real"
    }
}

print("📋 Pipeline Types para Delta Sync:")
for ptype, info in PIPELINE_TYPES.items():
    print(f"\n  {ptype}:")
    print(f"    {info['description']}")
    print(f"    Latency: {info['latency']}")
    print(f"    Cost: {info['cost']}")
    print(f"    Use Case: {info['use_case']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Otimizar Queries com Filtros

# COMMAND ----------

# DBTITLE 1,Estratégias de filtro
def search_with_filter(query: str, filter_dict: dict = None, num_results: int = 5) -> dict:
    """
    Executa busca com filtro opcional.

    Args:
        query: Texto da query
        filter_dict: Filtros a aplicar
        num_results: Número de resultados

    Returns:
        Resultados da busca com métricas
    """
    try:
        index = vsc.get_index(VS_ENDPOINT, VS_INDEX)

        start_time = time.time()

        results = index.similarity_search(
            query_text=query,
            columns=["chunk_id", "event_id", "subject", "chunk_text"],
            num_results=num_results,
            filters=filter_dict
        )

        elapsed = time.time() - start_time

        return {
            "query": query,
            "filter": filter_dict,
            "num_results": len(results.get("result", {}).get("data_array", [])),
            "latency_ms": round(elapsed * 1000, 2),
            "results": results
        }

    except Exception as e:
        return {"error": str(e)}


# Testar queries com e sem filtro
print("📊 Comparação: Com Filtro vs Sem Filtro")
print("-" * 60)

query = "gamma-ray burst detection"

# Sem filtro
result_no_filter = search_with_filter(query, filter_dict=None)
print(f"\n   Sem filtro:")
print(f"     Results: {result_no_filter.get('num_results', 0)}")
print(f"     Latency: {result_no_filter.get('latency_ms', 'N/A')}ms")

# Com filtro por event_id prefix
result_with_filter = search_with_filter(query, filter_dict={"event_id LIKE": "GRB%"})
print(f"\n   Com filtro (event_id LIKE 'GRB%'):")
print(f"     Results: {result_with_filter.get('num_results', 0)}")
print(f"     Latency: {result_with_filter.get('latency_ms', 'N/A')}ms")

# COMMAND ----------

# DBTITLE 1,Estratégia de pré-filtragem
print("""
📋 Estratégias de Filtragem Eficiente:

1. COLUMN FILTERS (Recomendado):
   - Filtrar por colunas indexadas
   - Exemplo: {"event_id LIKE": "GRB%"}
   - Performance: O(log n) com índice

2. POST-FILTERING:
   - Buscar primeiro, filtrar depois
   - Exemplo: Recuperar 100, filtrar para 10
   - Performance: Mais lento, mas mais flexível

3. HYBRID APPROACH:
   - Pré-filtro amplo + pós-filtro refinado
   - Exemplo: Filtro por tipo + filtro por data em Python

Recomendação para NASA GCN:
  - Indexar coluna 'event_id' para filtros por tipo (GRB, GW, etc.)
  - Usar filtro no Vector Search para categoria principal
  - Pós-filtrar por data se necessário
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Benchmark de K (Número de Resultados)

# COMMAND ----------

# DBTITLE 1,Impacto do K na latência e qualidade
def benchmark_k_values(query: str, k_values: list = [3, 5, 10, 20, 50]) -> list:
    """
    Benchmark de diferentes valores de K.

    Args:
        query: Query para testar
        k_values: Lista de valores de K

    Returns:
        Lista de resultados
    """
    results = []

    for k in k_values:
        search_result = search_with_filter(query, num_results=k)

        results.append({
            "k": k,
            "actual_results": search_result.get("num_results", 0),
            "latency_ms": search_result.get("latency_ms", 0)
        })

        print(f"   K={k}: {search_result.get('latency_ms', 0):.0f}ms, {search_result.get('num_results', 0)} results")

    return results


print("📊 Benchmark de K (número de resultados):")
print("-" * 50)
k_benchmark = benchmark_k_values("optical afterglow observation")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Sincronização do Índice

# COMMAND ----------

# DBTITLE 1,Verificar status de sincronização
try:
    index = vsc.get_index(VS_ENDPOINT, VS_INDEX)
    index_info = vsc.get_index(VS_ENDPOINT, VS_INDEX)

    sync_status = index_info.get("status", {})

    print(f"""
📊 Status de Sincronização:
   Ready: {sync_status.get('ready', False)}
   State: {sync_status.get('detailed_state', 'UNKNOWN')}
   Indexed rows: {sync_status.get('indexed_row_count', 'N/A')}
   Last sync: {sync_status.get('last_sync_time', 'N/A')}
""")

except Exception as e:
    print(f"⚠️ Erro: {e}")

# COMMAND ----------

# DBTITLE 1,Trigger sync manual (se necessário)
# Descomentar para forçar sincronização
# try:
#     index = vsc.get_index(VS_ENDPOINT, VS_INDEX)
#     index.sync()
#     print("✅ Sync triggered successfully")
# except Exception as e:
#     print(f"⚠️ Erro ao trigger sync: {e}")

print("""
📋 Para sincronizar manualmente:

```python
index = vsc.get_index(VS_ENDPOINT, VS_INDEX)
index.sync()
```

Ou via SDK:
```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
w.vector_search_indexes.sync_index(
    index_name="sandbox.nasa_gcn_dev.gcn_chunks_vs_index"
)
```
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Salvar Configuração Otimizada

# COMMAND ----------

# DBTITLE 1,Configuração recomendada
OPTIMIZED_CONFIG = {
    "index_type": "DELTA_SYNC",
    "pipeline_type": "TRIGGERED",
    "embedding_model": "databricks-bge-large-en",
    "embedding_column": "document_for_embedding",
    "primary_key": "chunk_id",
    "recommended_k": 5,
    "filter_columns": ["event_id"],
    "notes": "Otimizado para queries de astronomia com filtragem por tipo de evento"
}

# Salvar configuração
config_df = spark.createDataFrame([
    (k, str(v)) for k, v in OPTIMIZED_CONFIG.items()
], ["key", "value"])

config_df.write.mode("overwrite").saveAsTable("vs_optimized_config")

print("✅ Configuração otimizada salva em 'vs_optimized_config'")
print(json.dumps(OPTIMIZED_CONFIG, indent=2))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Configurações Recomendadas:
# MAGIC
# MAGIC | Parâmetro | Valor | Justificativa |
# MAGIC |-----------|-------|---------------|
# MAGIC | Index Type | DELTA_SYNC | Atualização automática |
# MAGIC | Pipeline | TRIGGERED | Balance custo/atualização |
# MAGIC | K | 5 | Balance precisão/latência |
# MAGIC | Filtros | event_id | Categorização eficiente |
# MAGIC
# MAGIC ### Próximo Notebook: 03-benchmarking.py
