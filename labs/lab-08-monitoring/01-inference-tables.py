# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 8.1: Inference Tables for LLM Monitoring
# MAGIC
# MAGIC Este notebook configura e analisa inference tables para monitoramento de LLMs.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Entender estrutura de inference tables
# MAGIC 2. Configurar logging de inferências
# MAGIC 3. Analisar padrões de uso
# MAGIC 4. Identificar anomalias
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 4: Evaluation and Monitoring (18%)
# MAGIC - Configure inference tables for model monitoring
# MAGIC - Analyze inference patterns and anomalies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql.functions import (
    col, count, avg, min, max, sum, stddev,
    from_json, explode, to_timestamp, date_trunc,
    when, lit, expr, percentile_approx
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, IntegerType
import json
from datetime import datetime, timedelta

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Estrutura de Inference Tables

# COMMAND ----------

# DBTITLE 1,Schema de inference table
# Schema típico de inference table (Databricks Model Serving)
INFERENCE_SCHEMA = StructType([
    StructField("request_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("timestamp_ms", DoubleType(), True),
    StructField("status_code", IntegerType(), True),
    StructField("execution_time_ms", DoubleType(), True),
    StructField("request", StringType(), True),  # JSON
    StructField("response", StringType(), True),  # JSON
    StructField("served_model_name", StringType(), True),
    StructField("model_version", StringType(), True),
    StructField("client_request_id", StringType(), True),
    StructField("databricks_request_id", StringType(), True)
])

print("📋 Inference Table Schema:")
for field in INFERENCE_SCHEMA.fields:
    print(f"   {field.name}: {field.dataType.simpleString()}")

# COMMAND ----------

# DBTITLE 1,Criar dados de exemplo (simulação)
import random
from datetime import datetime, timedelta

def generate_sample_inference_data(num_records: int = 1000):
    """Gera dados de inferência de exemplo."""

    questions = [
        "What observations were made for gamma-ray bursts?",
        "What is the position of GRB 251208B?",
        "How did IceCube detect the neutrino?",
        "What optical follow-up was performed?",
        "What is the redshift of the host galaxy?",
        "What X-ray afterglow was detected?",
        "What is the T90 duration?",
        "Were there any radio observations?"
    ]

    model_versions = ["1", "2"]
    status_codes = [200, 200, 200, 200, 200, 500, 408]  # Mostly 200

    records = []
    base_time = datetime.now() - timedelta(days=7)

    for i in range(num_records):
        timestamp = base_time + timedelta(minutes=random.randint(0, 10080))  # 7 days
        question = random.choice(questions)
        version = random.choice(model_versions)
        status = random.choice(status_codes)

        # Latência varia por versão e status
        base_latency = 2000 if version == "1" else 2500
        if status != 200:
            base_latency = 30000  # Timeout

        latency = base_latency + random.randint(-500, 1000)

        records.append({
            "request_id": f"req_{i:06d}",
            "timestamp": timestamp,
            "timestamp_ms": timestamp.timestamp() * 1000,
            "status_code": status,
            "execution_time_ms": latency,
            "request": json.dumps({"dataframe_split": {"columns": ["question"], "data": [[question]]}}),
            "response": json.dumps({"predictions": [{"answer": "...", "sources": "[]", "num_docs": 5}]}) if status == 200 else json.dumps({"error": "timeout"}),
            "served_model_name": f"gcn_rag_assistant-{version}",
            "model_version": version,
            "client_request_id": f"client_{i:06d}",
            "databricks_request_id": f"dbx_{i:06d}"
        })

    return records

# Gerar dados
sample_data = generate_sample_inference_data(1000)
df_inference = spark.createDataFrame(sample_data, INFERENCE_SCHEMA)

# Salvar como tabela de exemplo
df_inference.write.mode("overwrite").saveAsTable("inference_logs_sample")

print(f"✅ Criados {len(sample_data)} registros de inferência de exemplo")
print(f"   Tabela: inference_logs_sample")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Análise de Padrões de Uso

# COMMAND ----------

# DBTITLE 1,Estatísticas gerais
df_logs = spark.table("inference_logs_sample")

# Estatísticas básicas
stats = df_logs.agg(
    count("*").alias("total_requests"),
    avg("execution_time_ms").alias("avg_latency_ms"),
    percentile_approx("execution_time_ms", 0.5).alias("p50_latency_ms"),
    percentile_approx("execution_time_ms", 0.95).alias("p95_latency_ms"),
    percentile_approx("execution_time_ms", 0.99).alias("p99_latency_ms"),
    min("timestamp").alias("first_request"),
    max("timestamp").alias("last_request")
).collect()[0]

print(f"""
╔══════════════════════════════════════════════════════════════╗
║              Inference Logs - Overview                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Total requests:      {stats.total_requests:>10,}                         ║
║  Period:              {str(stats.first_request)[:10]} to {str(stats.last_request)[:10]}         ║
║                                                              ║
║  Latency (ms):                                               ║
║    Average:           {stats.avg_latency_ms:>10,.0f}                         ║
║    P50:               {stats.p50_latency_ms:>10,.0f}                         ║
║    P95:               {stats.p95_latency_ms:>10,.0f}                         ║
║    P99:               {stats.p99_latency_ms:>10,.0f}                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# DBTITLE 1,Requests por status code
print("📊 Requests por Status Code:")
df_logs.groupBy("status_code").agg(
    count("*").alias("count"),
    avg("execution_time_ms").alias("avg_latency_ms")
).orderBy("status_code").show()

# COMMAND ----------

# DBTITLE 1,Requests por versão do modelo
print("📊 Requests por Versão do Modelo:")
df_logs.groupBy("model_version").agg(
    count("*").alias("count"),
    avg("execution_time_ms").alias("avg_latency_ms"),
    percentile_approx("execution_time_ms", 0.95).alias("p95_latency_ms")
).orderBy("model_version").show()

# COMMAND ----------

# DBTITLE 1,Requests por hora
# Agregar por hora
df_hourly = df_logs.withColumn(
    "hour", date_trunc("hour", col("timestamp"))
).groupBy("hour").agg(
    count("*").alias("requests"),
    avg("execution_time_ms").alias("avg_latency_ms"),
    sum(when(col("status_code") != 200, 1).otherwise(0)).alias("errors")
).orderBy("hour")

print("📊 Requests por Hora (últimas 24h):")
df_hourly.orderBy(col("hour").desc()).limit(24).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Extrair Detalhes das Requests

# COMMAND ----------

# DBTITLE 1,Parsear request JSON
# Schema para request
request_schema = StructType([
    StructField("dataframe_split", StructType([
        StructField("columns", StringType(), True),
        StructField("data", StringType(), True)
    ]), True)
])

# Extrair questions
df_with_questions = df_logs.withColumn(
    "request_parsed",
    from_json(col("request"), "struct<dataframe_split:struct<columns:array<string>,data:array<array<string>>>>")
).withColumn(
    "question",
    col("request_parsed.dataframe_split.data")[0][0]
)

# Top questions
print("📊 Top 10 Questions:")
df_with_questions.groupBy("question").agg(
    count("*").alias("count"),
    avg("execution_time_ms").alias("avg_latency_ms")
).orderBy(col("count").desc()).limit(10).show(truncate=50)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Detectar Anomalias

# COMMAND ----------

# DBTITLE 1,Identificar requests lentas
# Threshold: P95 + 2 * stddev
latency_stats = df_logs.agg(
    avg("execution_time_ms").alias("avg"),
    stddev("execution_time_ms").alias("std"),
    percentile_approx("execution_time_ms", 0.95).alias("p95")
).collect()[0]

threshold = latency_stats.p95 + (2 * (latency_stats.std or 0))

print(f"⚠️ Threshold para requests lentas: {threshold:,.0f}ms")

# Identificar outliers
df_slow = df_logs.filter(col("execution_time_ms") > threshold)
slow_count = df_slow.count()

print(f"   Requests lentas: {slow_count} ({slow_count/stats.total_requests*100:.2f}%)")

# Mostrar exemplos
print("\n📋 Exemplos de requests lentas:")
df_slow.select("request_id", "timestamp", "execution_time_ms", "status_code").show(5)

# COMMAND ----------

# DBTITLE 1,Detectar picos de erros
# Agrupar erros por janela de 1 hora
df_error_rate = df_logs.withColumn(
    "hour", date_trunc("hour", col("timestamp"))
).groupBy("hour").agg(
    count("*").alias("total"),
    sum(when(col("status_code") != 200, 1).otherwise(0)).alias("errors")
).withColumn(
    "error_rate", col("errors") / col("total")
)

# Identificar horas com error rate > 5%
df_high_error = df_error_rate.filter(col("error_rate") > 0.05)

print("⚠️ Períodos com alta taxa de erro (>5%):")
df_high_error.orderBy(col("error_rate").desc()).show(10)

# COMMAND ----------

# DBTITLE 1,Detectar degradação de performance
# Comparar latência entre versões
version_comparison = df_logs.groupBy("model_version").agg(
    count("*").alias("requests"),
    avg("execution_time_ms").alias("avg_latency"),
    percentile_approx("execution_time_ms", 0.95).alias("p95_latency")
).collect()

if len(version_comparison) >= 2:
    v1 = next((v for v in version_comparison if v.model_version == "1"), None)
    v2 = next((v for v in version_comparison if v.model_version == "2"), None)

    if v1 and v2:
        latency_diff = ((v2.avg_latency - v1.avg_latency) / v1.avg_latency) * 100
        print(f"""
📊 Comparação de Performance entre Versões:

   Version 1:
     - Requests: {v1.requests:,}
     - Avg Latency: {v1.avg_latency:,.0f}ms
     - P95 Latency: {v1.p95_latency:,.0f}ms

   Version 2:
     - Requests: {v2.requests:,}
     - Avg Latency: {v2.avg_latency:,.0f}ms
     - P95 Latency: {v2.p95_latency:,.0f}ms

   Diferença: {latency_diff:+.1f}% {'⚠️ Regressão' if latency_diff > 10 else '✅ OK'}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Salvar Métricas Agregadas

# COMMAND ----------

# DBTITLE 1,Criar tabela de métricas diárias
# Agregar por dia
df_daily_metrics = df_logs.withColumn(
    "date", date_trunc("day", col("timestamp"))
).groupBy("date", "model_version").agg(
    count("*").alias("total_requests"),
    sum(when(col("status_code") == 200, 1).otherwise(0)).alias("successful_requests"),
    sum(when(col("status_code") != 200, 1).otherwise(0)).alias("failed_requests"),
    avg("execution_time_ms").alias("avg_latency_ms"),
    percentile_approx("execution_time_ms", 0.5).alias("p50_latency_ms"),
    percentile_approx("execution_time_ms", 0.95).alias("p95_latency_ms"),
    percentile_approx("execution_time_ms", 0.99).alias("p99_latency_ms"),
    min("execution_time_ms").alias("min_latency_ms"),
    max("execution_time_ms").alias("max_latency_ms")
).withColumn(
    "success_rate", col("successful_requests") / col("total_requests")
)

# Salvar
df_daily_metrics.write.mode("overwrite").saveAsTable("inference_daily_metrics")

print("✅ Métricas diárias salvas em 'inference_daily_metrics'")
df_daily_metrics.orderBy("date", "model_version").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Métricas Coletadas:
# MAGIC
# MAGIC | Métrica | Descrição |
# MAGIC |---------|-----------|
# MAGIC | Total Requests | Número total de inferências |
# MAGIC | Success Rate | % de requests com status 200 |
# MAGIC | Latency (P50/P95/P99) | Percentis de tempo de resposta |
# MAGIC | Error Rate | % de requests com erro |
# MAGIC
# MAGIC ### Tabelas Criadas:
# MAGIC
# MAGIC | Tabela | Descrição |
# MAGIC |--------|-----------|
# MAGIC | `inference_logs_sample` | Logs de inferência simulados |
# MAGIC | `inference_daily_metrics` | Métricas agregadas por dia |
# MAGIC
# MAGIC ### Próximo Notebook: 02-metrics-dashboard.py
