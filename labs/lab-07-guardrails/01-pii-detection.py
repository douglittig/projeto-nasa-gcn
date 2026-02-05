# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 7.1: PII Detection in GCN Circulars
# MAGIC
# MAGIC Este notebook implementa detecção de PII (Personally Identifiable Information) nos GCN Circulars.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Identificar tipos de PII presentes nos dados
# MAGIC 2. Implementar detecção com regex e NER
# MAGIC 3. Criar pipeline de scanning
# MAGIC 4. Gerar relatório de PII encontrado
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 6: Governance (16%)
# MAGIC - Identify PII in unstructured data
# MAGIC - Implement data scanning for sensitive information

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install presidio-analyzer presidio-anonymizer spacy -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports e configuração
import re
from typing import List, Dict, Tuple
from pyspark.sql.functions import col, udf, explode, lit, array
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Identificar Tipos de PII nos GCN Circulars

# COMMAND ----------

# DBTITLE 1,Analisar amostra dos dados
# Carregar amostra de circulars
df_sample = spark.table("gcn_circulars").limit(100)

# Mostrar estrutura
print("📋 Campos disponíveis:")
df_sample.printSchema()

# Exemplo de submitter (principal fonte de PII)
print("\n📧 Exemplos de submitter:")
df_sample.select("submitter").distinct().show(10, truncate=False)

# COMMAND ----------

# DBTITLE 1,Tipos de PII esperados nos GCN Circulars
PII_TYPES = {
    "EMAIL": {
        "description": "Endereços de email dos astrônomos",
        "example": "astronomer@university.edu",
        "risk": "Medium",
        "fields": ["submitter", "body"]
    },
    "PERSON_NAME": {
        "description": "Nomes de pesquisadores",
        "example": "A. von Kienlin, J. Smith",
        "risk": "Low",
        "fields": ["submitter", "body"]
    },
    "INSTITUTION": {
        "description": "Afiliações institucionais",
        "example": "MPE, Caltech, NASA",
        "risk": "Low",
        "fields": ["submitter", "body"]
    },
    "PHONE": {
        "description": "Números de telefone (raro)",
        "example": "+1-555-123-4567",
        "risk": "High",
        "fields": ["body"]
    }
}

