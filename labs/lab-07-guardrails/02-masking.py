# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 7.2: PII Masking and Anonymization
# MAGIC
# MAGIC Este notebook implementa masking de PII para proteger dados sensíveis.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Implementar estratégias de masking
# MAGIC 2. Aplicar anonymization com Presidio
# MAGIC 3. Criar versão anonymizada do dataset
# MAGIC 4. Validar que PII foi removido
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 6: Governance (16%)
# MAGIC - Implement data anonymization
# MAGIC - Apply masking strategies for PII protection

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install presidio-analyzer presidio-anonymizer -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports
import re
from typing import Dict
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Estratégias de Masking

# COMMAND ----------

# DBTITLE 1,Definir estratégias
MASKING_STRATEGIES = {
    "REPLACE": {
        "description": "Substitui PII por placeholder",
        "example": "email@example.com → [EMAIL]",
        "use_case": "Logs, debugging"
    },
    "REDACT": {
        "description": "Remove PII completamente",
        "example": "email@example.com → ",
        "use_case": "Publicação, compartilhamento"
    },
    "HASH": {
        "description": "Substitui por hash",
        "example": "email@example.com → abc123...",
        "use_case": "Análise que preserva unicidade"
    },
    "MASK": {
        "description": "Mascara parcialmente",
        "example": "email@example.com → e***@e***.com",
        "use_case": "Visualização com contexto parcial"
    },
    "ENCRYPT": {
        "description": "Criptografa (reversível)",
        "example": "email@example.com → [encrypted]",
        "use_case": "Dados que precisam ser recuperados"
    }
}

