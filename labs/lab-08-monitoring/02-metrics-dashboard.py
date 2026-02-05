# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 8.2: Metrics Dashboard for RAG Monitoring
# MAGIC
# MAGIC Este notebook cria queries e visualizações para monitoramento do RAG.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Definir métricas chave para RAG
# MAGIC 2. Criar queries de monitoramento
# MAGIC 3. Implementar KPIs e SLOs
# MAGIC 4. Gerar relatórios automatizados
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 4: Evaluation and Monitoring (18%)
# MAGIC - Define monitoring metrics for GenAI applications
# MAGIC - Create dashboards for model performance

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql.functions import *
from datetime import datetime, timedelta
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Definir Métricas Chave (KPIs)

# COMMAND ----------

# DBTITLE 1,KPIs para RAG
KPIS = {
    "availability": {
        "name": "Service Availability",
        "description": "% de requests com sucesso",
        "target": 99.5,
        "unit": "%",
        "formula": "successful_requests / total_requests * 100"
    },
    "latency_p95": {
        "name": "P95 Latency",
        "description": "Latência no percentil 95",
        "target": 5000,
        "unit": "ms",
        "formula": "percentile(execution_time_ms, 0.95)"
    },
    "error_rate": {
        "name": "Error Rate",
        "description": "% de requests com erro",
        "target": 0.5,
        "unit": "%",
        "formula": "failed_requests / total_requests * 100"
    },
    "throughput": {
        "name": "Throughput",
        "description": "Requests por minuto",
        "target": 100,
        "unit": "rpm",
        "formula": "count(*) / period_minutes"
    },
    "retrieval_quality": {
        "name": "Retrieval Quality",
        "description": "Média de documentos recuperados",
        "target": 5,
        "unit": "docs",
        "formula": "avg(num_docs)"
    }
}

