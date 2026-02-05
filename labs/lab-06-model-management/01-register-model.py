# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 6.1: Registering Models in Unity Catalog
# MAGIC
# MAGIC Este notebook demonstra o registro e gerenciamento de modelos no Unity Catalog.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Registrar modelo no Unity Catalog
# MAGIC 2. Adicionar descrições e tags
# MAGIC 3. Configurar permissões
# MAGIC 4. Explorar model lineage
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 6: Governance (16%)
# MAGIC - Register models in Unity Catalog
# MAGIC - Configure model permissions and access control

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
import mlflow
from mlflow import MlflowClient
from mlflow.models import ModelVersion
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"
MODEL_SCHEMA = "nasa_gcn_models"

spark.sql(f"USE CATALOG {CATALOG}")

# Criar schema para modelos se não existir
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{MODEL_SCHEMA}")

# Model name
MODEL_NAME = f"{CATALOG}.{MODEL_SCHEMA}.gcn_rag_assistant"

print(f"""
⚙️ Configuração:
  - Catalog: {CATALOG}
  - Model Schema: {MODEL_SCHEMA}
  - Model Name: {MODEL_NAME}
""")

# COMMAND ----------

# DBTITLE 1,Initialize MLflow Client
client = MlflowClient()

# Set registry URI to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

print("✅ MLflow client initialized with Unity Catalog registry")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Verificar Modelo Existente

# COMMAND ----------

# DBTITLE 1,Listar versões do modelo
try:
    # Get model info
    model = client.get_registered_model(MODEL_NAME)

    print(f"📦 Model: {model.name}")
    print(f"   Description: {model.description[:100] if model.description else 'None'}...")
    print(f"   Creation time: {model.creation_timestamp}")
    print(f"   Last updated: {model.last_updated_timestamp}")

    # List versions
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    print(f"\n📋 Versions ({len(versions)}):")
    for v in versions:
        aliases = v.aliases if hasattr(v, 'aliases') else []
        print(f"   v{v.version}: {v.current_stage} | Aliases: {aliases}")

except Exception as e:
    print(f"⚠️ Model not found or error: {e}")
    print("   Run Lab 5 first to create the model")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Adicionar Metadados ao Modelo

# COMMAND ----------

# DBTITLE 1,Atualizar descrição do modelo
MODEL_DESCRIPTION = """
# NASA GCN RAG Assistant

A Retrieval-Augmented Generation model for answering questions about astronomical transient events using GCN Circulars as the knowledge base.

## Capabilities
- Answer questions about gamma-ray bursts (GRBs)
- Provide information on gravitational wave events
- Retrieve neutrino detection details from IceCube
- Include source citations (event_ids) for traceability

## Technical Details
- **Retriever**: Databricks Vector Search with BGE embeddings
- **LLM**: Llama 3.1 70B Instruct
- **Knowledge Base**: ~15,000 GCN Circulars

## Input/Output
- **Input**: Question string about astronomical events
- **Output**: JSON with answer, source citations, and document count

## Usage
```python
result = endpoint.predict({"question": "What caused GRB 251208B?"})
print(result["answer"])
print(result["sources"])  # ['GRB 251208B']
```

## Owner
NASA GCN Data Pipeline Team
"""

try:
    client.update_registered_model(
        name=MODEL_NAME,
        description=MODEL_DESCRIPTION
    )
    print("✅ Model description updated")
except Exception as e:
    print(f"⚠️ Could not update description: {e}")

# COMMAND ----------

# DBTITLE 1,Adicionar tags ao modelo
# Tags para categorização e busca
MODEL_TAGS = {
    "domain": "astronomy",
    "use_case": "question_answering",
    "model_type": "rag",
    "data_source": "gcn_circulars",
    "llm": "llama-3.1-70b",
    "embedding": "bge-large-en",
    "team": "nasa-gcn-pipeline",
    "certification_lab": "lab-06"
}

try:
    for key, value in MODEL_TAGS.items():
        client.set_registered_model_tag(MODEL_NAME, key, value)

    print("✅ Model tags added:")
    for k, v in MODEL_TAGS.items():
        print(f"   {k}: {v}")
