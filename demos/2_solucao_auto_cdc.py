# Databricks notebook source
# MAGIC %md
# MAGIC # Solução: AUTO CDC para Deduplicação no SDP
# MAGIC
# MAGIC Este notebook demonstra como usar **AUTO CDC** (Change Data Capture) no
# MAGIC Spark Declarative Pipelines para resolver o problema de duplicatas.
# MAGIC
# MAGIC ## O que é AUTO CDC?
# MAGIC
# MAGIC AUTO CDC é uma funcionalidade do SDP que automaticamente:
# MAGIC - **Deduplica** registros por chave primária
# MAGIC - **Ordena** por timestamp (SEQUENCE BY)
# MAGIC - **Mantém histórico** (SCD Type 2) ou **sobrescreve** (SCD Type 1)
# MAGIC
# MAGIC ## Requisitos
# MAGIC - Databricks Runtime com suporte a SDP
# MAGIC - Unity Catalog habilitado
# MAGIC - Serverless ou cluster com edition ADVANCED/PRO

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Configuração

# COMMAND ----------

# Configurar catálogo
CATALOG = "sandbox"  # ou "nasa_gcn" para prod
SCHEMA_SILVER = "silver"
SCHEMA_GOLD = "gold"

spark.sql(f"USE CATALOG {CATALOG}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Conceitos: SCD Type 1 vs Type 2
# MAGIC
# MAGIC ### SCD Type 1 (Sobrescrever)
# MAGIC - Mantém apenas o **registro mais recente**
# MAGIC - Útil quando só importa o estado atual
# MAGIC - Exemplo: último alerta de um evento GW
# MAGIC
# MAGIC ### SCD Type 2 (Histórico)
# MAGIC - Mantém **todos os registros** com timestamps de validade
# MAGIC - Colunas `__START_AT` e `__END_AT` são adicionadas
# MAGIC - Útil para auditoria e análise temporal
# MAGIC - Exemplo: histórico completo de alertas de um evento

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Exemplo SQL: AUTO CDC com SCD Type 1
# MAGIC
# MAGIC Este exemplo cria uma tabela com apenas o **último alerta** por evento.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Primeiro, vamos ver o estado atual (com duplicatas)
# MAGIC SELECT
# MAGIC     event_id,
# MAGIC     COUNT(*) as total_alerts,
# MAGIC     MAX(kafka_timestamp) as last_alert_time
# MAGIC FROM sandbox.silver.gcn_gwalert
# MAGIC WHERE event_id IS NOT NULL
# MAGIC GROUP BY event_id
# MAGIC HAVING COUNT(*) > 1
# MAGIC ORDER BY total_alerts DESC
# MAGIC LIMIT 5

# COMMAND ----------

# MAGIC %md
# MAGIC ### Sintaxe AUTO CDC (para referência)
# MAGIC
# MAGIC ```sql
# MAGIC -- Este código seria usado em um arquivo .sql do pipeline SDP
# MAGIC -- NÃO execute diretamente - é apenas para demonstração
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE gcn_gwalert_latest;
# MAGIC
# MAGIC CREATE FLOW gwalert_dedup_flow AS
# MAGIC AUTO CDC INTO gcn_gwalert_latest
# MAGIC FROM stream(bronze.gcn_raw)
# MAGIC KEYS (event_id)                    -- Chave de deduplicação
# MAGIC SEQUENCE BY kafka_timestamp        -- Mais recente vence
# MAGIC WHERE topic = 'igwn.gwalert'
# MAGIC COLUMNS (
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     json,
# MAGIC     kafka_timestamp
# MAGIC )
# MAGIC STORED AS SCD TYPE 1;              -- Sobrescreve registro anterior
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Simulação: Deduplicação Manual (sem AUTO CDC)
# MAGIC
# MAGIC Para demonstrar o conceito, vamos simular o comportamento do SCD Type 1
# MAGIC usando SQL padrão.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Simular SCD Type 1: Manter apenas o último alerta por evento
# MAGIC CREATE OR REPLACE TEMPORARY VIEW gcn_gwalert_latest_simulated AS
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC     SELECT
# MAGIC         *,
# MAGIC         ROW_NUMBER() OVER (
# MAGIC             PARTITION BY event_id
# MAGIC             ORDER BY kafka_timestamp DESC
# MAGIC         ) as rn
# MAGIC     FROM sandbox.silver.gcn_gwalert
# MAGIC     WHERE event_id IS NOT NULL
# MAGIC )
# MAGIC WHERE rn = 1

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Comparar: Antes vs Depois da deduplicação
# MAGIC SELECT
# MAGIC     'Original (com duplicatas)' as versao,
# MAGIC     COUNT(*) as total_registros,
# MAGIC     COUNT(DISTINCT event_id) as eventos_unicos
# MAGIC FROM sandbox.silver.gcn_gwalert
# MAGIC WHERE event_id IS NOT NULL
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'Deduplicado (SCD Type 1)' as versao,
# MAGIC     COUNT(*) as total_registros,
# MAGIC     COUNT(DISTINCT event_id) as eventos_unicos
# MAGIC FROM gcn_gwalert_latest_simulated

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Ver resultado: Apenas o último alerta por evento
# MAGIC SELECT
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     kafka_timestamp
# MAGIC FROM gcn_gwalert_latest_simulated
# MAGIC ORDER BY kafka_timestamp DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Exemplo SQL: AUTO CDC com SCD Type 2
# MAGIC
# MAGIC Mantém o histórico completo com timestamps de validade.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Sintaxe AUTO CDC SCD Type 2 (para referência)
# MAGIC
# MAGIC ```sql
# MAGIC -- Este código seria usado em um arquivo .sql do pipeline SDP
# MAGIC -- NÃO execute diretamente - é apenas para demonstração
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE gcn_gwalert_history;
# MAGIC
# MAGIC CREATE FLOW gwalert_history_flow AS
# MAGIC AUTO CDC INTO gcn_gwalert_history
# MAGIC FROM stream(bronze.gcn_raw)
# MAGIC KEYS (event_id)
# MAGIC SEQUENCE BY kafka_timestamp
# MAGIC WHERE topic = 'igwn.gwalert'
# MAGIC COLUMNS (
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     json,
# MAGIC     kafka_timestamp
# MAGIC )
# MAGIC STORED AS SCD TYPE 2;              -- Mantém histórico
# MAGIC ```
# MAGIC
# MAGIC ### Resultado do SCD Type 2
# MAGIC
# MAGIC A tabela terá colunas adicionais:
# MAGIC - `__START_AT`: Quando este registro se tornou válido
# MAGIC - `__END_AT`: Quando este registro foi substituído (NULL = atual)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Simulação: SCD Type 2 Manual

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Simular SCD Type 2: Adicionar timestamps de validade
# MAGIC CREATE OR REPLACE TEMPORARY VIEW gcn_gwalert_history_simulated AS
# MAGIC SELECT
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     json,
# MAGIC     kafka_timestamp,
# MAGIC     kafka_timestamp as __START_AT,
# MAGIC     LEAD(kafka_timestamp) OVER (
# MAGIC         PARTITION BY event_id
# MAGIC         ORDER BY kafka_timestamp
# MAGIC     ) as __END_AT
# MAGIC FROM sandbox.silver.gcn_gwalert
# MAGIC WHERE event_id IS NOT NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Ver histórico de um evento específico
# MAGIC SELECT
# MAGIC     event_id,
# MAGIC     alert_type,
# MAGIC     kafka_timestamp,
# MAGIC     __START_AT,
# MAGIC     __END_AT,
# MAGIC     CASE WHEN __END_AT IS NULL THEN 'CURRENT' ELSE 'HISTORICAL' END as status
# MAGIC FROM gcn_gwalert_history_simulated
# MAGIC WHERE event_id IN (
# MAGIC     SELECT event_id
# MAGIC     FROM sandbox.silver.gcn_gwalert
# MAGIC     GROUP BY event_id
# MAGIC     HAVING COUNT(*) > 3
# MAGIC     LIMIT 1
# MAGIC )
# MAGIC ORDER BY kafka_timestamp

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Consultas Úteis com SCD Type 2
# MAGIC
# MAGIC ### 7.1 Estado Atual (Current State)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Obter apenas registros atuais (equivalente a SCD Type 1)
# MAGIC SELECT *
# MAGIC FROM gcn_gwalert_history_simulated
# MAGIC WHERE __END_AT IS NULL
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7.2 Point-in-Time Query (Estado em um momento específico)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Qual era o estado dos eventos há 7 dias?
# MAGIC SELECT *
# MAGIC FROM gcn_gwalert_history_simulated
# MAGIC WHERE __START_AT <= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
# MAGIC   AND (__END_AT IS NULL OR __END_AT > DATEADD(DAY, -7, CURRENT_TIMESTAMP()))
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Implementação no Pipeline SDP (Python)
# MAGIC
# MAGIC Para implementar AUTO CDC em Python no SDP, você usaria:

# COMMAND ----------

# Este é um EXEMPLO de código - não execute diretamente
# Seria usado em um arquivo de pipeline .py

example_code = '''
from pyspark import pipelines as dp

# Para SCD Type 1 em Python, você usaria uma abordagem diferente
# já que AUTO CDC é mais comum em SQL

# Alternativa: Usar dropDuplicates com watermark
@dp.table(
    name="gcn_gwalert_dedup",
    comment="Deduplicated GW alerts - latest per event",
)
def gwalert_dedup():
    return (
        spark.readStream.table("bronze.gcn_raw")
        .filter(col("topic") == "igwn.gwalert")
        .withWatermark("kafka_timestamp", "1 hour")
        .dropDuplicatesWithinWatermark(["event_id"])
    )

# Ou usando window function para batch
@dp.materialized_view(
    name="gcn_gwalert_latest",
    comment="Latest GW alert per event (SCD Type 1 equivalent)",
)
def gwalert_latest():
    from pyspark.sql.window import Window
    from pyspark.sql.functions import row_number

    window = Window.partitionBy("event_id").orderBy(col("kafka_timestamp").desc())

    return (
        spark.read.table("silver.gcn_gwalert")
        .withColumn("rn", row_number().over(window))
        .filter(col("rn") == 1)
        .drop("rn")
    )
'''

print(example_code)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Resumo: Quando Usar Cada Abordagem
# MAGIC
# MAGIC | Cenário | Abordagem | Implementação |
# MAGIC |---------|-----------|---------------|
# MAGIC | Apenas último registro | **SCD Type 1** | `STORED AS SCD TYPE 1` |
# MAGIC | Histórico completo | **SCD Type 2** | `STORED AS SCD TYPE 2` |
# MAGIC | Streaming com dedup | **dropDuplicatesWithinWatermark** | Python API |
# MAGIC | Batch com dedup | **ROW_NUMBER()** | SQL ou Python |
# MAGIC | Simples, sem CDC | **DISTINCT** ou **GROUP BY** | SQL |
# MAGIC
# MAGIC ## 10. Benefícios do AUTO CDC
# MAGIC
# MAGIC 1. **Declarativo**: Define O QUE fazer, não COMO
# MAGIC 2. **Incremental**: Processa apenas novos dados
# MAGIC 3. **Automático**: Gerencia estado internamente
# MAGIC 4. **Eficiente**: Otimizado pelo Databricks
# MAGIC 5. **Histórico**: SCD Type 2 preserva auditoria

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos Passos
# MAGIC
# MAGIC Para implementar AUTO CDC no pipeline NASA GCN:
# MAGIC
# MAGIC 1. Criar novo arquivo SQL em `src/nasa_gcn/pipelines/`
# MAGIC 2. Definir o FLOW com AUTO CDC
# MAGIC 3. Adicionar ao job de orquestração
# MAGIC 4. Testar em dev antes de prod
# MAGIC
# MAGIC Consulte a documentação oficial:
# MAGIC - [SDP CDC Documentation](https://docs.databricks.com/aws/en/ldp/cdc)
