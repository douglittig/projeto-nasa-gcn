# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 8.3: Alerting and Anomaly Detection
# MAGIC
# MAGIC Este notebook implementa alertas e detecção de anomalias para o sistema RAG.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Definir regras de alerta
# MAGIC 2. Implementar detecção de anomalias
# MAGIC 3. Configurar notificações
# MAGIC 4. Criar runbook de resposta
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 4: Evaluation and Monitoring (18%)
# MAGIC - Configure alerts for model degradation
# MAGIC - Implement anomaly detection

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql.functions import *
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Definir Regras de Alerta

# COMMAND ----------

# DBTITLE 1,Classes de alerta
class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AlertRule:
    name: str
    description: str
    severity: AlertSeverity
    condition: str  # SQL condition
    threshold: float
    window_minutes: int
    cooldown_minutes: int = 30


# Definir regras
ALERT_RULES = [
    AlertRule(
        name="high_error_rate",
        description="Taxa de erros acima do limite",
        severity=AlertSeverity.ERROR,
        condition="error_rate > {threshold}",
        threshold=5.0,  # 5%
        window_minutes=15
    ),
    AlertRule(
        name="high_latency_p95",
        description="Latência P95 acima do SLO",
        severity=AlertSeverity.WARNING,
        condition="p95_latency > {threshold}",
        threshold=5000,  # ms
        window_minutes=15
    ),
    AlertRule(
        name="availability_drop",
        description="Disponibilidade abaixo do SLO",
        severity=AlertSeverity.CRITICAL,
        condition="availability < {threshold}",
        threshold=99.0,  # %
        window_minutes=60
    ),
    AlertRule(
        name="latency_spike",
        description="Pico de latência detectado",
        severity=AlertSeverity.WARNING,
        condition="p99_latency > {threshold}",
        threshold=10000,  # ms
        window_minutes=5
    ),
    AlertRule(
        name="no_requests",
        description="Sem requests no período",
        severity=AlertSeverity.ERROR,
        condition="total_requests < {threshold}",
        threshold=1,
        window_minutes=30
    )
]

print("📋 Regras de Alerta Definidas:")
for rule in ALERT_RULES:
    print(f"\n  [{rule.severity.value.upper()}] {rule.name}")
    print(f"    {rule.description}")
    print(f"    Threshold: {rule.threshold}")
    print(f"    Window: {rule.window_minutes}min")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Implementar Avaliação de Alertas

# COMMAND ----------

# DBTITLE 1,Função de avaliação
@dataclass
class Alert:
    rule_name: str
    severity: AlertSeverity
    message: str
    current_value: float
    threshold: float
    timestamp: str
    status: str  # "firing", "resolved"


def evaluate_alert_rules(window_minutes: int = 15) -> List[Alert]:
    """
    Avalia todas as regras de alerta.

    Args:
        window_minutes: Janela de tempo para análise

    Returns:
        Lista de alertas disparados
    """
    alerts = []

    # Calcular métricas para a janela
    metrics = spark.sql(f"""
        SELECT
            COUNT(*) as total_requests,
            SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful,
            SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) as failed,
            ROUND(SUM(CASE WHEN status_code != 200 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) as error_rate,
            ROUND(SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) as availability,
            ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency,
            ROUND(PERCENTILE(execution_time_ms, 0.99), 0) as p99_latency
        FROM inference_logs_sample
        WHERE timestamp >= current_timestamp() - INTERVAL {window_minutes} MINUTE
    """).collect()[0]

    timestamp = datetime.now().isoformat()

    for rule in ALERT_RULES:
        current_value = None
        triggered = False

        # Avaliar condição
        if rule.name == "high_error_rate":
            current_value = metrics.error_rate or 0
            triggered = current_value > rule.threshold

        elif rule.name == "high_latency_p95":
            current_value = metrics.p95_latency or 0
            triggered = current_value > rule.threshold

        elif rule.name == "availability_drop":
            current_value = metrics.availability or 100
            triggered = current_value < rule.threshold

        elif rule.name == "latency_spike":
            current_value = metrics.p99_latency or 0
            triggered = current_value > rule.threshold

        elif rule.name == "no_requests":
            current_value = metrics.total_requests or 0
            triggered = current_value < rule.threshold

        if triggered:
            alerts.append(Alert(
                rule_name=rule.name,
                severity=rule.severity,
                message=f"{rule.description}: {current_value} (threshold: {rule.threshold})",
                current_value=current_value,
                threshold=rule.threshold,
                timestamp=timestamp,
                status="firing"
            ))

    return alerts


