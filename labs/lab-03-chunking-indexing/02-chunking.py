# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 3.2: Chunking Strategies for RAG
# MAGIC
# MAGIC Este notebook implementa diferentes estratégias de chunking para os GCN Circulars.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Implementar chunking por caracteres (simples)
# MAGIC 2. Implementar chunking por sentenças (NLTK)
# MAGIC 3. Implementar chunking semântico (parágrafos)
# MAGIC 4. Comparar estratégias e escolher a melhor
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 2: Data Preparation (14%)
# MAGIC - Apply chunking strategy for document structure and model constraints
# MAGIC - Design retrieval systems using advanced chunking strategies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install nltk tiktoken -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports e configuração
import nltk
import tiktoken
from typing import List, Dict, Any
from pyspark.sql.functions import (
    col, udf, explode, lit, length,
    monotonically_increasing_id, concat_ws, size, array
)
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# DBTITLE 1,Carregar dados preparados
# Carregar dataset do notebook anterior
df_prepared = spark.table("gcn_circulars_prepared")

# Estatísticas
total_docs = df_prepared.count()
avg_chars = df_prepared.agg({"char_count": "avg"}).collect()[0][0]

print(f"""
📊 Dataset carregado:
  - Total documentos: {total_docs:,}
  - Média de caracteres: {avg_chars:,.0f}
""")

# Mostrar exemplo
df_prepared.select("circular_id", "event_id", "char_count").show(5)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Estratégia 1: Character-based Chunking
# MAGIC
# MAGIC Chunking simples por número de caracteres com overlap.

# COMMAND ----------