print("📋 Estratégias de Masking Disponíveis:")
for strategy, info in MASKING_STRATEGIES.items():
    print(f"\n  {strategy}:")
    print(f"    {info['description']}")
    print(f"    Exemplo: {info['example']}")
    print(f"    Uso: {info['use_case']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Implementar Masking com Regex

# COMMAND ----------

# DBTITLE 1,Funções de masking com regex
def mask_email_replace(text: str) -> str:
    """Substitui emails por [EMAIL]."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(pattern, '[EMAIL]', text, flags=re.IGNORECASE)


def mask_email_partial(text: str) -> str:
    """Mascara emails parcialmente."""
    def partial_mask(match):
        email = match.group()
        local, domain = email.split('@')
        masked_local = local[0] + '*' * (len(local) - 1)
        domain_parts = domain.split('.')
        masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1)
        return f"{masked_local}@{masked_domain}.{domain_parts[-1]}"

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(pattern, partial_mask, text, flags=re.IGNORECASE)


def mask_phone(text: str) -> str:
    """Substitui telefones por [PHONE]."""
    patterns = [
        r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    ]
    for pattern in patterns:
        text = re.sub(pattern, '[PHONE]', text)
    return text


# Testar
test_text = "Contact A. Smith at asmith@university.edu or +1-555-123-4567 for details."

print("📝 Texto original:")
print(f"   {test_text}")
print("\n📝 Com masking:")
print(f"   Replace: {mask_email_replace(test_text)}")
print(f"   Partial: {mask_email_partial(test_text)}")
print(f"   Phone:   {mask_phone(test_text)}")

# COMMAND ----------

# DBTITLE 1,Função de masking combinado
def apply_all_masks(text: str, strategy: str = "replace") -> str:
    """
    Aplica todos os masks ao texto.

    Args:
        text: Texto para mascarar
        strategy: 'replace', 'partial', ou 'redact'

    Returns:
        Texto mascarado
    """
    if not text:
        return text

    if strategy == "replace":
        text = mask_email_replace(text)
        text = mask_phone(text)
    elif strategy == "partial":
        text = mask_email_partial(text)
        text = mask_phone(text)
    elif strategy == "redact":
        # Remove completamente
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text, flags=re.IGNORECASE)
        text = mask_phone(text)
        text = re.sub(r'<[^>]*>', '', text)  # Remove email em brackets
        text = re.sub(r'\s+', ' ', text)  # Normaliza espaços

    return text.strip()


# Testar todas as estratégias
gcn_example = "A. von Kienlin at MPE <azk@mpe.mpg.de> reports on behalf of the Fermi GBM team:"

print("📝 Exemplo GCN Circular:")
print(f"   Original: {gcn_example}")
print(f"   Replace:  {apply_all_masks(gcn_example, 'replace')}")
print(f"   Partial:  {apply_all_masks(gcn_example, 'partial')}")
print(f"   Redact:   {apply_all_masks(gcn_example, 'redact')}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Masking com Presidio

# COMMAND ----------

# DBTITLE 1,Configurar Presidio Anonymizer
# Inicializar engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Configurar operadores de anonymização
operators = {
    "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
    "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE]"}),
    "PERSON": OperatorConfig("replace", {"new_value": "[PERSON]"}),
    "URL": OperatorConfig("replace", {"new_value": "[URL]"}),
    "DEFAULT": OperatorConfig("replace", {"new_value": "[REDACTED]"})
}

print("✅ Presidio Anonymizer configurado")

# COMMAND ----------

# DBTITLE 1,Função de anonymização com Presidio
def anonymize_with_presidio(text: str, language: str = "en") -> Dict:
    """
    Anonymiza texto usando Presidio.

    Args:
        text: Texto para anonymizar
        language: Idioma do texto

    Returns:
        Dict com texto anonymizado e estatísticas
    """
    if not text:
        return {"anonymized_text": text, "entities_found": 0, "entities": []}

    try:
        # Analisar
        analysis_results = analyzer.analyze(
            text=text,
            language=language,
            entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "URL"]
        )

        # Anonymizar
        anonymized = anonymizer.anonymize(
            text=text,
            analyzer_results=analysis_results,
            operators=operators
        )

        return {
            "anonymized_text": anonymized.text,
            "entities_found": len(analysis_results),
            "entities": [r.entity_type for r in analysis_results]
        }

    except Exception as e:
        return {
            "anonymized_text": text,
            "entities_found": 0,
            "entities": [],
            "error": str(e)
        }


# Testar
result = anonymize_with_presidio(gcn_example)
print("📝 Presidio Anonymization:")
print(f"   Original:   {gcn_example}")
print(f"   Anonymized: {result['anonymized_text']}")
print(f"   Entities:   {result['entities']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Aplicar ao Dataset

# COMMAND ----------

# DBTITLE 1,Criar UDF para masking
# UDF para Spark
@udf(returnType=StringType())
def mask_pii_udf(text: str) -> str:
    """UDF para masking de PII."""
    return apply_all_masks(text, strategy="replace") if text else text

# COMMAND ----------

# DBTITLE 1,Aplicar masking ao dataset
# Carregar dados
df_original = spark.table("gcn_circulars").limit(1000)

# Aplicar masking
df_masked = df_original.withColumn(
    "submitter_masked",
    mask_pii_udf(col("submitter"))
).withColumn(
    "body_masked",
    mask_pii_udf(col("body"))
)

# Comparar
print("📊 Comparação Original vs Masked:")
df_masked.select(
    "circular_id",
    "submitter",
    "submitter_masked"
).show(5, truncate=60)

# COMMAND ----------

# DBTITLE 1,Criar tabela anonymizada
# Selecionar colunas para versão anonymizada
df_anonymized = df_masked.select(
    "circular_id",
    "event_id",
    "subject",
    col("submitter_masked").alias("submitter"),
    col("body_masked").alias("body"),
    "created_on"
)

# Salvar
df_anonymized.write.mode("overwrite").saveAsTable("gcn_circulars_anonymized")

print(f"✅ Tabela anonymizada criada: gcn_circulars_anonymized")
print(f"   Registros: {df_anonymized.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Validar Anonymização

# COMMAND ----------

# DBTITLE 1,Verificar que PII foi removido
# Verificar se ainda existem emails na versão anonymizada
df_check = spark.table("gcn_circulars_anonymized")

# Contar ocorrências de padrões de email
email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'

# Amostra
sample = df_check.select("submitter", "body").limit(100).collect()

emails_found = 0
for row in sample:
    if row.submitter and re.search(email_pattern, row.submitter, re.IGNORECASE):
        emails_found += 1
    if row.body and re.search(email_pattern, row.body[:500], re.IGNORECASE):
        emails_found += 1

print(f"""
╔══════════════════════════════════════════════════════════════╗
║            Validation Report - Anonymized Dataset            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Sample size:          100 records                           ║
║  Emails found:         {emails_found:>3} (should be 0)                     ║
║  Validation:           {'✅ PASSED' if emails_found == 0 else '❌ FAILED'}                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# DBTITLE 1,Comparação lado a lado
print("📊 Comparação Original vs Anonymized:\n")

# Pegar um exemplo
original = spark.table("gcn_circulars").filter("submitter IS NOT NULL").limit(1).collect()[0]
anonymized = spark.table("gcn_circulars_anonymized").filter(f"circular_id = {original.circular_id}").collect()[0]

print(f"Circular ID: {original.circular_id}")
print(f"\nOriginal submitter:")
print(f"  {original.submitter}")
print(f"\nAnonymized submitter:")
print(f"  {anonymized.submitter}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Estratégias Implementadas:
# MAGIC
# MAGIC | Estratégia | Implementação | Uso |
# MAGIC |------------|---------------|-----|
# MAGIC | Replace | Regex + Presidio | Padrão |
# MAGIC | Partial | Regex | Debug |
# MAGIC | Redact | Regex | Publicação |
# MAGIC
# MAGIC ### Tabelas Criadas:
# MAGIC
# MAGIC | Tabela | Descrição |
# MAGIC |--------|-----------|
# MAGIC | `gcn_circulars_anonymized` | Versão sem PII |
# MAGIC
# MAGIC ### Próximo Notebook: 03-prompt-protection.py