# Avaliar alertas
current_alerts = evaluate_alert_rules(window_minutes=60)

print(f"🚨 Alertas Ativos: {len(current_alerts)}")
for alert in current_alerts:
    icon = {"critical": "🔴", "error": "🟠", "warning": "🟡", "info": "🔵"}
    print(f"\n  {icon.get(alert.severity.value, '⚪')} [{alert.severity.value.upper()}] {alert.rule_name}")
    print(f"    {alert.message}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Detecção de Anomalias

# COMMAND ----------

# DBTITLE 1,Anomaly detection com Z-score
def detect_latency_anomalies(lookback_hours: int = 24, z_threshold: float = 3.0) -> List[Dict]:
    """
    Detecta anomalias de latência usando Z-score.

    Args:
        lookback_hours: Horas para calcular baseline
        z_threshold: Threshold do Z-score para anomalia

    Returns:
        Lista de anomalias detectadas
    """
    # Calcular baseline (média e desvio padrão)
    baseline = spark.sql(f"""
        SELECT
            AVG(execution_time_ms) as mean_latency,
            STDDEV(execution_time_ms) as std_latency
        FROM inference_logs_sample
        WHERE timestamp >= current_timestamp() - INTERVAL {lookback_hours} HOUR
          AND status_code = 200
    """).collect()[0]

    mean = baseline.mean_latency or 0
    std = baseline.std_latency or 1

    # Encontrar anomalias recentes
    anomalies = spark.sql(f"""
        SELECT
            request_id,
            timestamp,
            execution_time_ms,
            ({baseline.mean_latency} - execution_time_ms) / {std} as z_score
        FROM inference_logs_sample
        WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR
          AND ABS(({mean} - execution_time_ms) / {std}) > {z_threshold}
        ORDER BY execution_time_ms DESC
        LIMIT 20
    """).collect()

    return [{
        "request_id": a.request_id,
        "timestamp": str(a.timestamp),
        "latency_ms": a.execution_time_ms,
        "z_score": round(abs(a.z_score), 2)
    } for a in anomalies]


# Detectar anomalias
anomalies = detect_latency_anomalies(lookback_hours=24, z_threshold=2.5)

print(f"🔍 Anomalias de Latência Detectadas: {len(anomalies)}")
for a in anomalies[:5]:
    print(f"   {a['request_id']}: {a['latency_ms']:.0f}ms (z-score: {a['z_score']})")

# COMMAND ----------

# DBTITLE 1,Detectar mudança de padrão (trend)
def detect_trend_change(metric: str = "p95_latency", window_hours: int = 6) -> Dict:
    """
    Detecta mudança significativa de tendência.

    Args:
        metric: Métrica para analisar
        window_hours: Janela de comparação

    Returns:
        Dict com análise de tendência
    """
    # Comparar período atual com período anterior
    comparison = spark.sql(f"""
        WITH current_period AS (
            SELECT
                ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency,
                COUNT(*) as requests
            FROM inference_logs_sample
            WHERE timestamp >= current_timestamp() - INTERVAL {window_hours} HOUR
        ),
        previous_period AS (
            SELECT
                ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency,
                COUNT(*) as requests
            FROM inference_logs_sample
            WHERE timestamp >= current_timestamp() - INTERVAL {window_hours * 2} HOUR
              AND timestamp < current_timestamp() - INTERVAL {window_hours} HOUR
        )
        SELECT
            c.p95_latency as current_value,
            p.p95_latency as previous_value,
            ROUND((c.p95_latency - p.p95_latency) * 100.0 / NULLIF(p.p95_latency, 0), 2) as change_percent
        FROM current_period c, previous_period p
    """).collect()[0]

    change = comparison.change_percent or 0
    status = "stable"
    if change > 20:
        status = "degrading"
    elif change < -20:
        status = "improving"

    return {
        "metric": metric,
        "current_value": comparison.current_value,
        "previous_value": comparison.previous_value,
        "change_percent": change,
        "status": status,
        "alert": abs(change) > 30
    }


# Detectar mudança de tendência
trend = detect_trend_change("p95_latency", window_hours=6)

print(f"""
📈 Análise de Tendência (P95 Latency):
   Período anterior: {trend['previous_value']}ms
   Período atual:    {trend['current_value']}ms
   Mudança:          {trend['change_percent']:+.1f}%
   Status:           {trend['status'].upper()}
   Alerta:           {'🚨 SIM' if trend['alert'] else '✅ NÃO'}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Salvar Alertas e Histórico

# COMMAND ----------

# DBTITLE 1,Salvar alertas em tabela
# Converter alertas para DataFrame
alert_records = [{
    "alert_id": f"alert_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}",
    "rule_name": a.rule_name,
    "severity": a.severity.value,
    "message": a.message,
    "current_value": a.current_value,
    "threshold": a.threshold,
    "timestamp": a.timestamp,
    "status": a.status
} for i, a in enumerate(current_alerts)]

if alert_records:
    spark.createDataFrame(alert_records).write.mode("append").saveAsTable("alert_history")
    print(f"✅ {len(alert_records)} alertas salvos em 'alert_history'")
else:
    print("✅ Nenhum alerta ativo no momento")

# COMMAND ----------

# DBTITLE 1,Ver histórico de alertas
spark.sql("""
    SELECT
        timestamp,
        rule_name,
        severity,
        message,
        status
    FROM alert_history
    ORDER BY timestamp DESC
    LIMIT 20
""").show(truncate=60)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Runbook de Resposta

# COMMAND ----------

# DBTITLE 1,Runbook de resposta a alertas
RUNBOOK = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RUNBOOK - NASA GCN RAG Alert Response                     ║
╠══════════════════════════════════════════════════════════════════════════════╣

🔴 CRITICAL: availability_drop
   Sintoma: Disponibilidade abaixo de 99%
   Impacto: Usuários não conseguem fazer queries
   Ações:
     1. Verificar status do endpoint: w.serving_endpoints.get("nasa-gcn-rag-assistant")
     2. Verificar logs do endpoint no UI
     3. Verificar status do Vector Search index
     4. Se necessário, reiniciar endpoint
     5. Escalar para on-call se não resolver em 15min

🟠 ERROR: high_error_rate
   Sintoma: Taxa de erros > 5%
   Impacto: Algumas queries falhando
   Ações:
     1. Identificar padrão de erros: SELECT status_code, COUNT(*) FROM logs GROUP BY status_code
     2. Verificar se há timeout (408) ou erro interno (500)
     3. Para timeouts: verificar latência do Vector Search
     4. Para erros internos: verificar logs do modelo
     5. Considerar rollback se versão nova

🟠 ERROR: no_requests
   Sintoma: Sem requests por 30min
   Impacto: Possível problema de conectividade ou deploy
   Ações:
     1. Verificar se endpoint está READY
     2. Verificar se há problemas de rede
     3. Fazer request de teste manual
     4. Verificar se houve deploy recente

🟡 WARNING: high_latency_p95
   Sintoma: P95 latência > 5000ms
   Impacto: Experiência degradada para usuários
   Ações:
     1. Verificar volume de requests (possível overload)
     2. Verificar latência do Vector Search
     3. Verificar se há queries específicas lentas
     4. Considerar aumentar capacidade se persistir

🟡 WARNING: latency_spike
   Sintoma: Pico de latência P99 > 10s
   Impacto: Algumas requests muito lentas
   Ações:
     1. Identificar requests afetadas
     2. Verificar se padrão de query específico
     3. Pode ser cold start - aguardar normalização
     4. Monitorar por 15min antes de escalar

═══════════════════════════════════════════════════════════════════════════════

CONTATOS:
  - On-call: #nasa-gcn-oncall (Slack)
  - Escalonamento: mlops-team@example.com
  - Documentação: /docs/nasa-gcn-troubleshooting.md

════════════════════════════════════════════════════════════════════════════════
"""

print(RUNBOOK)

# Salvar runbook
spark.createDataFrame([{
    "document": "runbook",
    "content": RUNBOOK,
    "updated_at": datetime.now().isoformat()
}]).write.mode("overwrite").saveAsTable("monitoring_runbook")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Regras de Alerta Configuradas:
# MAGIC
# MAGIC | Alerta | Severidade | Threshold |
# MAGIC |--------|------------|-----------|
# MAGIC | availability_drop | CRITICAL | <99% |
# MAGIC | high_error_rate | ERROR | >5% |
# MAGIC | no_requests | ERROR | <1 em 30min |
# MAGIC | high_latency_p95 | WARNING | >5000ms |
# MAGIC | latency_spike | WARNING | >10000ms |
# MAGIC
# MAGIC ### Tabelas Criadas:
# MAGIC
# MAGIC | Tabela | Descrição |
# MAGIC |--------|-----------|
# MAGIC | `alert_history` | Histórico de alertas |
# MAGIC | `monitoring_runbook` | Procedimentos de resposta |