# DBTITLE 1,Definir função de chunking por caracteres
def chunk_by_chars(text: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Divide texto em chunks de tamanho fixo com overlap.

    Args:
        text: Texto a ser dividido
        chunk_size: Tamanho máximo de cada chunk em caracteres
        overlap: Número de caracteres de sobreposição entre chunks

    Returns:
        Lista de dicts com chunk_text, chunk_index, start_pos, end_pos
    """
    if not text or len(text) == 0:
        return []

    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(text):
        end = start + chunk_size

        # Tentar quebrar em espaço para não cortar palavras
        if end < len(text):
            # Procurar último espaço dentro do chunk
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append({
                "chunk_text": chunk_text,
                "chunk_index": chunk_idx,
                "start_pos": start,
                "end_pos": end,
                "char_count": len(chunk_text)
            })
            chunk_idx += 1

        # Próximo chunk começa com overlap
        start = end - overlap if end < len(text) else len(text)

    return chunks

# Testar
test_text = "This is a test. " * 50
test_chunks = chunk_by_chars(test_text, chunk_size=200, overlap=50)
print(f"Texto de {len(test_text)} chars → {len(test_chunks)} chunks")
print(f"Primeiro chunk: '{test_chunks[0]['chunk_text'][:50]}...'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Estratégia 2: Sentence-based Chunking (NLTK)
# MAGIC
# MAGIC Chunking inteligente que respeita limites de sentenças.

# COMMAND ----------

# DBTITLE 1,Definir função de chunking por sentenças
from nltk.tokenize import sent_tokenize

def chunk_by_sentences(text: str, max_chunk_size: int = 500, overlap_sentences: int = 1) -> List[Dict[str, Any]]:
    """
    Divide texto em chunks respeitando limites de sentenças.

    Args:
        text: Texto a ser dividido
        max_chunk_size: Tamanho máximo aproximado de cada chunk
        overlap_sentences: Número de sentenças de overlap

    Returns:
        Lista de chunks
    """
    if not text or len(text) == 0:
        return []

    # Tokenizar em sentenças
    sentences = sent_tokenize(text)

    if len(sentences) == 0:
        return [{"chunk_text": text, "chunk_index": 0, "sentence_count": 1, "char_count": len(text)}]

    chunks = []
    current_chunk = []
    current_size = 0
    chunk_idx = 0

    for i, sentence in enumerate(sentences):
        sentence_size = len(sentence)

        # Se adicionar esta sentença ultrapassa o limite
        if current_size + sentence_size > max_chunk_size and current_chunk:
            # Salvar chunk atual
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                "chunk_text": chunk_text,
                "chunk_index": chunk_idx,
                "sentence_count": len(current_chunk),
                "char_count": len(chunk_text)
            })
            chunk_idx += 1

            # Overlap: manter últimas N sentenças
            current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
            current_size = sum(len(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_size += sentence_size

    # Último chunk
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append({
            "chunk_text": chunk_text,
            "chunk_index": chunk_idx,
            "sentence_count": len(current_chunk),
            "char_count": len(chunk_text)
        })

    return chunks

# Testar
test_text = "GRB 251208B was detected by Fermi GBM. The burst had a duration of 2.5 seconds. " * 20
test_chunks = chunk_by_sentences(test_text, max_chunk_size=300, overlap_sentences=1)
print(f"Texto de {len(test_text)} chars → {len(test_chunks)} chunks")
for i, c in enumerate(test_chunks[:2]):
    print(f"  Chunk {i}: {c['sentence_count']} sentenças, {c['char_count']} chars")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Estratégia 3: Semantic/Paragraph Chunking
# MAGIC
# MAGIC Chunking que respeita parágrafos e estrutura do documento.

# COMMAND ----------

# DBTITLE 1,Definir função de chunking por parágrafos
import re

def chunk_by_paragraphs(text: str, max_chunk_size: int = 800, min_paragraph_size: int = 50) -> List[Dict[str, Any]]:
    """
    Divide texto em chunks respeitando parágrafos.

    Args:
        text: Texto a ser dividido
        max_chunk_size: Tamanho máximo de cada chunk
        min_paragraph_size: Tamanho mínimo para considerar um parágrafo separado

    Returns:
        Lista de chunks
    """
    if not text or len(text) == 0:
        return []

    # Dividir por linhas duplas (parágrafos)
    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if len(paragraphs) == 0:
        return [{"chunk_text": text, "chunk_index": 0, "paragraph_count": 1, "char_count": len(text)}]

    chunks = []
    current_chunk = []
    current_size = 0
    chunk_idx = 0

    for para in paragraphs:
        para_size = len(para)

        # Parágrafo muito pequeno? Juntar com o anterior
        if para_size < min_paragraph_size and current_chunk:
            current_chunk.append(para)
            current_size += para_size
            continue

        # Se adicionar ultrapassa o limite
        if current_size + para_size > max_chunk_size and current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            chunks.append({
                "chunk_text": chunk_text,
                "chunk_index": chunk_idx,
                "paragraph_count": len(current_chunk),
                "char_count": len(chunk_text)
            })
            chunk_idx += 1
            current_chunk = []
            current_size = 0

        current_chunk.append(para)
        current_size += para_size

    # Último chunk
    if current_chunk:
        chunk_text = '\n\n'.join(current_chunk)
        chunks.append({
            "chunk_text": chunk_text,
            "chunk_index": chunk_idx,
            "paragraph_count": len(current_chunk),
            "char_count": len(chunk_text)
        })

    return chunks

# Testar
test_text = """GRB 251208B was detected by Fermi GBM on December 8, 2025 at 14:32:15 UT.

The burst showed a complex light curve with multiple peaks. The T90 duration was measured at 2.5 seconds, classifying it as a short GRB.

Follow-up observations were conducted with Swift XRT starting at T+300 seconds. An X-ray afterglow was detected at coordinates RA=123.456, Dec=-45.678.

Optical observations from NOT revealed a fading counterpart with magnitude r=21.5 at T+2 hours."""

test_chunks = chunk_by_paragraphs(test_text, max_chunk_size=400)
print(f"Texto de {len(test_text)} chars → {len(test_chunks)} chunks")
for i, c in enumerate(test_chunks):
    print(f"  Chunk {i}: {c['paragraph_count']} parágrafos, {c['char_count']} chars")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Aplicar Chunking ao Dataset

# COMMAND ----------

# DBTITLE 1,Definir UDF para chunking
# Schema para os chunks
chunk_schema = ArrayType(StructType([
    StructField("chunk_text", StringType(), True),
    StructField("chunk_index", IntegerType(), True),
    StructField("char_count", IntegerType(), True)
]))

# UDF para chunking por sentenças (melhor para textos científicos)
@udf(returnType=chunk_schema)
def sentence_chunk_udf(text: str) -> List[Dict]:
    if not text:
        return []
    chunks = chunk_by_sentences(text, max_chunk_size=500, overlap_sentences=1)
    return [{"chunk_text": c["chunk_text"], "chunk_index": c["chunk_index"], "char_count": c["char_count"]}
            for c in chunks]

# COMMAND ----------

# DBTITLE 1,Aplicar chunking
from pyspark.sql.functions import posexplode

# Aplicar chunking
df_chunked = df_prepared.withColumn(
    "chunks", sentence_chunk_udf(col("body"))
)

# Explodir chunks em linhas separadas
df_exploded = df_chunked.select(
    col("circular_id"),
    col("event_id"),
    col("subject"),
    col("created_on"),
    posexplode(col("chunks")).alias("chunk_index", "chunk")
).select(
    col("circular_id"),
    col("event_id"),
    col("subject"),
    col("created_on"),
    col("chunk_index"),
    col("chunk.chunk_text").alias("chunk_text"),
    col("chunk.char_count").alias("chunk_char_count")
)

# Adicionar ID único para cada chunk
df_final = df_exploded.withColumn(
    "chunk_id",
    concat_ws("_", col("circular_id").cast("string"), col("chunk_index").cast("string"))
)

# Mostrar resultado
print("📄 Resultado do chunking:")
df_final.select("chunk_id", "circular_id", "event_id", "chunk_index", "chunk_char_count").show(10)

# COMMAND ----------

# DBTITLE 1,Estatísticas de chunking
# Estatísticas
chunk_stats = df_final.agg({
    "*": "count",
    "chunk_char_count": "avg",
    "chunk_char_count": "min",
    "chunk_char_count": "max"
}).collect()[0]

chunks_per_doc = df_final.groupBy("circular_id").count()
avg_chunks = chunks_per_doc.agg({"count": "avg"}).collect()[0][0]
max_chunks = chunks_per_doc.agg({"count": "max"}).collect()[0][0]

print(f"""
📊 Estatísticas de Chunking:
────────────────────────────
Total de chunks:           {df_final.count():,}
Documentos originais:      {df_prepared.count():,}
Média de chunks/doc:       {avg_chunks:.1f}
Máximo de chunks em 1 doc: {max_chunks}

Tamanho dos chunks:
  - Mínimo: {df_final.agg({'chunk_char_count': 'min'}).collect()[0][0]:,} chars
  - Médio:  {df_final.agg({'chunk_char_count': 'avg'}).collect()[0][0]:,.0f} chars
  - Máximo: {df_final.agg({'chunk_char_count': 'max'}).collect()[0][0]:,} chars
""")

# COMMAND ----------

# DBTITLE 1,Distribuição de tamanho dos chunks
from pyspark.sql.functions import when

# Categorizar chunks por tamanho
df_size_dist = df_final.withColumn(
    "size_bucket",
    when(col("chunk_char_count") < 200, "tiny (<200)")
    .when(col("chunk_char_count") < 400, "small (200-400)")
    .when(col("chunk_char_count") < 600, "medium (400-600)")
    .when(col("chunk_char_count") < 800, "large (600-800)")
    .otherwise("very_large (800+)")
)

print("📏 Distribuição de tamanho dos chunks:")
df_size_dist.groupBy("size_bucket").count().orderBy("size_bucket").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Salvar Chunks

# COMMAND ----------

# DBTITLE 1,Salvar tabela de chunks
# Criar documento formatado para embedding (incluindo metadados)
df_to_save = df_final.withColumn(
    "document_for_embedding",
    concat_ws(
        "\n",
        concat_ws(": ", lit("EVENT"), col("event_id")),
        concat_ws(": ", lit("SUBJECT"), col("subject")),
        lit("---"),
        col("chunk_text")
    )
)

# Salvar
TABLE_NAME = "gcn_circulars_chunks"

df_to_save.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(TABLE_NAME)

saved_count = spark.table(TABLE_NAME).count()
print(f"✅ Tabela {CATALOG}.{SCHEMA}.{TABLE_NAME} criada com {saved_count:,} chunks")

# COMMAND ----------

# DBTITLE 1,Verificar tabela salva
# Mostrar exemplos
print("📄 Exemplos de chunks salvos:")
spark.table(TABLE_NAME).select(
    "chunk_id", "event_id", "chunk_index", "chunk_char_count", "document_for_embedding"
).show(5, truncate=100)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Estimativa de Tokens (para custo de embedding)

# COMMAND ----------

# DBTITLE 1,Calcular tokens estimados
# Usar tiktoken para estimativa mais precisa
encoding = tiktoken.get_encoding("cl100k_base")  # Encoding usado pelo OpenAI/BGE

# Sample para estimativa
sample_chunks = spark.table(TABLE_NAME).select("chunk_text").limit(1000).collect()
total_tokens = sum(len(encoding.encode(row.chunk_text)) for row in sample_chunks)
avg_tokens = total_tokens / len(sample_chunks)

total_chunks = spark.table(TABLE_NAME).count()
estimated_total_tokens = avg_tokens * total_chunks

print(f"""
🎯 Estimativa de Tokens:
────────────────────────
Sample size:              {len(sample_chunks):,} chunks
Média tokens/chunk:       {avg_tokens:.0f}
Total de chunks:          {total_chunks:,}
Tokens estimados (total): {estimated_total_tokens:,.0f}

💰 Custo estimado de embedding (databricks-bge-large-en):
   ~$0.0001 por 1K tokens
   Custo estimado: ${estimated_total_tokens/1000 * 0.0001:.2f}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos Passos
# MAGIC
# MAGIC ✅ Chunks criados e salvos
# MAGIC ➡️ Próximo notebook: `03-embeddings-vector-search.py`
# MAGIC    - Gerar embeddings com modelo BGE
# MAGIC    - Criar índice Vector Search
# MAGIC    - Testar retrieval
