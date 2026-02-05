# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 9.1: Embedding Strategies for RAG Optimization
# MAGIC
# MAGIC Este notebook explora diferentes estratégias de embedding para otimizar retrieval.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Comparar modelos de embedding
# MAGIC 2. Avaliar impacto de dimensionalidade
# MAGIC 3. Implementar embedding batching
# MAGIC 4. Medir trade-offs de performance
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 3: Application Development (30%)
# MAGIC - Select embedding model based on requirements
# MAGIC - Optimize embedding generation for scale

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql.functions import col, lit, length, udf, size, array
from pyspark.sql.types import ArrayType, FloatType, StructType, StructField, StringType
import time
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Modelos de Embedding Disponíveis

# COMMAND ----------

# DBTITLE 1,Listar modelos disponíveis
EMBEDDING_MODELS = {
    "databricks-bge-large-en": {
        "dimensions": 1024,
        "max_tokens": 512,
        "description": "BGE Large English - High quality, larger model",
        "use_case": "Production RAG with high accuracy requirements"
    },
    "databricks-gte-large-en": {
        "dimensions": 1024,
        "max_tokens": 512,
        "description": "GTE Large English - Balanced performance",
        "use_case": "General purpose RAG applications"
    },
    "databricks-e5-large-v2": {
        "dimensions": 1024,
        "max_tokens": 512,
        "description": "E5 Large V2 - Good for asymmetric search",
        "use_case": "Question-document matching"
    }
}