print("📊 KPIs Definidos:")
for kpi_id, kpi in KPIS.items():
    print(f"\n  {kpi['name']} ({kpi_id})")
    print(f"    Target: {kpi['target']} {kpi['unit']}")
    print(f"    Formula: {kpi['formula']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Queries de Monitoramento

# COMMAND ----------

# DBTITLE 1,Query: Resumo Geral (última hora)
# Resumo da última hora
query_summary = """
SELECT
    COUNT(*) as total_requests,
    SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) as failed,
    ROUND(SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate,
    ROUND(AVG(execution_time_ms), 0) as avg_latency_ms,
    ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency_ms
FROM inference_logs_sample
WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR
"""

print("📊 Query: Resumo Última Hora")
spark.sql(query_summary).show()

# COMMAND ----------

# DBTITLE 1,Query: Trend de latência (últimos 7 dias)
query_latency_trend = """
SELECT
    DATE(timestamp) as date,
    model_version,
    COUNT(*) as requests,
    ROUND(AVG(execution_time_ms), 0) as avg_latency,
    ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency
FROM inference_logs_sample
WHERE timestamp >= current_timestamp() - INTERVAL 7 DAY
GROUP BY DATE(timestamp), model_version
ORDER BY date, model_version
"""

print("📊 Query: Trend de Latência (7 dias)")
spark.sql(query_latency_trend).show(20)

# COMMAND ----------

# DBTITLE 1,Query: Error breakdown
query_errors = """
SELECT
    status_code,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM inference_logs_sample
WHERE status_code != 200
GROUP BY status_code
ORDER BY count DESC
"""

print("📊 Query: Breakdown de Erros")
spark.sql(query_errors).show()

# COMMAND ----------

# DBTITLE 1,Query: Top slow requests
query_slow_requests = """
SELECT
    request_id,
    timestamp,
    model_version,
    execution_time_ms,
    status_code
FROM inference_logs_sample
WHERE execution_time_ms > 5000  -- SLO threshold
ORDER BY execution_time_ms DESC
LIMIT 20
"""

print("📊 Query: Requests Lentas (>5s)")
spark.sql(query_slow_requests).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Service Level Objectives (SLOs)

# COMMAND ----------

# DBTITLE 1,Definir SLOs
SLOS = {
    "availability": {
        "name": "Availability SLO",
        "target": 99.5,
        "window": "1 day",
        "query": """
            SELECT
                DATE(timestamp) as date,
                ROUND(SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as availability
            FROM inference_logs_sample
            GROUP BY DATE(timestamp)
        """
    },
    "latency": {
        "name": "Latency SLO",
        "target": 5000,  # ms
        "window": "1 hour",
        "query": """
            SELECT
                DATE_TRUNC('hour', timestamp) as hour,
                ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency
            FROM inference_logs_sample
            GROUP BY DATE_TRUNC('hour', timestamp)
        """
    },
    "error_budget": {
        "name": "Error Budget SLO",
        "target": 0.5,  # % máximo de erros
        "window": "1 month",
        "query": """
            SELECT
                ROUND(SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as error_rate
            FROM inference_logs_sample
        """
    }
}

print("📋 SLOs Definidos:")
for slo_id, slo in SLOS.items():
    print(f"\n  {slo['name']}")
    print(f"    Target: {slo['target']}")
    print(f"    Window: {slo['window']}")

# COMMAND ----------

# DBTITLE 1,Verificar cumprimento de SLOs
def check_slo_compliance(slo_name: str, slo_config: dict) -> dict:
    """Verifica cumprimento de SLO."""
    df = spark.sql(slo_config["query"])
    results = df.collect()

    if not results:
        return {"status": "unknown", "message": "No data"}

    # Calcular compliance
    if slo_name == "availability":
        values = [r.availability for r in results]
        current = sum(values) / len(values)
        compliant = current >= slo_config["target"]
    elif slo_name == "latency":
        values = [r.p95_latency for r in results]
        current = max(values) if values else 0
        compliant = current <= slo_config["target"]
    elif slo_name == "error_budget":
        current = results[0].error_rate if results else 0
        compliant = current <= slo_config["target"]
    else:
        return {"status": "unknown", "message": "Unknown SLO type"}

    return {
        "slo": slo_config["name"],
        "target": slo_config["target"],
        "current": round(current, 2),
        "compliant": compliant,
        "status": "✅ OK" if compliant else "❌ VIOLATION"
    }


print("📊 SLO Compliance Check:")
print("=" * 60)

for slo_id, slo_config in SLOS.items():
    result = check_slo_compliance(slo_id, slo_config)
    print(f"\n{result['status']} {result['slo']}")
    print(f"   Target: {result['target']}")
    print(f"   Current: {result['current']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Dashboard Data

# COMMAND ----------

# DBTITLE 1,Criar view para dashboard
# View consolidada para dashboard
spark.sql("""
CREATE OR REPLACE VIEW v_rag_monitoring_dashboard AS
SELECT
    DATE(timestamp) as date,
    HOUR(timestamp) as hour,
    model_version,
    COUNT(*) as total_requests,
    SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful_requests,
    SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) as failed_requests,
    ROUND(SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate,
    ROUND(AVG(execution_time_ms), 0) as avg_latency_ms,
    ROUND(PERCENTILE(execution_time_ms, 0.5), 0) as p50_latency_ms,
    ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency_ms,
    ROUND(PERCENTILE(execution_time_ms, 0.99), 0) as p99_latency_ms,
    MIN(execution_time_ms) as min_latency_ms,
    MAX(execution_time_ms) as max_latency_ms
FROM inference_logs_sample
GROUP BY DATE(timestamp), HOUR(timestamp), model_version
""")

print("✅ View criada: v_rag_monitoring_dashboard")

# Mostrar dados
spark.sql("SELECT * FROM v_rag_monitoring_dashboard ORDER BY date DESC, hour DESC LIMIT 10").show()

# COMMAND ----------

# DBTITLE 1,Métricas em tempo real (última hora)
# Métricas para widget de dashboard
realtime_metrics = spark.sql("""
SELECT
    'Last Hour' as period,
    COUNT(*) as requests,
    ROUND(SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as availability,
    ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency,
    SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) as errors
FROM inference_logs_sample
WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR
""").collect()[0]

print(f"""
╔══════════════════════════════════════════════════════════════╗
║              Real-time Dashboard - Last Hour                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║    📈 Requests:      {realtime_metrics.requests:>10,}                          ║
║    ✅ Availability:   {realtime_metrics.availability:>10.2f}%                        ║
║    ⏱️  P95 Latency:   {realtime_metrics.p95_latency:>10,.0f}ms                       ║
║    ❌ Errors:        {realtime_metrics.errors:>10,}                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Relatório Automatizado

# COMMAND ----------

# DBTITLE 1,Gerar relatório diário
def generate_daily_report(date: str = None) -> str:
    """Gera relatório diário de monitoramento."""

    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Métricas do dia
    metrics = spark.sql(f"""
        SELECT
            COUNT(*) as total_requests,
            SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful,
            SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) as failed,
            ROUND(AVG(execution_time_ms), 0) as avg_latency,
            ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency
        FROM inference_logs_sample
        WHERE DATE(timestamp) = '{date}'
    """).collect()[0]

    # Por versão
    by_version = spark.sql(f"""
        SELECT
            model_version,
            COUNT(*) as requests,
            ROUND(AVG(execution_time_ms), 0) as avg_latency
        FROM inference_logs_sample
        WHERE DATE(timestamp) = '{date}'
        GROUP BY model_version
    """).collect()

    report = f"""
================================================================================
                    NASA GCN RAG - Daily Monitoring Report
                              Date: {date}
================================================================================

SUMMARY
-------
Total Requests:     {metrics.total_requests:,}
Successful:         {metrics.successful:,}
Failed:             {metrics.failed:,}
Availability:       {metrics.successful/metrics.total_requests*100:.2f}%

LATENCY
-------
Average:            {metrics.avg_latency:,.0f}ms
P95:                {metrics.p95_latency:,.0f}ms

BY MODEL VERSION
----------------
"""
    for v in by_version:
        report += f"  v{v.model_version}: {v.requests:,} requests, {v.avg_latency:,.0f}ms avg latency\n"

    report += """
SLO STATUS
----------
"""
    for slo_id, slo_config in SLOS.items():
        result = check_slo_compliance(slo_id, slo_config)
        report += f"  {result['status']} {result['slo']}: {result['current']} (target: {result['target']})\n"

    report += """
================================================================================
                        End of Report
================================================================================
"""
    return report


# Gerar relatório
report = generate_daily_report()
print(report)

# COMMAND ----------

# DBTITLE 1,Salvar relatório
# Salvar relatório em tabela
report_data = [{
    "report_date": datetime.now().strftime("%Y-%m-%d"),
    "report_type": "daily",
    "report_content": report,
    "generated_at": datetime.now().isoformat()
}]

spark.createDataFrame(report_data).write.mode("append").saveAsTable("monitoring_reports")

print("✅ Relatório salvo em 'monitoring_reports'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### KPIs Definidos:
# MAGIC
# MAGIC | KPI | Target | Descrição |
# MAGIC |-----|--------|-----------|
# MAGIC | Availability | 99.5% | % requests com sucesso |
# MAGIC | P95 Latency | 5000ms | Latência no P95 |
# MAGIC | Error Rate | <0.5% | % requests com erro |
# MAGIC
# MAGIC ### Views Criadas:
# MAGIC
# MAGIC | View | Descrição |
# MAGIC |------|-----------|
# MAGIC | `v_rag_monitoring_dashboard` | Dados agregados para dashboard |
# MAGIC
# MAGIC ### Próximo Notebook: 03-alerting.py