print("📋 Tipos de PII nos GCN Circulars:")
for pii_type, info in PII_TYPES.items():
    print(f"\n  {pii_type}:")
    print(f"    Descrição: {info['description']}")
    print(f"    Exemplo: {info['example']}")
    print(f"    Risco: {info['risk']}")
    print(f"    Campos: {', '.join(info['fields'])}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Detecção com Regex

# COMMAND ----------

# DBTITLE 1,Padrões regex para PII
# Padrões de detecção
PII_PATTERNS = {
    "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "PHONE_US": r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    "PHONE_INTL": r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
    "URL": r'https?://[^\s<>"{}|\\^`\[\]]+',
    "INSTITUTION_EMAIL_DOMAIN": r'@([\w-]+\.)*?(edu|ac\.[a-z]{2}|gov|org)\b'
}

def detect_pii_regex(text: str) -> List[Dict]:
    """
    Detecta PII usando regex.

    Args:
        text: Texto para analisar

    Returns:
        Lista de PII encontrados
    """
    if not text:
        return []

    findings = []

    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            findings.append({
                "type": pii_type,
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

    return findings


# Testar
test_text = """
A. von Kienlin at MPE <azk@mpe.mpg.de> reports on behalf of the Fermi GBM team:
For more information, contact support@nasa.gov or call +1-301-555-1234.
"""

findings = detect_pii_regex(test_text)
print("🔍 PII encontrado no texto de teste:")
for f in findings:
    print(f"   {f['type']}: '{f['value']}'")

# COMMAND ----------

# DBTITLE 1,Aplicar detecção ao dataset
# Schema para resultados
pii_schema = ArrayType(StructType([
    StructField("type", StringType(), True),
    StructField("value", StringType(), True),
    StructField("start", IntegerType(), True),
    StructField("end", IntegerType(), True)
]))

# UDF para detecção
@udf(returnType=pii_schema)
def detect_pii_udf(text: str) -> List[Dict]:
    return detect_pii_regex(text) if text else []

# Aplicar ao submitter field
df_pii = df_sample.withColumn(
    "pii_findings",
    detect_pii_udf(col("submitter"))
)

# Contar findings
print("📊 Resultados da detecção no campo 'submitter':")
df_pii.select(
    "circular_id",
    "submitter",
    "pii_findings"
).filter("size(pii_findings) > 0").show(5, truncate=60)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Detecção com Presidio (NER)

# COMMAND ----------

# DBTITLE 1,Configurar Presidio Analyzer
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern

# Inicializar analyzer
analyzer = AnalyzerEngine()

# Adicionar reconhecedor customizado para instituições
institution_patterns = [
    Pattern("INSTITUTION_PATTERN", r"\b(MPE|Caltech|NASA|ESA|MIT|Stanford|Harvard|Berkeley)\b", 0.7),
    Pattern("OBSERVATORY_PATTERN", r"\b[\w\s]*(Observatory|Institute|Laboratory|Center)\b", 0.6)
]

institution_recognizer = PatternRecognizer(
    supported_entity="INSTITUTION",
    patterns=institution_patterns
)
analyzer.registry.add_recognizer(institution_recognizer)

print("✅ Presidio Analyzer configurado com reconhecedores customizados")

# COMMAND ----------

# DBTITLE 1,Função de análise com Presidio
def analyze_with_presidio(text: str, language: str = "en") -> List[Dict]:
    """
    Analisa texto com Presidio para detecção de PII.

    Args:
        text: Texto para analisar
        language: Idioma do texto

    Returns:
        Lista de entidades PII encontradas
    """
    if not text:
        return []

    try:
        results = analyzer.analyze(
            text=text,
            language=language,
            entities=["EMAIL_ADDRESS", "PERSON", "PHONE_NUMBER", "URL", "INSTITUTION"]
        )

        findings = []
        for result in results:
            findings.append({
                "type": result.entity_type,
                "value": text[result.start:result.end],
                "start": result.start,
                "end": result.end,
                "score": result.score
            })

        return findings
    except Exception as e:
        return [{"type": "ERROR", "value": str(e), "start": 0, "end": 0, "score": 0}]


# Testar
presidio_findings = analyze_with_presidio(test_text)
print("🔍 PII encontrado com Presidio:")
for f in presidio_findings:
    print(f"   {f['type']}: '{f['value']}' (score: {f.get('score', 'N/A')})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Scanning Completo do Dataset

# COMMAND ----------

# DBTITLE 1,Função de scanning combinado
def comprehensive_pii_scan(text: str) -> Dict:
    """
    Realiza scanning completo de PII combinando métodos.

    Args:
        text: Texto para analisar

    Returns:
        Dict com resultados do scanning
    """
    if not text:
        return {"total_findings": 0, "findings": []}

    # Regex findings
    regex_results = detect_pii_regex(text)

    # Presidio findings
    presidio_results = analyze_with_presidio(text)

    # Combinar e deduplicar
    all_findings = []
    seen_values = set()

    for f in regex_results + presidio_results:
        value = f.get("value", "")
        if value and value not in seen_values:
            seen_values.add(value)
            all_findings.append(f)

    return {
        "total_findings": len(all_findings),
        "findings": all_findings,
        "has_email": any(f["type"] in ["EMAIL", "EMAIL_ADDRESS"] for f in all_findings),
        "has_phone": any(f["type"] in ["PHONE_US", "PHONE_INTL", "PHONE_NUMBER"] for f in all_findings),
        "has_person": any(f["type"] == "PERSON" for f in all_findings)
    }


# Testar
scan_result = comprehensive_pii_scan(test_text)
print(f"📊 Scan completo: {scan_result['total_findings']} findings")
print(f"   Has email: {scan_result['has_email']}")
print(f"   Has phone: {scan_result['has_phone']}")
print(f"   Has person: {scan_result['has_person']}")

# COMMAND ----------

# DBTITLE 1,Aplicar scanning ao dataset completo
# Carregar dataset completo (limitado para demo)
df_full = spark.table("gcn_circulars").limit(1000)

# Coletar para processar localmente (em produção, usar UDF distribuído)
sample_data = df_full.select("circular_id", "submitter", "body").collect()

# Scanning
scan_results = []
for row in sample_data[:100]:  # Limitar para demo
    submitter_scan = comprehensive_pii_scan(row.submitter)
    body_scan = comprehensive_pii_scan(row.body[:1000] if row.body else "")  # Primeiros 1000 chars

    scan_results.append({
        "circular_id": row.circular_id,
        "submitter_pii_count": submitter_scan["total_findings"],
        "body_pii_count": body_scan["total_findings"],
        "has_email": submitter_scan["has_email"] or body_scan["has_email"],
        "has_phone": submitter_scan["has_phone"] or body_scan["has_phone"],
        "sample_findings": str(submitter_scan["findings"][:3])
    })

# Criar DataFrame
import pandas as pd
scan_df = spark.createDataFrame(pd.DataFrame(scan_results))

print("📊 Resultados do scanning:")
scan_df.show(10, truncate=60)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Relatório de PII

# COMMAND ----------

# DBTITLE 1,Gerar relatório agregado
# Estatísticas
total_docs = len(scan_results)
docs_with_email = sum(1 for r in scan_results if r["has_email"])
docs_with_phone = sum(1 for r in scan_results if r["has_phone"])
total_pii = sum(r["submitter_pii_count"] + r["body_pii_count"] for r in scan_results)

print(f"""
╔══════════════════════════════════════════════════════════════╗
║              PII Scanning Report - GCN Circulars             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Documents scanned:     {total_docs:>6,}                            ║
║  Total PII findings:    {total_pii:>6,}                            ║
║                                                              ║
║  Documents with:                                             ║
║    - Email addresses:   {docs_with_email:>6,} ({docs_with_email/total_docs*100:.1f}%)                   ║
║    - Phone numbers:     {docs_with_phone:>6,} ({docs_with_phone/total_docs*100:.1f}%)                    ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Risk Assessment:                                            ║
║    - Email exposure: MEDIUM (common in scientific papers)    ║
║    - Phone exposure: LOW (rare in circulars)                 ║
║    - Name exposure: LOW (public information)                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# DBTITLE 1,Salvar resultados
# Salvar resultados do scanning
scan_df.write.mode("overwrite").saveAsTable("pii_scan_results")

print("✅ Resultados salvos em 'pii_scan_results'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Tipos de PII Detectados:
# MAGIC
# MAGIC | Tipo | Método | Prevalência |
# MAGIC |------|--------|-------------|
# MAGIC | Email | Regex + Presidio | Alta |
# MAGIC | Person Name | Presidio NER | Média |
# MAGIC | Institution | Custom Pattern | Alta |
# MAGIC | Phone | Regex | Baixa |
# MAGIC
# MAGIC ### Próximo Notebook: 02-masking.py
# MAGIC
# MAGIC No próximo notebook, implementaremos masking do PII detectado.