print("📋 Modelos de Embedding Disponíveis no Databricks:")
for model, info in EMBEDDING_MODELS.items():
    print(f"\n  {model}:")
    print(f"    Dimensions: {info['dimensions']}")
    print(f"    Max Tokens: {info['max_tokens']}")
    print(f"    Description: {info['description']}")
    print(f"    Use Case: {info['use_case']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Gerar Embeddings com API

# COMMAND ----------

# DBTITLE 1,Função para gerar embeddings
import requests
import os

def get_embedding(text: str, model: str = "databricks-bge-large-en") -> list:
    """
    Gera embedding para um texto usando Databricks Foundation Model API.

    Args:
        text: Texto para gerar embedding
        model: Nome do modelo de embedding

    Returns:
        Lista de floats representando o embedding
    """
    # Em ambiente Databricks, usar o endpoint interno
    token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
    host = spark.conf.get("spark.databricks.workspaceUrl")

    url = f"https://{host}/serving-endpoints/{model}/invocations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": [text]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("data", [{}])[0].get("embedding", [])
    except Exception as e:
        print(f"Error: {e}")
        return []


# Testar
test_text = "Gamma-ray burst detected by Fermi GBM"
print(f"🔍 Testing embedding generation...")
print(f"   Text: '{test_text}'")

embedding = get_embedding(test_text)
print(f"   Dimensions: {len(embedding)}")
print(f"   First 5 values: {embedding[:5]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Batch Embedding para Eficiência

# COMMAND ----------

# DBTITLE 1,Função de batch embedding
def get_embeddings_batch(texts: list, model: str = "databricks-bge-large-en", batch_size: int = 20) -> list:
    """
    Gera embeddings para múltiplos textos em batches.

    Args:
        texts: Lista de textos
        model: Nome do modelo
        batch_size: Tamanho do batch

    Returns:
        Lista de embeddings
    """
    token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
    host = spark.conf.get("spark.databricks.workspaceUrl")

    url = f"https://{host}/serving-endpoints/{model}/invocations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        payload = {"input": batch}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            batch_embeddings = [item.get("embedding", []) for item in result.get("data", [])]
            all_embeddings.extend(batch_embeddings)

        except Exception as e:
            print(f"Error in batch {i//batch_size}: {e}")
            all_embeddings.extend([[] for _ in batch])

    return all_embeddings


# Testar batch
test_texts = [
    "Gamma-ray burst observation",
    "Neutrino detection by IceCube",
    "Optical follow-up observation",
    "X-ray afterglow detected"
]

print("🔄 Testing batch embedding...")
start_time = time.time()
batch_embeddings = get_embeddings_batch(test_texts, batch_size=4)
elapsed = time.time() - start_time

print(f"   Texts processed: {len(test_texts)}")
print(f"   Time: {elapsed:.2f}s")
print(f"   Throughput: {len(test_texts)/elapsed:.1f} texts/sec")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Comparar Qualidade de Embeddings

# COMMAND ----------

# DBTITLE 1,Calcular similaridade de cosseno
import numpy as np

def cosine_similarity(vec1: list, vec2: list) -> float:
    """Calcula similaridade de cosseno entre dois vetores."""
    if not vec1 or not vec2:
        return 0.0

    a = np.array(vec1)
    b = np.array(vec2)

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# Testar similaridade
queries = [
    "What caused the gamma-ray burst?",
    "How was the neutrino detected?",
    "What is the position of the source?"
]

documents = [
    "Fermi GBM triggered on a gamma-ray burst at 14:32 UTC.",
    "IceCube detected a high-energy neutrino event.",
    "The source position was determined to be RA=123.45, Dec=-67.89."
]

print("📊 Matriz de Similaridade (Query x Document):")
print("-" * 70)

# Gerar embeddings
query_embeddings = get_embeddings_batch(queries)
doc_embeddings = get_embeddings_batch(documents)

# Calcular matriz
print(f"{'Query':<35} | Doc1 | Doc2 | Doc3")
print("-" * 70)

for i, (q, q_emb) in enumerate(zip(queries, query_embeddings)):
    sims = [cosine_similarity(q_emb, d_emb) for d_emb in doc_embeddings]
    sim_str = " | ".join([f"{s:.2f}" for s in sims])
    print(f"{q[:35]:<35} | {sim_str}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Benchmark de Performance

# COMMAND ----------

# DBTITLE 1,Benchmark embedding throughput
def benchmark_embedding_throughput(texts: list, batch_sizes: list = [1, 5, 10, 20]) -> dict:
    """
    Benchmark de throughput para diferentes batch sizes.

    Args:
        texts: Lista de textos para testar
        batch_sizes: Lista de batch sizes para testar

    Returns:
        Dict com resultados do benchmark
    """
    results = {}

    for batch_size in batch_sizes:
        start_time = time.time()
        embeddings = get_embeddings_batch(texts[:50], batch_size=batch_size)  # Limitar para demo
        elapsed = time.time() - start_time

        successful = sum(1 for e in embeddings if e)

        results[batch_size] = {
            "batch_size": batch_size,
            "total_texts": len(texts[:50]),
            "successful": successful,
            "time_seconds": round(elapsed, 2),
            "throughput": round(successful / elapsed, 1) if elapsed > 0 else 0
        }

        print(f"   Batch size {batch_size}: {results[batch_size]['throughput']} texts/sec")

    return results


# Carregar textos de exemplo
sample_texts = spark.table("gcn_circulars_chunks").select("chunk_text").limit(100).collect()
texts = [row.chunk_text for row in sample_texts]

print("📊 Benchmark de Throughput por Batch Size:")
print("-" * 50)
benchmark_results = benchmark_embedding_throughput(texts, batch_sizes=[1, 5, 10, 20])

# COMMAND ----------

# DBTITLE 1,Salvar resultados do benchmark
benchmark_df = spark.createDataFrame([
    {**result, "model": "databricks-bge-large-en", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    for result in benchmark_results.values()
])

benchmark_df.write.mode("append").saveAsTable("embedding_benchmark_results")

print("✅ Resultados salvos em 'embedding_benchmark_results'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Recomendações de Configuração

# COMMAND ----------

# DBTITLE 1,Recomendações
print("""
╔══════════════════════════════════════════════════════════════╗
║          Embedding Configuration Recommendations              ║
╠══════════════════════════════════════════════════════════════╣

📊 Por Caso de Uso:

  PRODUÇÃO (Alta qualidade):
    - Model: databricks-bge-large-en
    - Batch size: 20
    - Max tokens: 512
    - Dimensões: 1024

  DESENVOLVIMENTO (Rápido):
    - Model: databricks-gte-large-en
    - Batch size: 50
    - Max tokens: 256
    - Dimensões: 1024

  GRANDE ESCALA (Milhões de docs):
    - Model: databricks-e5-large-v2
    - Batch size: 100
    - Considerar truncamento agressivo
    - Usar Delta Sync para atualização incremental

📈 Otimizações:
  1. Batch processing sempre que possível
  2. Truncar textos longos antes de embedar
  3. Cache embeddings para textos frequentes
  4. Usar Delta Sync para manter índice atualizado
  5. Monitorar latência e ajustar batch size

╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Modelos Comparados:
# MAGIC
# MAGIC | Modelo | Dimensões | Uso |
# MAGIC |--------|-----------|-----|
# MAGIC | databricks-bge-large-en | 1024 | Produção |
# MAGIC | databricks-gte-large-en | 1024 | Geral |
# MAGIC | databricks-e5-large-v2 | 1024 | Assimétrico |
# MAGIC
# MAGIC ### Próximo Notebook: 02-index-tuning.py
