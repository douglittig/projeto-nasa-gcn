# Databricks notebook source
# MAGIC %md
# MAGIC # Validação: AUTO CDC SCD Type 2 - gcn_gwalert
# MAGIC
# MAGIC Este notebook valida a implementação do AUTO CDC para a tabela `gcn_gwalert`.
# MAGIC
# MAGIC ## O que é AUTO CDC com SCD Type 2?
# MAGIC
# MAGIC **AUTO CDC** (Change Data Capture) é uma funcionalidade do Spark Declarative Pipelines que:
# MAGIC - **Deduplica** registros automaticamente por chave primária (`event_id`)
# MAGIC - **Mantém histórico completo** de todas as versões de cada evento
# MAGIC - **Adiciona colunas temporais**: `__START_AT` e `__END_AT`
# MAGIC
# MAGIC **SCD Type 2** (Slowly Changing Dimension Type 2) preserva o histórico:
# MAGIC - Cada vez que um evento recebe um novo alerta, a versão anterior é "fechada"
# MAGIC - A coluna `__END_AT` indica quando aquela versão foi substituída
# MAGIC - Registros atuais têm `__END_AT = NULL`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuração

# COMMAND ----------

CATALOG = "sandbox"  # ou "nasa_gcn" para prod

spark.sql(f"USE CATALOG {CATALOG}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Contagens: Bronze → Parsed → CDC
# MAGIC
# MAGIC Esta query compara as contagens em cada etapa do pipeline para validar que:
# MAGIC - Todos os registros da Bronze foram parseados corretamente
# MAGIC - O histórico completo está preservado no CDC
# MAGIC - A deduplicação está funcionando (CURRENT < ALL)
# MAGIC
# MAGIC **Esperado:**
# MAGIC - Bronze e Parsed devem ter a mesma contagem (todos alertas)
# MAGIC - CDC ALL = histórico completo preservado
# MAGIC - CDC CURRENT = apenas o último estado de cada evento (deduplicado)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Bronze (gcn_raw - gwalert only)' as etapa, COUNT(*) as total
# MAGIC FROM bronze.gcn_raw
# MAGIC WHERE topic = 'igwn.gwalert'
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'Silver (gcn_gwalert_parsed)' as etapa, COUNT(*) as total
# MAGIC FROM silver.gcn_gwalert_parsed
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'Silver (gcn_gwalert - ALL rows)' as etapa, COUNT(*) as total
# MAGIC FROM silver.gcn_gwalert
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'Silver (gcn_gwalert - CURRENT only)' as etapa, COUNT(*) as total
# MAGIC FROM silver.gcn_gwalert
# MAGIC WHERE __END_AT IS NULL

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validar Deduplicação
# MAGIC
# MAGIC Esta query verifica se a deduplicação está funcionando corretamente:
# MAGIC - Conta registros atuais (`__END_AT IS NULL`)
# MAGIC - Conta eventos únicos (`DISTINCT event_id`)
# MAGIC - Se forem iguais, cada evento tem exatamente 1 registro atual
# MAGIC
# MAGIC **Esperado:** `total_registros_atuais = eventos_unicos` → ✅ DEDUPLICADO

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) as total_registros_atuais,
# MAGIC     COUNT(DISTINCT event_id) as eventos_unicos,
# MAGIC     CASE
# MAGIC         WHEN COUNT(*) = COUNT(DISTINCT event_id) THEN '✅ DEDUPLICADO'
# MAGIC         ELSE '❌ DUPLICATAS ENCONTRADAS'
# MAGIC     END as status_deduplicacao
# MAGIC FROM silver.gcn_gwalert
# MAGIC WHERE __END_AT IS NULL

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verificar Estrutura SCD Type 2
# MAGIC
# MAGIC O SCD Type 2 adiciona duas colunas especiais à tabela:
# MAGIC - `__START_AT`: Timestamp de quando esta versão do registro se tornou válida
# MAGIC - `__END_AT`: Timestamp de quando esta versão foi substituída (NULL = registro atual)
# MAGIC
# MAGIC A tabela também está clusterizada por `event_id` para otimizar consultas.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE silver.gcn_gwalert

# COMMAND ----------

# MAGIC %md
# MAGIC ## Visualizar Histórico de Eventos
# MAGIC
# MAGIC Esta query mostra como o SCD Type 2 preserva o histórico completo de cada evento.
# MAGIC
# MAGIC **Exemplo típico de um evento gravitacional:**
# MAGIC ```
# MAGIC PRELIMINARY (detecção automática) → PRELIMINARY (atualização) → INITIAL/RETRACTION (confirmação/cancelamento)
# MAGIC ```
# MAGIC
# MAGIC - Registros `HISTORICAL` têm `__END_AT` preenchido (foram substituídos)
# MAGIC - Registro `CURRENT` tem `__END_AT = NULL` (é o estado atual)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     kafka_timestamp,
# MAGIC     __START_AT,
# MAGIC     __END_AT,
# MAGIC     CASE WHEN __END_AT IS NULL THEN 'CURRENT' ELSE 'HISTORICAL' END as status
# MAGIC FROM silver.gcn_gwalert
# MAGIC ORDER BY event_id, __START_AT
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %md
# MAGIC ## Histórico Detalhado de um Evento
# MAGIC
# MAGIC Mostra a progressão completa de um evento específico com múltiplas versões.
# MAGIC
# MAGIC **Interpretação:**
# MAGIC - Cada linha representa um estado do evento em um momento no tempo
# MAGIC - `__START_AT` = quando este alerta chegou
# MAGIC - `__END_AT` = quando foi substituído pelo próximo alerta
# MAGIC - `→ CURRENT` = estado atual do evento (última informação disponível)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     kafka_timestamp,
# MAGIC     __START_AT,
# MAGIC     __END_AT,
# MAGIC     CASE WHEN __END_AT IS NULL THEN '→ CURRENT' ELSE '' END as is_current
# MAGIC FROM silver.gcn_gwalert
# MAGIC WHERE event_id IN (
# MAGIC     SELECT event_id
# MAGIC     FROM silver.gcn_gwalert
# MAGIC     GROUP BY event_id
# MAGIC     HAVING COUNT(*) > 2
# MAGIC     LIMIT 1
# MAGIC )
# MAGIC ORDER BY __START_AT

