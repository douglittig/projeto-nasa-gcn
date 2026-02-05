# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 3.2: Chunking Strategies for RAG
# MAGIC
# MAGIC Este notebook implementa diferentes estratégias de chunking para os GCN Circulars,
# MAGIC seguindo as melhores práticas dos labs oficiais da Databricks.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Implementar chunking por caracteres (simples)
# MAGIC 2. Implementar chunking por sentenças (regex - compatível com serverless)
# MAGIC 3. Implementar chunking semântico (parágrafos)
# MAGIC 4. **Comparar estratégias COM vs SEM overlap** e avaliar trade-offs
# MAGIC 5. **Analisar impacto do tamanho do chunk** na qualidade do retrieval
# MAGIC 6. Aplicar chunking ao dataset e salvar em Delta Lake
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 2: Data Preparation (14%)
# MAGIC   - Apply chunking strategy for document structure and model constraints
# MAGIC   - Design retrieval systems using advanced chunking strategies
# MAGIC   - Evaluate how chunk size and overlap affect retrieval precision

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install tiktoken -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports e configuração
import re
import tiktoken
from typing import List, Dict, Any
from pyspark.sql.functions import (
    col, udf, explode, lit, length,
    monotonically_increasing_id, concat_ws, size, array
)
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

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
# MAGIC ## 2. Estratégia 2: Sentence-based Chunking (Regex)
# MAGIC
# MAGIC Chunking inteligente que respeita limites de sentenças.
# MAGIC
# MAGIC > **Nota:** Usamos regex ao invés de NLTK para compatibilidade com clusters serverless.
# MAGIC > NLTK requer download de dados que não ficam disponíveis nos workers do Spark.

# COMMAND ----------

# DBTITLE 1,Definir função de chunking por sentenças
# Nota: Usamos regex ao invés de NLTK para compatibilidade com clusters serverless
# NLTK requer download de dados que não ficam disponíveis nos workers

def simple_sent_tokenize(text: str) -> List[str]:
    """
    Tokenizador de sentenças simples usando regex.
    Compatível com clusters serverless (não requer NLTK).

    Funciona bem para textos científicos em inglês como GCN Circulars.
    """
    # Proteger abreviações comuns substituindo temporariamente
    abbreviations = ['Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.', 'Fig.', 'Tab.', 'Eq.', 'et al.', 'i.e.', 'e.g.', 'vs.', 'etc.']
    protected = text
    for i, abbr in enumerate(abbreviations):
        protected = protected.replace(abbr, f"__ABBR{i}__")

    # Dividir em sentenças: . ! ? seguido de espaço e letra maiúscula
    sentences = re.split(r'([.!?]) +(?=[A-Z])', protected)

    # Recombinar pontuação com a sentença anterior
    result = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
            result.append(sentences[i] + sentences[i + 1])
            i += 2
        else:
            result.append(sentences[i])
            i += 1

    # Restaurar abreviações
    final = []
    for sent in result:
        restored = sent
        for i, abbr in enumerate(abbreviations):
            restored = restored.replace(f"__ABBR{i}__", abbr)
        if restored.strip():
            final.append(restored.strip())

    return final


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

    # Tokenizar em sentenças (usando regex, compatível com serverless)
    sentences = simple_sent_tokenize(text)

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
# IMPORTANTE: Todo o código deve estar inline no UDF para funcionar em clusters serverless
@udf(returnType=chunk_schema)
def sentence_chunk_udf(text: str) -> List[Dict]:
    """
    UDF que aplica chunking por sentenças.
    Código inline para compatibilidade com serverless.
    """
    import re
    from typing import List, Dict, Any

    def _sent_tokenize(text: str) -> List[str]:
        """Tokenizador de sentenças usando regex."""
        # Proteger abreviações comuns
        abbreviations = ['Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.', 'Fig.', 'Tab.', 'Eq.', 'et al.', 'i.e.', 'e.g.', 'vs.', 'etc.']
        protected = text
        for i, abbr in enumerate(abbreviations):
            protected = protected.replace(abbr, f"__ABBR{i}__")

        # Dividir em sentenças
        sentences = re.split(r'([.!?]) +(?=[A-Z])', protected)

        # Recombinar pontuação
        result = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
                result.append(sentences[i] + sentences[i + 1])
                i += 2
            else:
                result.append(sentences[i])
                i += 1

        # Restaurar abreviações
        final = []
        for sent in result:
            restored = sent
            for i, abbr in enumerate(abbreviations):
                restored = restored.replace(f"__ABBR{i}__", abbr)
            if restored.strip():
                final.append(restored.strip())

        return final

    def _chunk_by_sentences(text: str, max_chunk_size: int = 500, overlap_sentences: int = 1) -> List[Dict[str, Any]]:
        if not text or len(text) == 0:
            return []

        sentences = _sent_tokenize(text)

        if len(sentences) == 0:
            return [{"chunk_text": text, "chunk_index": 0, "sentence_count": 1, "char_count": len(text)}]

        chunks = []
        current_chunk = []
        current_size = 0
        chunk_idx = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            if current_size + sentence_size > max_chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    "chunk_text": chunk_text,
                    "chunk_index": chunk_idx,
                    "sentence_count": len(current_chunk),
                    "char_count": len(chunk_text)
                })
                chunk_idx += 1
                current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
                current_size = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_size += sentence_size

        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                "chunk_text": chunk_text,
                "chunk_index": chunk_idx,
                "sentence_count": len(current_chunk),
                "char_count": len(chunk_text)
            })

        return chunks

    # Executar chunking
    if not text:
        return []
    chunks = _chunk_by_sentences(text, max_chunk_size=500, overlap_sentences=1)
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
# MAGIC ## 7. Comparar Estratégias: Com vs Sem Overlap
# MAGIC
# MAGIC Uma das decisões mais importantes no chunking é o **overlap** (sobreposição).
# MAGIC Vamos comparar os resultados para entender o impacto.
# MAGIC
# MAGIC ### 🎯 Por que Overlap Importa?
# MAGIC
# MAGIC **Sem overlap:**
# MAGIC ```
# MAGIC Chunk 1: "...the burst was detected at T0."
# MAGIC Chunk 2: "Follow-up observations started at T+300s."
# MAGIC ```
# MAGIC Uma query sobre "when did observations start after detection" pode perder o contexto.
# MAGIC
# MAGIC **Com overlap:**
# MAGIC ```
# MAGIC Chunk 1: "...the burst was detected at T0. Follow-up observations..."
# MAGIC Chunk 2: "...detected at T0. Follow-up observations started at T+300s."
# MAGIC ```
# MAGIC Ambos os chunks contêm o contexto completo!

