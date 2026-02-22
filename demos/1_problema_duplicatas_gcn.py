# Databricks notebook source
# MAGIC %md
# MAGIC # Problema: Duplicatas e Múltiplos Registros no GCN
# MAGIC
# MAGIC Este notebook demonstra o problema de duplicatas e múltiplos registros
# MAGIC no pipeline NASA GCN, especialmente para alertas de ondas gravitacionais.
# MAGIC
# MAGIC ## Contexto
# MAGIC - O GCN (Gamma-ray Coordinates Network) envia alertas de eventos astronômicos
# MAGIC - Um mesmo evento pode gerar MÚLTIPLOS alertas (PRELIMINARY → INITIAL → UPDATE)
# MAGIC - Sem tratamento adequado, temos "duplicatas semânticas" na Silver layer

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Configuração

# COMMAND ----------

# Configurar catálogo (ajuste conforme seu ambiente)
CATALOG = "sandbox"  # ou "nasa_gcn" para prod
SCHEMA_SILVER = "silver"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA_SILVER}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Análise: Alertas de Ondas Gravitacionais (GW Alerts)
# MAGIC
# MAGIC Vamos analisar a tabela `gcn_gwalert` que contém alertas do LIGO/Virgo/KAGRA.

# COMMAND ----------

# Total de registros na tabela
total_alerts = spark.sql("SELECT COUNT(*) as total FROM gcn_gwalert").collect()[0]["total"]
print(f"Total de alertas GW na Silver: {total_alerts:,}")

# COMMAND ----------

# Quantos eventos ÚNICOS temos?
unique_events = spark.sql("""
    SELECT COUNT(DISTINCT event_id) as unique_events
    FROM gcn_gwalert
    WHERE event_id IS NOT NULL
""").collect()[0]["unique_events"]

print(f"Eventos únicos: {unique_events:,}")
print(f"Média de alertas por evento: {total_alerts / unique_events:.1f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Problema Identificado
# MAGIC
# MAGIC Cada evento gravitacional gera múltiplos alertas com diferentes `alert_type`:
# MAGIC - `PRELIMINARY` - Detecção inicial automática
# MAGIC - `INITIAL` - Primeira análise humana
# MAGIC - `UPDATE` - Atualizações com mais dados
# MAGIC - `RETRACTION` - Cancelamento (falso positivo)

# COMMAND ----------

# Distribuição de tipos de alerta
display(spark.sql("""
    SELECT
        alert_type,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
    FROM gcn_gwalert
    GROUP BY alert_type
    ORDER BY count DESC
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Exemplo: Eventos com Múltiplos Alertas

# COMMAND ----------

# Top 10 eventos com mais alertas
display(spark.sql("""
    SELECT
        event_id,
        COUNT(*) as alert_count,
        COLLECT_SET(alert_type) as alert_types,
        MIN(kafka_timestamp) as first_alert,
        MAX(kafka_timestamp) as last_alert,
        TIMESTAMPDIFF(MINUTE, MIN(kafka_timestamp), MAX(kafka_timestamp)) as duration_minutes
    FROM gcn_gwalert
    WHERE event_id IS NOT NULL
    GROUP BY event_id
    HAVING COUNT(*) > 1
    ORDER BY alert_count DESC
    LIMIT 10
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualização: Timeline de um Evento Específico

# COMMAND ----------

# Selecionar um evento com múltiplos alertas para análise detalhada
sample_event = spark.sql("""
    SELECT event_id
    FROM gcn_gwalert
    WHERE event_id IS NOT NULL
    GROUP BY event_id
    HAVING COUNT(*) > 3
    ORDER BY COUNT(*) DESC
    LIMIT 1
""").collect()

if sample_event:
    event_id = sample_event[0]["event_id"]
    print(f"Analisando evento: {event_id}")

    display(spark.sql(f"""
        SELECT
            event_id,
            alert_type,
            kafka_timestamp,
            ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY kafka_timestamp) as sequence
        FROM gcn_gwalert
        WHERE event_id = '{event_id}'
        ORDER BY kafka_timestamp
    """))
else:
    print("Nenhum evento com múltiplos alertas encontrado")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Análise: GCN Circulars
# MAGIC
# MAGIC Circulares científicas também podem ter múltiplas versões para o mesmo evento.

# COMMAND ----------

# Eventos com múltiplas circulares
display(spark.sql("""
    SELECT
        event_id,
        COUNT(*) as circular_count,
        COLLECT_LIST(circular_id) as circular_ids
    FROM gcn_circulars
    WHERE event_id IS NOT NULL
    GROUP BY event_id
    HAVING COUNT(*) > 5
    ORDER BY circular_count DESC
    LIMIT 10
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Impacto na Camada Gold
# MAGIC
# MAGIC Sem deduplicação, as agregações podem ficar incorretas.

# COMMAND ----------

# Verificar a tabela gold de eventos
display(spark.sql(f"""
    SELECT
        event_id,
        circular_count,
        alert_type,
        last_updated
    FROM {CATALOG}.gold.gcn_events_summary
    ORDER BY circular_count DESC
    LIMIT 10
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. O Problema Resumido
# MAGIC
# MAGIC | Cenário | Problema | Impacto |
# MAGIC |---------|----------|---------|
# MAGIC | GW Alerts | Múltiplos alertas por evento | Contagens infladas, estado inconsistente |
# MAGIC | Circulars | Múltiplas circulares por evento | OK (esperado - são documentos diferentes) |
# MAGIC | Notices | Possíveis duplicatas de mensagens | Dados redundantes |
# MAGIC
# MAGIC ### Solução: AUTO CDC
# MAGIC
# MAGIC O próximo notebook demonstra como usar **AUTO CDC** para:
# MAGIC - **SCD Type 1**: Manter apenas o registro mais recente (última versão)
# MAGIC - **SCD Type 2**: Manter histórico completo com timestamps de validade

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximo Passo
# MAGIC
# MAGIC Veja o notebook `2_solucao_auto_cdc` para a implementação da solução.