except Exception as e:
    print(f"⚠️ Could not set tags: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Gerenciar Versões

# COMMAND ----------

# DBTITLE 1,Adicionar descrição à versão
try:
    # Get latest version
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if versions:
        latest = max(versions, key=lambda v: int(v.version))

        VERSION_DESCRIPTION = """
## Version Notes

Initial production release of the NASA GCN RAG Assistant.

### Features
- Vector Search retrieval with k=5
- Sentence-based chunking (500 chars, 1 sentence overlap)
- Source citations included in response

### Training Data
- GCN Circulars from 2020-2025
- ~15,000 documents indexed

### Performance
- Average latency: ~2-3s
- Keyword precision: >80%

### Known Limitations
- Limited to events present in GCN Circulars
- May not have latest events if index not synced
"""

        client.update_model_version(
            name=MODEL_NAME,
            version=latest.version,
            description=VERSION_DESCRIPTION
        )
        print(f"✅ Version {latest.version} description updated")
except Exception as e:
    print(f"⚠️ Could not update version: {e}")

# COMMAND ----------

# DBTITLE 1,Adicionar tags à versão
VERSION_TAGS = {
    "release_type": "initial",
    "tested": "true",
    "eval_precision": "0.85",
    "eval_faithfulness": "0.90"
}

try:
    for key, value in VERSION_TAGS.items():
        client.set_model_version_tag(
            name=MODEL_NAME,
            version=latest.version,
            key=key,
            value=value
        )
    print(f"✅ Version {latest.version} tags added")
except Exception as e:
    print(f"⚠️ Could not set version tags: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Explorar Model Lineage

# COMMAND ----------

# DBTITLE 1,Ver lineage do modelo
try:
    # Get run info for the model version
    version_info = client.get_model_version(MODEL_NAME, latest.version)
    run_id = version_info.run_id

    if run_id:
        run = client.get_run(run_id)

        print(f"📊 Model Lineage for v{latest.version}:")
        print(f"\n   Run ID: {run_id}")
        print(f"   Experiment: {run.info.experiment_id}")
        print(f"   Start time: {run.info.start_time}")

        print(f"\n   Parameters:")
        for k, v in run.data.params.items():
            print(f"      {k}: {v}")

        print(f"\n   Metrics:")
        for k, v in run.data.metrics.items():
            print(f"      {k}: {v}")

        print(f"\n   Artifacts:")
        artifacts = client.list_artifacts(run_id)
        for a in artifacts[:5]:
            print(f"      {a.path}")
    else:
        print("⚠️ No run ID associated with this version")

except Exception as e:
    print(f"⚠️ Could not get lineage: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Configurar Permissões

# COMMAND ----------

# DBTITLE 1,Ver permissões atuais
# Exemplo de como verificar permissões via SQL
permissions_query = f"""
SHOW GRANTS ON MODEL {MODEL_NAME}
"""

try:
    permissions_df = spark.sql(permissions_query)
    print("📋 Current Permissions:")
    permissions_df.show(truncate=False)
except Exception as e:
    print(f"⚠️ Could not show grants: {e}")
    print("   This may require MANAGE permission on the model")

# COMMAND ----------

# DBTITLE 1,Exemplo de como conceder permissões
# Exemplo de SQL para conceder permissões
# (Descomentar e ajustar conforme necessário)

print("""
📋 Para configurar permissões, use SQL:

-- Conceder permissão de execução
GRANT EXECUTE ON MODEL {model_name} TO `user@example.com`;

-- Conceder permissão de gerenciamento
GRANT MANAGE ON MODEL {model_name} TO `data-scientists`;

-- Conceder todas as permissões
GRANT ALL PRIVILEGES ON MODEL {model_name} TO `admin-group`;

Níveis de permissão:
  - EXECUTE: Pode usar o modelo para inferência
  - MANAGE: Pode gerenciar versões e aliases
  - ALL PRIVILEGES: Controle total
""".format(model_name=MODEL_NAME))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Salvar Informações do Registro

# COMMAND ----------

# DBTITLE 1,Salvar metadata
# Salvar informações para referência
registration_info = {
    "model_name": MODEL_NAME,
    "catalog": CATALOG,
    "schema": MODEL_SCHEMA,
    "latest_version": latest.version if 'latest' in dir() else "1",
    "tags": json.dumps(MODEL_TAGS),
    "registered_at": str(spark.sql("SELECT current_timestamp()").collect()[0][0])
}

registration_df = spark.createDataFrame([
    (k, str(v)) for k, v in registration_info.items()
], ["key", "value"])

registration_df.write.mode("overwrite").saveAsTable(f"{SCHEMA}.model_registration_info")

print("✅ Registration info saved")
spark.table(f"{SCHEMA}.model_registration_info").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### O que foi configurado:
# MAGIC
# MAGIC | Item | Valor |
# MAGIC |------|-------|
# MAGIC | **Model Name** | `{MODEL_NAME}` |
# MAGIC | **Description** | Documentação completa em Markdown |
# MAGIC | **Tags** | domain, use_case, model_type, etc. |
# MAGIC | **Version Notes** | Features, performance, limitations |
# MAGIC
# MAGIC ### Próximo Notebook: 02-versioning.py
# MAGIC
# MAGIC No próximo notebook, gerenciaremos múltiplas versões do modelo.
