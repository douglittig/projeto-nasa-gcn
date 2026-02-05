# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 9.3: Retrieval Benchmarking and Evaluation
# MAGIC
# MAGIC Este notebook implementa benchmarks sistemáticos para avaliar qualidade do retrieval.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Criar dataset de benchmark
# MAGIC 2. Medir precision e recall
# MAGIC 3. Avaliar MRR (Mean Reciprocal Rank)
# MAGIC 4. Comparar configurações
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 4: Evaluation and Monitoring (18%)
# MAGIC - Evaluate retrieval quality
# MAGIC - Measure RAG performance metrics

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from databricks.vector_search.client import VectorSearchClient
from pyspark.sql.functions import col
import time
import json
from typing import List, Dict
from dataclasses import dataclass

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

vsc = VectorSearchClient()

print(f"⚙️ Config loaded: {VS_INDEX}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Criar Dataset de Benchmark

# COMMAND ----------

# DBTITLE 1,Dataset com queries e documentos relevantes
# Queries com documentos esperados
BENCHMARK_DATASET = [
    {
        "query": "Fermi GBM triggered on gamma-ray burst",
        "expected_keywords": ["Fermi", "GBM", "trigger", "burst"],
        "expected_event_prefix": "GRB",
        "difficulty": "easy"
    },
    {
        "query": "IceCube high energy neutrino detection",
        "expected_keywords": ["IceCube", "neutrino", "energy"],
        "expected_event_prefix": "IceCube",
        "difficulty": "easy"
    },
    {
        "query": "optical telescope follow-up observation magnitude",
        "expected_keywords": ["optical", "magnitude", "observation"],
        "expected_event_prefix": None,
        "difficulty": "medium"
    },
    {
        "query": "Swift XRT X-ray afterglow position",
        "expected_keywords": ["Swift", "XRT", "X-ray", "afterglow"],
        "expected_event_prefix": "GRB",
        "difficulty": "medium"
    },
    {
        "query": "gravitational wave binary neutron star",
        "expected_keywords": ["gravitational", "wave", "neutron"],
        "expected_event_prefix": "S",
        "difficulty": "hard"
    },
    {
        "query": "radio observation interferometry",
        "expected_keywords": ["radio", "observation"],
        "expected_event_prefix": None,
        "difficulty": "hard"
    },
    {
        "query": "redshift spectroscopic measurement host galaxy",
        "expected_keywords": ["redshift", "spectroscopic", "galaxy"],
        "expected_event_prefix": None,
        "difficulty": "hard"
    },
    {
        "query": "T90 duration short gamma-ray burst",
        "expected_keywords": ["T90", "duration", "short", "burst"],
        "expected_event_prefix": "GRB",
        "difficulty": "medium"
    }
]

print(f"📋 Benchmark Dataset: {len(BENCHMARK_DATASET)} queries")
for item in BENCHMARK_DATASET:
    print(f"   [{item['difficulty']}] {item['query'][:50]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Métricas de Retrieval

# COMMAND ----------

# DBTITLE 1,Definir métricas
@dataclass
class RetrievalMetrics:
    query: str
    k: int
    num_results: int
    keyword_precision: float  # % de keywords encontradas
    event_prefix_match: float  # % de resultados com prefix correto
    mrr: float  # Mean Reciprocal Rank
    latency_ms: float


def calculate_keyword_precision(results: list, expected_keywords: list) -> float:
    """Calcula % de keywords esperadas encontradas nos resultados."""
    if not expected_keywords:
        return 1.0

    # Combinar todos os textos dos resultados
    all_text = " ".join([
        str(r.get("chunk_text", "")) + " " + str(r.get("subject", ""))
        for r in results
    ]).lower()

    found = sum(1 for kw in expected_keywords if kw.lower() in all_text)
    return found / len(expected_keywords)


def calculate_event_prefix_match(results: list, expected_prefix: str) -> float:
    """Calcula % de resultados com prefix de evento correto."""
    if not expected_prefix:
        return 1.0

    if not results:
        return 0.0

    matches = sum(1 for r in results if str(r.get("event_id", "")).startswith(expected_prefix))
    return matches / len(results)


def calculate_mrr(results: list, expected_keywords: list) -> float:
    """
    Calcula Mean Reciprocal Rank.
    MRR = 1/rank do primeiro resultado relevante.
    """
    if not expected_keywords:
        return 1.0

    for i, r in enumerate(results, 1):
        text = (str(r.get("chunk_text", "")) + " " + str(r.get("subject", ""))).lower()
        # Considera relevante se contém pelo menos metade das keywords
        matches = sum(1 for kw in expected_keywords if kw.lower() in text)
        if matches >= len(expected_keywords) / 2:
            return 1.0 / i

    return 0.0  # Nenhum resultado relevante

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Executar Benchmark

# COMMAND ----------

# DBTITLE 1,Função de benchmark
def run_retrieval_benchmark(
    benchmark_data: list,
    k: int = 5,
    filter_dict: dict = None
) -> List[RetrievalMetrics]:
    """
    Executa benchmark de retrieval.

    Args:
        benchmark_data: Lista de queries com expected values
        k: Número de resultados
        filter_dict: Filtros opcionais

    Returns:
        Lista de métricas por query
    """
    index = vsc.get_index(VS_ENDPOINT, VS_INDEX)
    results = []

    for item in benchmark_data:
        query = item["query"]
        expected_keywords = item["expected_keywords"]
        expected_prefix = item.get("expected_event_prefix")

        # Executar busca
        start_time = time.time()
        try:
            search_results = index.similarity_search(
                query_text=query,
                columns=["chunk_id", "event_id", "subject", "chunk_text"],
                num_results=k,
                filters=filter_dict
            )
            latency = (time.time() - start_time) * 1000

            data_array = search_results.get("result", {}).get("data_array", [])

            # Converter para dicts
            columns = ["chunk_id", "event_id", "subject", "chunk_text"]
            result_dicts = [
                {col: row[i] for i, col in enumerate(columns)}
                for row in data_array
            ]

        except Exception as e:
            print(f"Error for query '{query[:30]}...': {e}")
            result_dicts = []
            latency = 0

        # Calcular métricas
        metrics = RetrievalMetrics(
            query=query,
            k=k,
            num_results=len(result_dicts),
            keyword_precision=calculate_keyword_precision(result_dicts, expected_keywords),
            event_prefix_match=calculate_event_prefix_match(result_dicts, expected_prefix),
            mrr=calculate_mrr(result_dicts, expected_keywords),
            latency_ms=round(latency, 2)
        )

        results.append(metrics)

    return results


# Executar benchmark
print("🔄 Executando benchmark...")
print("-" * 60)

benchmark_results = run_retrieval_benchmark(BENCHMARK_DATASET, k=5)

# COMMAND ----------

# DBTITLE 1,Analisar resultados
import pandas as pd

# Converter para DataFrame
results_df = pd.DataFrame([{
    "query": m.query[:40] + "...",
    "k": m.k,
    "results": m.num_results,
    "keyword_precision": m.keyword_precision,
    "prefix_match": m.event_prefix_match,
    "mrr": m.mrr,
    "latency_ms": m.latency_ms
} for m in benchmark_results])

print("📊 Resultados do Benchmark:")
print(results_df.to_string(index=False))

# Métricas agregadas
print(f"""

═══════════════════════════════════════════════════════════════
                    BENCHMARK SUMMARY (K=5)
═══════════════════════════════════════════════════════════════

   Queries:             {len(benchmark_results)}
   Avg Results:         {results_df['results'].mean():.1f}

   Keyword Precision:   {results_df['keyword_precision'].mean():.2%}
   Event Prefix Match:  {results_df['prefix_match'].mean():.2%}
   MRR:                 {results_df['mrr'].mean():.3f}

   Avg Latency:         {results_df['latency_ms'].mean():.0f}ms
   P95 Latency:         {results_df['latency_ms'].quantile(0.95):.0f}ms

═══════════════════════════════════════════════════════════════
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Comparar Diferentes Valores de K

# COMMAND ----------

# DBTITLE 1,Benchmark por K
k_comparison = {}

for k in [3, 5, 7, 10]:
    results = run_retrieval_benchmark(BENCHMARK_DATASET, k=k)

    k_comparison[k] = {
        "k": k,
        "avg_keyword_precision": sum(m.keyword_precision for m in results) / len(results),
        "avg_mrr": sum(m.mrr for m in results) / len(results),
        "avg_latency_ms": sum(m.latency_ms for m in results) / len(results)
    }

print("📊 Comparação por K:")
print("-" * 60)
print(f"{'K':>5} | {'Precision':>10} | {'MRR':>8} | {'Latency':>10}")
print("-" * 60)

for k, metrics in k_comparison.items():
    print(f"{k:>5} | {metrics['avg_keyword_precision']:>10.2%} | {metrics['avg_mrr']:>8.3f} | {metrics['avg_latency_ms']:>8.0f}ms")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Salvar Resultados do Benchmark

# COMMAND ----------

# DBTITLE 1,Salvar em tabela
# Resultados detalhados
results_spark = spark.createDataFrame([{
    "query": m.query,
    "k": m.k,
    "num_results": m.num_results,
    "keyword_precision": m.keyword_precision,
    "event_prefix_match": m.event_prefix_match,
    "mrr": m.mrr,
    "latency_ms": m.latency_ms,
    "benchmark_date": time.strftime("%Y-%m-%d %H:%M:%S")
} for m in benchmark_results])

results_spark.write.mode("append").saveAsTable("retrieval_benchmark_results")

# Resumo por K
k_comparison_spark = spark.createDataFrame([
    {**metrics, "benchmark_date": time.strftime("%Y-%m-%d %H:%M:%S")}
    for metrics in k_comparison.values()
])

k_comparison_spark.write.mode("append").saveAsTable("retrieval_k_comparison")

print("✅ Resultados salvos:")
print("   - retrieval_benchmark_results")
print("   - retrieval_k_comparison")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Recomendações Baseadas no Benchmark

# COMMAND ----------

# DBTITLE 1,Análise e recomendações
# Encontrar melhor K
best_k = max(k_comparison.items(), key=lambda x: x[1]['avg_mrr'])[0]

print(f"""
╔══════════════════════════════════════════════════════════════╗
║          Retrieval Optimization Recommendations              ║
╠══════════════════════════════════════════════════════════════╣

📊 Baseado no Benchmark:

   Melhor K por MRR: {best_k}
   - MRR: {k_comparison[best_k]['avg_mrr']:.3f}
   - Precision: {k_comparison[best_k]['avg_keyword_precision']:.2%}
   - Latency: {k_comparison[best_k]['avg_latency_ms']:.0f}ms

📋 Recomendações:

   1. USE K={best_k} para balance qualidade/performance

   2. Para queries sobre GRBs:
      - Adicionar filtro: {{"event_id LIKE": "GRB%"}}
      - Melhora precision para eventos específicos

   3. Para queries ambíguas:
      - Aumentar K para 7-10
      - Usar reranking no pós-processamento

   4. Para latência crítica:
      - Reduzir K para 3
      - Aceitar trade-off em recall

   5. Monitorar métricas em produção:
      - Keyword precision > 70%
      - MRR > 0.5
      - P95 latency < 500ms

╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Métricas de Retrieval:
# MAGIC
# MAGIC | Métrica | Valor (K=5) | Target |
# MAGIC |---------|-------------|--------|
# MAGIC | Keyword Precision | {:.2%} | >70% |
# MAGIC | MRR | {:.3f} | >0.5 |
# MAGIC | Avg Latency | {:.0f}ms | <500ms |
# MAGIC
# MAGIC ### Tabelas Criadas:
# MAGIC
# MAGIC | Tabela | Descrição |
# MAGIC |--------|-----------|
# MAGIC | `retrieval_benchmark_results` | Resultados detalhados |
# MAGIC | `retrieval_k_comparison` | Comparação por K |
""".format(
    results_df['keyword_precision'].mean(),
    results_df['mrr'].mean(),
    results_df['latency_ms'].mean()
)