# COMMAND ----------

# DBTITLE 1,Criar chunks SEM overlap para comparação
def chunk_by_sentences_no_overlap(text: str, max_chunk_size: int = 500) -> List[Dict[str, Any]]:
    """Chunking por sentenças SEM overlap."""
    if not text or len(text) == 0:
        return []

    sentences = simple_sent_tokenize(text)
    if len(sentences) == 0:
        return [{"chunk_text": text, "chunk_index": 0, "char_count": len(text)}]

    chunks = []
    current_chunk = []
    current_size = 0
    chunk_idx = 0

    for sentence in sentences:
        sentence_size = len(sentence)

        if current_size + sentence_size > max_chunk_size and current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                "chunk_text": chunk_text,
                "chunk_index": chunk_idx,
                "char_count": len(chunk_text)
            })
            chunk_idx += 1
            current_chunk = []  # SEM overlap
            current_size = 0

        current_chunk.append(sentence)
        current_size += sentence_size

    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append({
            "chunk_text": chunk_text,
            "chunk_index": chunk_idx,
            "char_count": len(chunk_text)
        })

    return chunks

# Comparar com um documento de exemplo
sample_doc = df_prepared.select("body").limit(1).collect()[0][0]

chunks_with_overlap = chunk_by_sentences(sample_doc, max_chunk_size=500, overlap_sentences=1)
chunks_no_overlap = chunk_by_sentences_no_overlap(sample_doc, max_chunk_size=500)

print(f"""
🔬 Comparação de Overlap:
─────────────────────────
Documento original: {len(sample_doc):,} caracteres

COM overlap (1 sentença):
  - Total chunks: {len(chunks_with_overlap)}
  - Chars total: {sum(c['char_count'] for c in chunks_with_overlap):,}
  - Redundância: {sum(c['char_count'] for c in chunks_with_overlap) - len(sample_doc):,} chars extras

SEM overlap:
  - Total chunks: {len(chunks_no_overlap)}
  - Chars total: {sum(c['char_count'] for c in chunks_no_overlap):,}
  - Redundância: ~0 chars
""")

