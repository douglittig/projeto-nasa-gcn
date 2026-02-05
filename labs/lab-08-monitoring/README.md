# Lab 8: LLM Evaluation & Monitoring

Este lab implementa monitoramento completo para aplicações GenAI, incluindo inference tables, métricas e alertas.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Configurar inference tables** para captura de logs
2. **Definir KPIs e SLOs** para RAG
3. **Criar dashboards** de monitoramento
4. **Implementar alertas** e detecção de anomalias

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 4: Evaluation and Monitoring** | 18% | Inference tables, metrics, alerting, anomaly detection |

## Pré-requisitos

- Endpoint RAG deployado (Lab 5)
- Tabelas de configuração dos labs anteriores

## Estrutura do Lab

```
lab-08-monitoring/
├── 01-inference-tables.py       # Configuração e análise de logs
├── 02-metrics-dashboard.py      # KPIs, SLOs, e dashboard
├── 03-alerting.py               # Alertas e anomaly detection
└── README.md                    # Este arquivo
```

## Notebooks

### 1. Inference Tables (`01-inference-tables.py`)

**O que você vai aprender:**
- Estrutura de inference tables do Model Serving
- Análise de padrões de uso
- Identificar requests lentas
- Detectar picos de erros

**Schema de inference table:**
```
request_id: string
timestamp: timestamp
status_code: int
execution_time_ms: double
request: string (JSON)
response: string (JSON)
served_model_name: string
model_version: string
```

### 2. Metrics Dashboard (`02-metrics-dashboard.py`)

**O que você vai aprender:**
- Definir KPIs para RAG
- Criar queries de monitoramento
- Implementar SLOs
- Gerar relatórios automatizados

**KPIs definidos:**
| KPI | Target | Descrição |
|-----|--------|-----------|
| Availability | 99.5% | % requests com sucesso |
| P95 Latency | 5000ms | Latência no percentil 95 |
| Error Rate | <0.5% | % requests com erro |
| Throughput | 100 rpm | Requests por minuto |

### 3. Alerting (`03-alerting.py`)

**O que você vai aprender:**
- Definir regras de alerta
- Implementar detecção de anomalias (Z-score)
- Detectar mudanças de tendência
- Criar runbook de resposta

**Regras de alerta:**
| Alerta | Severidade | Threshold |
|--------|------------|-----------|
| availability_drop | CRITICAL | <99% |
| high_error_rate | ERROR | >5% |
| no_requests | ERROR | <1 em 30min |
| high_latency_p95 | WARNING | >5000ms |

## Arquitetura de Monitoramento

```
┌─────────────────────────────────────────────────────────────────┐
│                     Model Serving Endpoint                       │
│                   nasa-gcn-rag-assistant                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼ Auto-capture
┌─────────────────────────────────────────────────────────────────┐
│                     Inference Tables                             │
│                rag_inference_payload                             │
│                rag_inference_response                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │  Metrics  │   │  Alerts   │   │ Anomaly   │
    │ Dashboard │   │  Engine   │   │ Detection │
    └───────────┘   └───────────┘   └───────────┘
            │               │               │
            └───────────────┼───────────────┘
                            ▼
                    ┌───────────────┐
                    │ Notifications │
                    │ Slack/Email   │
                    └───────────────┘
```

## Recursos Criados

| Recurso | Nome | Descrição |
|---------|------|-----------|
| Table | `inference_logs_sample` | Logs de inferência simulados |
| Table | `inference_daily_metrics` | Métricas agregadas por dia |
| View | `v_rag_monitoring_dashboard` | Dados para dashboard |
| Table | `alert_history` | Histórico de alertas |
| Table | `monitoring_reports` | Relatórios gerados |
| Table | `monitoring_runbook` | Procedimentos de resposta |

## Queries Úteis

### Resumo da última hora
```sql
SELECT
    COUNT(*) as total_requests,
    ROUND(AVG(execution_time_ms), 0) as avg_latency_ms,
    ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency_ms,
    ROUND(SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as availability
FROM inference_logs_sample
WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR
```

### Trend de latência por versão
```sql
SELECT
    DATE(timestamp) as date,
    model_version,
    COUNT(*) as requests,
    ROUND(PERCENTILE(execution_time_ms, 0.95), 0) as p95_latency
FROM inference_logs_sample
GROUP BY DATE(timestamp), model_version
ORDER BY date, model_version
```

### Alertas ativos
```sql
SELECT *
FROM alert_history
WHERE status = 'firing'
ORDER BY timestamp DESC
```

## SLOs (Service Level Objectives)

| SLO | Target | Window | Query |
|-----|--------|--------|-------|
| Availability | 99.5% | 1 day | `successful/total * 100` |
| Latency P95 | 5000ms | 1 hour | `percentile(latency, 0.95)` |
| Error Budget | 0.5% | 1 month | `errors/total * 100` |

## Anomaly Detection

### Z-score para latência
```python
# Identificar requests com latência > 3 desvios padrão
anomalies = spark.sql("""
    SELECT *
    FROM inference_logs_sample
    WHERE ABS((execution_time_ms - {mean}) / {std}) > 3
""")
```

### Detecção de mudança de tendência
- Compara período atual vs anterior
- Alerta se mudança > 30%

## Runbook de Resposta

| Alerta | Primeira Ação | Escalonamento |
|--------|---------------|---------------|
| CRITICAL | Verificar endpoint status | 15 min |
| ERROR | Identificar padrão | 30 min |
| WARNING | Monitorar tendência | 1 hora |

## Boas Práticas

1. **Retention**: Manter logs por pelo menos 30 dias
2. **Agregação**: Pré-agregar métricas para performance
3. **Alertas**: Evitar alert fatigue com thresholds adequados
4. **Runbook**: Manter procedimentos atualizados
5. **Revisão**: Revisar SLOs trimestralmente

## Próximos Passos

Após completar este lab, continue para:

- **Lab 9: Vector Optimization** - Otimização de retrieval
- **Lab 10: Readiness Assessment** - Checklist de produção

## Referências

- [Databricks Inference Tables](https://docs.databricks.com/en/machine-learning/model-serving/inference-tables.html)
- [MLflow Model Monitoring](https://mlflow.org/docs/latest/model-registry.html)
- [SRE Book - SLOs](https://sre.google/sre-book/service-level-objectives/)

---

*Última atualização: Fevereiro 2026*