# COMMAND ----------

# MAGIC %md
# MAGIC ## Distribuição de Tipos de Alerta (Estado Atual)
# MAGIC
# MAGIC Mostra a distribuição dos tipos de alerta considerando apenas o estado atual de cada evento.
# MAGIC
# MAGIC **Tipos de alerta GCN:**
# MAGIC - `PRELIMINARY`: Detecção automática inicial (pode ser falso positivo)
# MAGIC - `INITIAL`: Primeira confirmação por análise humana
# MAGIC - `UPDATE`: Atualização com mais dados/análise
# MAGIC - `RETRACTION`: Cancelamento (falso positivo confirmado)
# MAGIC
# MAGIC **Nota:** A maioria dos eventos termina em RETRACTION (falsos positivos) ou INITIAL (confirmados).
# MAGIC Poucos eventos permanecem em PRELIMINARY (aguardando análise).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     alert_type,
# MAGIC     COUNT(*) as count,
# MAGIC     ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
# MAGIC FROM silver.gcn_gwalert
# MAGIC WHERE __END_AT IS NULL
# MAGIC GROUP BY alert_type
# MAGIC ORDER BY count DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo da Validação
# MAGIC
# MAGIC Gera um relatório completo validando:
# MAGIC 1. **Pipeline completo**: Bronze → Parsed → CDC
# MAGIC 2. **Deduplicação**: Registros atuais = Eventos únicos
# MAGIC 3. **Histórico**: Total CDC >= Registros atuais

# COMMAND ----------

summary = spark.sql("""
    SELECT
        (SELECT COUNT(*) FROM bronze.gcn_raw WHERE topic = 'igwn.gwalert') as bronze_count,
        (SELECT COUNT(*) FROM silver.gcn_gwalert_parsed) as parsed_count,
        (SELECT COUNT(*) FROM silver.gcn_gwalert) as cdc_total_count,
        (SELECT COUNT(*) FROM silver.gcn_gwalert WHERE __END_AT IS NULL) as cdc_current_count,
        (SELECT COUNT(DISTINCT event_id) FROM silver.gcn_gwalert WHERE __END_AT IS NULL) as unique_events
""").collect()[0]

print("=" * 60)
print("RESUMO DA VALIDAÇÃO - AUTO CDC SCD Type 2")
print("=" * 60)
print(f"Bronze (gcn_raw gwalert):     {summary['bronze_count']:,}")
print(f"Parsed (gcn_gwalert_parsed):  {summary['parsed_count']:,}")
print(f"CDC Total (all versions):     {summary['cdc_total_count']:,}")
print(f"CDC Current (__END_AT NULL):  {summary['cdc_current_count']:,}")
print(f"Eventos Únicos:               {summary['unique_events']:,}")
print("=" * 60)

# Calcular taxa de deduplicação
if summary['bronze_count'] > 0:
    dedup_rate = (1 - summary['cdc_current_count'] / summary['bronze_count']) * 100
    print(f"Taxa de Deduplicação:         {dedup_rate:.1f}%")
    print(f"Média alertas/evento:         {summary['bronze_count'] / summary['unique_events']:.1f}")
    print("=" * 60)

if summary['cdc_current_count'] == summary['unique_events']:
    print("✅ VALIDAÇÃO OK: Deduplicação funcionando corretamente!")
else:
    print("❌ ERRO: Contagem de registros atuais != eventos únicos")

if summary['cdc_total_count'] >= summary['cdc_current_count']:
    print("✅ VALIDAÇÃO OK: Histórico sendo preservado!")
else:
    print("❌ ERRO: Problema no histórico")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Como Usar a Tabela Deduplicada
# MAGIC
# MAGIC ### Consultar apenas o estado atual (deduplicado)
# MAGIC ```sql
# MAGIC SELECT * FROM silver.gcn_gwalert WHERE __END_AT IS NULL
# MAGIC ```
# MAGIC
# MAGIC ### Consultar histórico completo de um evento
# MAGIC ```sql
# MAGIC SELECT * FROM silver.gcn_gwalert
# MAGIC WHERE event_id = 'MS260126c'
# MAGIC ORDER BY __START_AT
# MAGIC ```
# MAGIC
# MAGIC ### Point-in-time query (estado em um momento específico)
# MAGIC ```sql
# MAGIC SELECT * FROM silver.gcn_gwalert
# MAGIC WHERE __START_AT <= '2026-01-26 03:00:00'
# MAGIC   AND (__END_AT IS NULL OR __END_AT > '2026-01-26 03:00:00')
# MAGIC ```