# COMMAND ----------

# DBTITLE 1,Visualizar diferença de overlap
# Mostrar as bordas dos chunks para ver o overlap
print("📋 Primeiros 3 chunks COM overlap:")
print("=" * 80)
for i, chunk in enumerate(chunks_with_overlap[:3]):
    print(f"\nChunk {i} ({chunk['char_count']} chars):")
    # Mostrar início e fim
    text = chunk['chunk_text']
    print(f"  Início: '{text[:80]}...'")
    print(f"  Fim:    '...{text[-80:]}'")

print("\n\n📋 Primeiros 3 chunks SEM overlap:")
print("=" * 80)
for i, chunk in enumerate(chunks_no_overlap[:3]):
    print(f"\nChunk {i} ({chunk['char_count']} chars):")
    text = chunk['chunk_text']
    print(f"  Início: '{text[:80]}...'")
    print(f"  Fim:    '...{text[-80:]}'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Avaliar Impacto do Tamanho do Chunk
# MAGIC
# MAGIC O tamanho do chunk afeta diretamente a qualidade do retrieval:
# MAGIC
# MAGIC | Tamanho | Prós | Contras |
# MAGIC |---------|------|---------|
# MAGIC | **Pequeno** (100-200 chars) | Alta precisão, foco | Pode perder contexto |
# MAGIC | **Médio** (300-500 chars) | Bom equilíbrio | Escolha mais comum |
# MAGIC | **Grande** (600-1000 chars) | Mais contexto | Menor precisão, dilui relevância |
# MAGIC
# MAGIC ### 🎯 Recomendações por Caso de Uso:
# MAGIC
# MAGIC - **FAQ / Perguntas diretas**: Chunks menores (200-300)
# MAGIC - **Documentos técnicos**: Chunks médios (400-600)
# MAGIC - **Artigos científicos**: Chunks maiores (600-800)

# COMMAND ----------

# DBTITLE 1,Testar diferentes tamanhos de chunk
chunk_sizes = [200, 400, 600, 800]
results = []

for size in chunk_sizes:
    chunks = chunk_by_sentences(sample_doc, max_chunk_size=size, overlap_sentences=1)
    total_chars = sum(c['char_count'] for c in chunks)
    avg_chars = total_chars / len(chunks) if chunks else 0

    results.append({
        "max_size": size,
        "num_chunks": len(chunks),
        "avg_chunk_size": avg_chars,
        "total_chars": total_chars,
        "overhead_pct": ((total_chars - len(sample_doc)) / len(sample_doc)) * 100
    })

print("📊 Impacto do Tamanho do Chunk:")
print("=" * 80)
print(f"{'Max Size':<12} {'Chunks':<10} {'Avg Size':<12} {'Total':<12} {'Overhead %':<12}")
print("-" * 80)
for r in results:
    print(f"{r['max_size']:<12} {r['num_chunks']:<10} {r['avg_chunk_size']:<12.0f} {r['total_chars']:<12,} {r['overhead_pct']:<12.1f}")

# COMMAND ----------

# DBTITLE 1,Análise de trade-offs
print("""
📈 Análise de Trade-offs:
═════════════════════════

1. CHUNKS PEQUENOS (200-300 chars):
   ✅ Alta precisão no retrieval
   ✅ Menos tokens por chunk = menor custo de LLM
   ❌ Pode fragmentar informação relacionada
   ❌ Mais chunks = mais chamadas de embedding

2. CHUNKS MÉDIOS (400-600 chars):
   ✅ Bom equilíbrio entre precisão e contexto
   ✅ Adequado para a maioria dos casos
   ✅ Tamanho típico de 1-3 sentenças completas
   → RECOMENDADO para GCN Circulars

3. CHUNKS GRANDES (800+ chars):
   ✅ Contexto rico para respostas complexas
   ❌ Menor precisão (dilui relevância)
   ❌ Mais tokens = maior custo de LLM
   ❌ Pode incluir informação irrelevante

💡 Nossa Escolha: 500 chars com overlap de 1 sentença
   - Preserva contexto científico
   - Compatível com limite de tokens do embedding model
   - Overlap garante continuidade semântica
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Conceitos-Chave para o Exame
# MAGIC
# MAGIC ### 📚 Chunking Strategies (Section 2: Data Preparation - 14%)
# MAGIC
# MAGIC | Estratégia | Quando Usar | Trade-off |
# MAGIC |------------|-------------|-----------|
# MAGIC | **Fixed-size** | Documentos uniformes | Simples, mas pode cortar contexto |
# MAGIC | **Sentence-based** | Textos em prosa | Preserva semântica, overhead moderado |
# MAGIC | **Paragraph-based** | Docs estruturados | Respeita estrutura, chunks variáveis |
# MAGIC | **Semantic** | Docs complexos | Melhor qualidade, mais complexo |
# MAGIC
# MAGIC ### 🎯 Exam Tips:
# MAGIC
# MAGIC 1. **Overlap** previne perda de contexto nas bordas dos chunks
# MAGIC 2. **Chunk size** deve considerar:
# MAGIC    - Limite de tokens do embedding model (tipicamente 512)
# MAGIC    - Janela de contexto do LLM
# MAGIC    - Custo de embedding e inferência
# MAGIC 3. **Metadata enrichment** melhora retrieval (source, date, section)
# MAGIC 4. **Delta Lake** é preferido para armazenar chunks (ACID, versioning)

# COMMAND ----------

# DBTITLE 1,Resumo das decisões de chunking
print("""
📋 Resumo: Decisões de Chunking para GCN Circulars
═══════════════════════════════════════════════════

┌─────────────────────┬────────────────────────────────────────┐
│ Parâmetro           │ Valor Escolhido                        │
├─────────────────────┼────────────────────────────────────────┤
│ Estratégia          │ Sentence-based (regex)                 │
│ Max chunk size      │ 500 caracteres (~125 tokens)           │
│ Overlap             │ 1 sentença                             │
│ Min doc size        │ 100 caracteres (filtrado antes)        │
│ Metadata incluído   │ event_id, subject, created_on          │
│ Storage             │ Delta Lake (Unity Catalog)             │
└─────────────────────┴────────────────────────────────────────┘

Justificativas:
1. Sentence-based preserva contexto científico dos GCN Circulars
2. 500 chars é compatível com embeddings BGE (max 512 tokens)
3. Overlap de 1 sentença previne perda de contexto
4. Regex usado ao invés de NLTK para compatibilidade serverless
5. Metadata enriquece retrieval com informações do evento
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Lab Wrap-Up: Key Learnings
# MAGIC
# MAGIC ### ✅ O que você aprendeu:
# MAGIC
# MAGIC | Etapa | Conceito | Aplicação |
# MAGIC |-------|----------|-----------|
# MAGIC | **Chunking por caracteres** | Divisão simples com overlap | Baseline, documentos uniformes |
# MAGIC | **Chunking por sentenças** | Respeita limites semânticos | Textos científicos, prosa |
# MAGIC | **Chunking por parágrafos** | Preserva estrutura do documento | Docs com seções claras |
# MAGIC | **Comparação de overlap** | Trade-off redundância vs contexto | Decisão de design |
# MAGIC | **Análise de chunk size** | Impacto em precisão e custo | Otimização |
# MAGIC
# MAGIC ### 🧠 Insights Críticos:
# MAGIC
# MAGIC 1. **Qualidade > Quantidade**: Chunks bem estruturados superam volume
# MAGIC 2. **Overlap é essencial**: Previne perda de contexto em bordas
# MAGIC 3. **Tamanho importa**: Muito pequeno fragmenta, muito grande dilui
# MAGIC 4. **Metadata enriquece**: Source, date, section melhoram retrieval
# MAGIC 5. **Serverless requer adaptação**: NLTK não funciona, regex sim
# MAGIC
# MAGIC ### 🚀 Próximos Passos:
# MAGIC
# MAGIC 1. **Embeddings**: Gerar vetores com BGE model
# MAGIC 2. **Vector Search**: Criar índice para retrieval
# MAGIC 3. **RAG Chain**: Conectar retriever ao LLM
# MAGIC 4. **Avaliação**: Medir qualidade do retrieval

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos Passos
# MAGIC
# MAGIC ✅ Chunks criados e salvos
# MAGIC ➡️ Próximo notebook: `03-embeddings-vector-search.py`
# MAGIC    - Gerar embeddings com modelo BGE
# MAGIC    - Criar índice Vector Search
# MAGIC    - Testar retrieval
