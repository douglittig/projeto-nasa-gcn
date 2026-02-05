# Databricks notebook source
# MAGIC %pip install mlflow>=3

# COMMAND ----------

import mlflow
print(mlflow.__version__)

# COMMAND ----------

# MAGIC %md
# MAGIC # Lab 3.1: Extract GCN Circulars for RAG
# MAGIC
# MAGIC Este notebook extrai e prepara os GCN Circulars da camada Silver para processamento RAG.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Conectar à tabela Silver `gcn_circulars`
# MAGIC 2. Explorar a estrutura dos dados
# MAGIC 3. Filtrar e limpar documentos
# MAGIC 4. Preparar dataset para chunking
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 2: Data Preparation (14%)
# MAGIC - Identify source documents for RAG application quality
# MAGIC - Filter extraneous content that degrades RAG quality

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Configuração do Catálogo
# Configurar o catálogo e schema
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print(f"✅ Usando: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Explorar os Dados

# COMMAND ----------

# DBTITLE 1,Carregar tabela gcn_circulars
# Carregar a tabela Silver de circulars
df_circulars = spark.table("gcn_circulars")

# Verificar schema
print("📋 Schema da tabela gcn_circulars:")
df_circulars.printSchema()

# COMMAND ----------

# DBTITLE 1,Estatísticas básicas
from pyspark.sql.functions import col, count, avg, min, max, length

# Estatísticas gerais
stats = df_circulars.agg(
    count("*").alias("total_circulars"),
    count("event_id").alias("with_event_id"),
    count("body").alias("with_body"),
    avg(length("body")).alias("avg_body_length"),
    min("created_on").alias("oldest"),
    max("created_on").alias("newest")
).collect()[0]

print(f"""
📊 Estatísticas dos GCN Circulars:
─────────────────────────────────
Total de circulars:     {stats.total_circulars:,}
Com event_id:           {stats.with_event_id:,}
Com body:               {stats.with_body:,}
Tamanho médio do body:  {stats.avg_body_length:,.0f} chars
Mais antigo:            {stats.oldest}
Mais recente:           {stats.newest}
""")

# COMMAND ----------

# DBTITLE 1,Distribuição por tipo de evento
from pyspark.sql.functions import regexp_extract, when

# Extrair tipo de evento do event_id (ex: GRB, GW, SN, etc.)
df_with_type = df_circulars.withColumn(
    "event_type",
    when(col("event_id").startswith("GRB"), "GRB (Gamma-Ray Burst)")
    .when(col("event_id").startswith("GW"), "GW (Gravitational Wave)")
    .when(col("event_id").startswith("S"), "GW (Gravitational Wave)")
    .when(col("event_id").startswith("SN"), "SN (Supernova)")
    .when(col("event_id").startswith("AT"), "AT (Astronomical Transient)")
    .when(col("event_id").startswith("IceCube"), "IceCube (Neutrino)")
    .otherwise("Other")
)

# Contagem por tipo
print("📈 Distribuição por tipo de evento:")
df_with_type.groupBy("event_type").count().orderBy(col("count").desc()).show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Análise de Qualidade dos Documentos

# COMMAND ----------

# DBTITLE 1,Distribuição de tamanho dos documentos
from pyspark.sql.functions import length, when, floor

# Calcular tamanho em caracteres e palavras estimadas
df_sized = df_circulars.withColumn(
    "char_count", length("body")
).withColumn(
    "word_count_est", floor(length("body") / 5)  # ~5 chars por palavra em inglês
).withColumn(
    "token_count_est", floor(length("body") / 4)  # ~4 chars por token
)

# Categorizar por tamanho
df_categorized = df_sized.withColumn(
    "size_category",
    when(col("char_count") < 200, "tiny (<200 chars)")
    .when(col("char_count") < 500, "small (200-500)")
    .when(col("char_count") < 1000, "medium (500-1000)")
    .when(col("char_count") < 3000, "large (1000-3000)")
    .otherwise("very_large (3000+)")
)

print("📏 Distribuição por tamanho:")
df_categorized.groupBy("size_category").count().orderBy("size_category").show(truncate=False)

# COMMAND ----------

# DBTITLE 1,Exemplos de documentos por tamanho
# Mostrar exemplo de cada categoria
print("📝 Exemplo de documento SMALL (ideal para chunks únicos):")
df_categorized.filter(col("size_category") == "small (200-500)") \
    .select("circular_id", "subject", "body", "char_count") \
    .limit(1).show(truncate=100, vertical=True)

print("\n📝 Exemplo de documento LARGE (precisa chunking):")
df_categorized.filter(col("size_category") == "large (1000-3000)") \
    .select("circular_id", "subject", "body", "char_count") \
    .limit(1).show(truncate=200, vertical=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Filtrar e Preparar Documentos

# COMMAND ----------

# DBTITLE 1,Filtros de qualidade
from pyspark.sql.functions import trim, lower

# Critérios de filtragem:
# 1. Deve ter body não nulo
# 2. Mínimo 100 caracteres (evitar circulars vazios)
# 3. Máximo 50000 caracteres (evitar documentos extremamente longos)
# 4. Deve ter event_id (para contexto)

MIN_CHARS = 100
MAX_CHARS = 50000

df_filtered = df_circulars.filter(
    (col("body").isNotNull()) &
    (length(col("body")) >= MIN_CHARS) &
    (length(col("body")) <= MAX_CHARS) &
    (col("event_id").isNotNull())
).withColumn(
    "char_count", length("body")
).withColumn(
    "word_count_est", floor(length("body") / 5)
)

# Comparar antes/depois
original_count = df_circulars.count()
filtered_count = df_filtered.count()
removed = original_count - filtered_count

print(f"""
🔍 Resultado da filtragem:
─────────────────────────
Original:    {original_count:,} circulars
Filtrado:    {filtered_count:,} circulars
Removidos:   {removed:,} ({removed/original_count*100:.1f}%)

Critérios aplicados:
  - Body não nulo
  - Mínimo {MIN_CHARS} caracteres
  - Máximo {MAX_CHARS:,} caracteres
  - Event ID presente
""")

# COMMAND ----------

# DBTITLE 1,Criar dataset preparado para chunking
from pyspark.sql.functions import concat_ws, lit, current_timestamp

# Criar documento formatado para RAG
df_prepared = df_filtered.select(
    col("circular_id"),
    col("event_id"),
    col("subject"),
    col("body"),
    col("created_on"),
    col("char_count"),
    col("word_count_est"),
    # Criar document_text enriquecido para embedding
    concat_ws(
        "\n",
        concat_ws(": ", lit("CIRCULAR"), col("circular_id").cast("string")),
        concat_ws(": ", lit("EVENT"), col("event_id")),
        concat_ws(": ", lit("SUBJECT"), col("subject")),
        lit("---"),
        col("body")
    ).alias("document_text"),
    current_timestamp().alias("prepared_at")
)

# Mostrar exemplo
print("📄 Exemplo de documento preparado:")
df_prepared.select("circular_id", "event_id", "document_text", "char_count").limit(1).show(truncate=500, vertical=True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Salvar Dataset Preparado

# COMMAND ----------

# DBTITLE 1,Salvar como tabela Delta
# Salvar dataset preparado para o próximo notebook
TABLE_NAME = "gcn_circulars_prepared"

df_prepared.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(TABLE_NAME)

# Verificar
saved_count = spark.table(TABLE_NAME).count()
print(f"✅ Tabela {CATALOG}.{SCHEMA}.{TABLE_NAME} criada com {saved_count:,} documentos")

# COMMAND ----------

# DBTITLE 1,Estatísticas finais
# Estatísticas do dataset preparado
final_stats = spark.table(TABLE_NAME).agg(
    count("*").alias("total"),
    avg("char_count").alias("avg_chars"),
    avg("word_count_est").alias("avg_words"),
    min("char_count").alias("min_chars"),
    max("char_count").alias("max_chars")
).collect()[0]

print(f"""
📊 Dataset Preparado - Estatísticas Finais:
───────────────────────────────────────────
Total documentos:       {final_stats.total:,}
Média de caracteres:    {final_stats.avg_chars:,.0f}
Média de palavras:      {final_stats.avg_words:,.0f}
Menor documento:        {final_stats.min_chars:,} chars
Maior documento:        {final_stats.max_chars:,} chars

📍 Tabela salva: {CATALOG}.{SCHEMA}.{TABLE_NAME}
📍 Próximo passo: 02-chunking.py
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos Passos
# MAGIC
# MAGIC ✅ Dataset extraído e filtrado
# MAGIC ➡️ Próximo notebook: `02-chunking.py` - Aplicar estratégias de chunking
# MAGIC ➡️ Depois: `03-embeddings-vector-search.py` - Gerar embeddings e criar índice
