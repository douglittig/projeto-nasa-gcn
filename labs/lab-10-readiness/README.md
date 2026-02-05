# Lab 10: Production Readiness Assessment

Este lab implementa uma avaliação completa de prontidão para produção do sistema RAG.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Executar checklists sistemáticos** de produção
2. **Simular cenários de carga** em produção
3. **Validar SLOs e métricas** de performance
4. **Identificar gaps** antes do go-live

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 1: Design** | 22% | Production architecture |
| **Section 3: Application Development** | 30% | Deployment validation |
| **Section 4: Evaluation and Monitoring** | 18% | SLO validation, metrics |
| **Section 5: Governance** | 17% | Security, compliance |

## Pré-requisitos

- Labs 1-9 completos
- Sistema RAG deployado
- Model Serving endpoint ativo
- Vector Search index sincronizado

## Estrutura do Lab

```
lab-10-readiness/
├── 01-checklist.py      # Production readiness checklist
├── 02-simulation.py     # Load testing e simulação
└── README.md            # Este arquivo
```

## Notebooks

### 1. Production Checklist (`01-checklist.py`)

**O que você vai aprender:**
- Framework de checklist estruturado
- Verificações automatizadas de componentes
- Categorização de checks (critical vs optional)
- Geração de relatórios de readiness

**Categorias de Verificação:**
| Categoria | Checks | Críticos |
|-----------|--------|----------|
| Data Quality | 3 | 2 |
| Model | 3 | 3 |
| Deployment | 3 | 3 |
| Monitoring | 3 | 1 |
| Security | 3 | 2 |
| Governance | 3 | 0 |

**Checks Críticos:**
- Source data available
- Chunks table populated
- Model registered in UC
- Model has champion alias
- Model evaluation passed
- Vector Search endpoint ready
- Vector Search index synced
- Model Serving endpoint ready
- Inference logging enabled
- PII scanning completed
- Guardrails implemented

### 2. Production Simulation (`02-simulation.py`)

**O que você vai aprender:**
- Simulação de carga de produção
- Testes de resiliência e edge cases
- Medição de latência sob diferentes cargas
- Análise de compliance com SLOs

**Cenários de Teste:**
| Cenário | Usuários | Queries | Target P95 |
|---------|----------|---------|------------|
| Light Load | 2 | 5 | 5000ms |
| Normal Load | 5 | 10 | 8000ms |
| Peak Load | 10 | 20 | 15000ms |

**Testes de Resiliência:**
- Empty queries
- Very long queries
- Special characters
- SQL injection attempts
- Unicode stress test
- Prompt injection

## Framework de Readiness

### Status Possíveis

| Status | Símbolo | Significado |
|--------|---------|-------------|
| PASS | OK | Check passou |
| FAIL | FAIL | Check falhou (crítico) |
| WARN | WARN | Atenção necessária |
| SKIP | SKIP | Verificação manual |

### Critérios de Go-Live

```
Production Ready = (Critical Failures == 0)
```

- **Ready**: Todos os checks críticos passaram
- **Not Ready**: Um ou mais checks críticos falharam

## Métricas Coletadas

### Checklist
| Métrica | Descrição |
|---------|-----------|
| Pass Rate | % de checks que passaram |
| Critical Failures | Número de falhas críticas |
| Warnings | Número de warnings |

### Simulação
| Métrica | Descrição |
|---------|-----------|
| Success Rate | % de queries bem-sucedidas |
| Latency P50 | Mediana de latência |
| Latency P95 | Percentil 95 de latência |
| Latency P99 | Percentil 99 de latência |
| SLO Compliance | % de SLOs atingidos |

## Recursos Criados

| Recurso | Nome | Descrição |
|---------|------|-----------|
| Table | `readiness_check_results` | Resultados do checklist |
| Table | `readiness_summary_history` | Histórico de assessments |
| Table | `simulation_metrics` | Métricas de simulação |
| Table | `simulation_query_results` | Resultados de queries |
| Table | `simulation_resilience_results` | Testes de resiliência |

## Checklist de Go-Live

### Pre-Deployment
- [ ] Todos os Labs (1-9) completos
- [ ] Code review aprovado
- [ ] Documentação atualizada
- [ ] Runbook disponível

### Data Quality
- [ ] Tabelas source com dados
- [ ] Chunks table populada
- [ ] Dados atualizados

### Model
- [ ] Modelo registrado no Unity Catalog
- [ ] Alias "champion" configurado
- [ ] Avaliação passou thresholds

### Infrastructure
- [ ] VS endpoint ONLINE
- [ ] VS index sincronizado
- [ ] Model Serving READY
- [ ] Inference logging ativo

### Security
- [ ] PII scan executado
- [ ] Guardrails implementados
- [ ] Permissões configuradas

### Monitoring
- [ ] Alertas configurados
- [ ] Dashboard disponível
- [ ] Runbook documentado

## Comandos Úteis

### Executar checklist
```python
results = run_checklist()
critical_failures = [r for r in results if r.status == CheckStatus.FAIL]
is_ready = len(critical_failures) == 0
```

### Rodar simulação
```python
simulator = ProductionSimulator()
for scenario in SCENARIOS:
    metrics = simulator.run_scenario(scenario)
    print(f"SLO Met: {metrics['slo_met']}")
```

### Query histórico
```sql
SELECT
    timestamp,
    is_ready,
    passed,
    failed,
    critical_failures
FROM readiness_summary_history
ORDER BY timestamp DESC
```

## SLOs Recomendados

| Métrica | Target | Alerting |
|---------|--------|----------|
| Availability | 99.5% | <99% |
| Latency P95 | <5s | >8s |
| Error Rate | <1% | >5% |
| Success Rate | >95% | <90% |

## Troubleshooting

### Check falhou: Model not registered
- Executar Lab 6 (Model Registration)
- Verificar permissões no Unity Catalog

### Check falhou: VS endpoint not ready
- Verificar status no workspace
- Aguardar provisioning (pode levar minutos)

### Simulação: Alta latência
- Verificar escalonamento do endpoint
- Considerar otimização do retrieval (Lab 9)

### Simulação: Baixo success rate
- Verificar logs do endpoint
- Analisar patterns de erro

## Boas Práticas

1. **Executar periodicamente**: Rodar checklist antes de cada deploy
2. **Automatizar**: Integrar no CI/CD pipeline
3. **Documentar exceptions**: Registrar motivos de SKIPs
4. **Monitorar trends**: Acompanhar histórico de readiness
5. **Load test em staging**: Simular antes de produção

## Próximos Passos

Após completar este lab:

1. **Go-Live**: Se todos checks passaram, deploy para produção
2. **Monitoramento**: Configurar alertas e dashboards
3. **Iterate**: Usar feedback para melhorar o sistema

## Referências

- [MLOps Best Practices](https://docs.databricks.com/en/machine-learning/mlops/index.html)
- [Model Serving SLOs](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
- [Production ML Checklist](https://ml-ops.org/content/mlops-principles)

---

*Última atualização: Fevereiro 2026*
