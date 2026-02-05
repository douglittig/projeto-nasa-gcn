# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 6.2: Model Versioning and Comparison
# MAGIC
# MAGIC Este notebook demonstra versionamento e comparação de modelos.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Criar nova versão do modelo
# MAGIC 2. Comparar versões
# MAGIC 3. Implementar A/B testing
# MAGIC 4. Rollback de versão
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 6: Governance (16%)
# MAGIC - Manage model versions
# MAGIC - Compare model performance across versions

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
import mlflow
from mlflow import MlflowClient
from mlflow.pyfunc import PythonModel
import pandas as pd
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"
MODEL_NAME = f"{CATALOG}.nasa_gcn_models.gcn_rag_assistant"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

client = MlflowClient()
mlflow.set_registry_uri("databricks-uc")

print(f"⚙️ Model: {MODEL_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Listar Versões Existentes

# COMMAND ----------

# DBTITLE 1,Ver todas as versões
def list_model_versions(model_name: str) -> pd.DataFrame:
    """Lista todas as versões de um modelo."""
    versions = client.search_model_versions(f"name='{model_name}'")

    data = []
    for v in versions:
        aliases = v.aliases if hasattr(v, 'aliases') else []
        data.append({
            "version": v.version,
            "status": v.status,
            "aliases": ", ".join(aliases) if aliases else "none",
            "creation_time": v.creation_timestamp,
            "run_id": v.run_id[:8] if v.run_id else "N/A"
        })

    return pd.DataFrame(data).sort_values("version", ascending=False)


versions_df = list_model_versions(MODEL_NAME)
print("📋 Model Versions:")
print(versions_df.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar Nova Versão (Simulação)

# COMMAND ----------

# DBTITLE 1,Simular nova versão com parâmetros diferentes
# Em produção, você criaria uma nova versão retreinando o modelo
# Aqui simulamos logando o mesmo modelo com parâmetros diferentes

# Carregar config existente
config_df = spark.table("rag_config").collect()
config = {row.key: row.value for row in config_df}

# Novos parâmetros para versão 2
new_config = {
    "vs_endpoint": config.get("VS_ENDPOINT"),
    "vs_index": config.get("VS_INDEX"),
    "llm_endpoint": "databricks-meta-llama-3-1-70b-instruct",
    "retriever_k": 7,  # Aumentado de 5 para 7
    "temperature": 0.05,  # Reduzido de 0.1 para 0.05
    "max_tokens": 1500  # Aumentado de 1024 para 1500
}

print("🔧 New configuration for v2:")
for k, v in new_config.items():
    print(f"   {k}: {v}")

# COMMAND ----------

# DBTITLE 1,Logar nova versão
# Salvar nova config
config_path = "/tmp/rag_config_v2.json"
with open(config_path, "w") as f:
    json.dump(new_config, f, indent=2)

# Definir modelo (reutilizando classe do Lab 5)
class NASAGCNRagModelV2(PythonModel):
    """Version 2 with optimized parameters."""

    def load_context(self, context):
        from databricks.vector_search.client import VectorSearchClient
        from langchain_community.vectorstores import DatabricksVectorSearch
        from langchain_community.chat_models import ChatDatabricks

        config_path = context.artifacts.get("config")
        with open(config_path, "r") as f:
            config = json.load(f)

        self.vs_endpoint = config["vs_endpoint"]
        self.vs_index = config["vs_index"]

        vsc = VectorSearchClient()
        dvs = DatabricksVectorSearch(
            endpoint=self.vs_endpoint,
            index_name=self.vs_index,
            text_column="chunk_text",
            columns=["chunk_id", "event_id", "subject", "chunk_text"]
        )
        self.retriever = dvs.as_retriever(search_kwargs={"k": config["retriever_k"]})

        self.llm = ChatDatabricks(
            endpoint=config["llm_endpoint"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
        self.config = config

    def predict(self, context, model_input):
        results = []
        for _, row in model_input.iterrows():
            question = row.get("question", "")
            try:
                docs = self.retriever.invoke(question)
                context_str = "\n\n".join([
                    f"[{d.metadata.get('event_id')}]: {d.page_content}"
                    for d in docs
                ])

                from langchain_core.prompts import ChatPromptTemplate
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert astrophysics assistant. Answer using ONLY the context.\n\nContext:\n{context}"),
                    ("human", "{question}")
                ])
                messages = prompt.format_messages(context=context_str, question=question)
                response = self.llm.invoke(messages)

                citations = list(set(d.metadata.get("event_id") for d in docs if d.metadata.get("event_id")))

                results.append({
                    "answer": response.content,
                    "sources": json.dumps(sorted(citations)),
                    "num_docs": len(docs)
                })
            except Exception as e:
                results.append({"answer": str(e), "sources": "[]", "num_docs": 0})

        return pd.DataFrame(results)


print("✅ NASAGCNRagModelV2 defined")

# COMMAND ----------

# DBTITLE 1,Registrar nova versão
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec

# Signature
input_schema = Schema([ColSpec("string", "question")])
output_schema = Schema([
    ColSpec("string", "answer"),
    ColSpec("string", "sources"),
    ColSpec("integer", "num_docs")
])
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

# Log new version
experiment_name = f"/Users/{spark.sql('SELECT current_user()').collect()[0][0]}/nasa_gcn_rag_model"
mlflow.set_experiment(experiment_name)

with mlflow.start_run(run_name="nasa_gcn_rag_v2") as run:
    mlflow.log_params({
        "retriever_k": 7,
        "temperature": 0.05,
        "max_tokens": 1500,
        "version": "2.0"
    })

    mlflow.pyfunc.log_model(
        artifact_path="nasa_gcn_rag",
        python_model=NASAGCNRagModelV2(),
        artifacts={"config": config_path},
        signature=signature,
        pip_requirements=["databricks-vectorsearch", "langchain", "langchain-community", "mlflow"]
    )

    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/nasa_gcn_rag"

# Register new version
new_version = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)

print(f"✅ New version registered: v{new_version.version}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Comparar Versões

# COMMAND ----------

# DBTITLE 1,Comparar parâmetros entre versões
def compare_versions(model_name: str, v1: str, v2: str) -> pd.DataFrame:
    """Compara parâmetros de duas versões."""
    version1 = client.get_model_version(model_name, v1)
    version2 = client.get_model_version(model_name, v2)

    # Get runs
    run1 = client.get_run(version1.run_id) if version1.run_id else None
    run2 = client.get_run(version2.run_id) if version2.run_id else None

    params1 = run1.data.params if run1 else {}
    params2 = run2.data.params if run2 else {}

    # Combine all params
    all_params = set(params1.keys()) | set(params2.keys())

    comparison = []
    for param in sorted(all_params):
        val1 = params1.get(param, "N/A")
        val2 = params2.get(param, "N/A")
        changed = "✓" if val1 != val2 else ""
        comparison.append({
            "parameter": param,
            f"v{v1}": val1,
            f"v{v2}": val2,
            "changed": changed
        })

    return pd.DataFrame(comparison)


# Get versions
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
if len(versions) >= 2:
    sorted_versions = sorted(versions, key=lambda x: int(x.version))
    v1 = sorted_versions[-2].version
    v2 = sorted_versions[-1].version

    comparison_df = compare_versions(MODEL_NAME, v1, v2)
    print(f"📊 Parameter Comparison (v{v1} vs v{v2}):")
    print(comparison_df.to_string(index=False))
else:
    print("⚠️ Need at least 2 versions to compare")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Simulação de A/B Testing

# COMMAND ----------

# DBTITLE 1,Configurar traffic split para A/B test
# Em produção, isso seria feito no Model Serving endpoint
# Aqui demonstramos a lógica

print("""
📊 A/B Testing Configuration

Para configurar A/B testing no Model Serving:

1. Via UI:
   - Serving Endpoints > nasa-gcn-rag-assistant > Edit
   - Add second served entity with different version
   - Set traffic split (e.g., 90% v1, 10% v2)

2. Via SDK:
```python
from databricks.sdk.service.serving import TrafficConfig, Route

w.serving_endpoints.update_config(
    name="nasa-gcn-rag-assistant",
    traffic_config=TrafficConfig(
        routes=[
            Route(
                served_model_name="gcn_rag_assistant-1",
                traffic_percentage=90
            ),
            Route(
                served_model_name="gcn_rag_assistant-2",
                traffic_percentage=10
            )
        ]
    )
)
```

3. Monitorar métricas por versão:
```sql
SELECT
    served_model_name,
    COUNT(*) as requests,
    AVG(latency_ms) as avg_latency
FROM inference_logs
GROUP BY served_model_name
```
""")

# COMMAND ----------

# DBTITLE 1,Simular A/B test localmente
import random

def simulate_ab_test(questions: list, v1_weight: float = 0.9) -> pd.DataFrame:
    """Simula A/B test com distribuição de tráfego."""
    results = []

    for q in questions:
        # Simular roteamento
        version = "v1" if random.random() < v1_weight else "v2"

        # Simular latência (v2 pode ser mais lento por recuperar mais docs)
        base_latency = 2000
        latency = base_latency + random.randint(0, 500)
        if version == "v2":
            latency += 300  # v2 retrieves more docs

        results.append({
            "question": q[:40] + "...",
            "version": version,
            "latency_ms": latency,
            "success": True
        })

    return pd.DataFrame(results)


# Simular
test_questions = [
    "What is a gamma-ray burst?",
    "How does IceCube detect neutrinos?",
    "What caused GRB 251208B?",
    "Describe gravitational wave detection",
    "What are Swift XRT observations?"
] * 20  # 100 requests

ab_results = simulate_ab_test(test_questions, v1_weight=0.9)

# Analisar
print("📊 Simulated A/B Test Results:")
print("-" * 50)
print(ab_results.groupby("version").agg({
    "question": "count",
    "latency_ms": ["mean", "std"]
}).to_string())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Rollback Procedure

# COMMAND ----------

# DBTITLE 1,Documentar procedimento de rollback
print("""
🔄 Rollback Procedure

Se a nova versão apresentar problemas, siga estes passos:

1. **Identificar a versão estável:**
```python
# Encontrar versão com alias 'champion' ou última conhecida boa
stable_version = client.get_model_version_by_alias(MODEL_NAME, "champion")
```

2. **Atualizar o endpoint para versão anterior:**
```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()

w.serving_endpoints.update_config(
    name="nasa-gcn-rag-assistant",
    served_entities=[ServedEntityInput(
        entity_name=MODEL_NAME,
        entity_version=stable_version.version,  # Versão anterior
        workload_size="Small"
    )]
)
```

3. **Atualizar alias:**
```python
# Remover alias da versão problemática
client.delete_registered_model_alias(MODEL_NAME, "champion")

# Atribuir alias à versão estável
client.set_registered_model_alias(MODEL_NAME, "champion", stable_version.version)
```

4. **Documentar o incidente:**
```python
client.set_model_version_tag(
    name=MODEL_NAME,
    version=problematic_version,
    key="rollback_reason",
    value="Performance degradation detected"
)
```
""")

# COMMAND ----------

# DBTITLE 1,Exemplo de rollback (simulado)
# Marcar versão problemática (se existir v2)
if len(versions) >= 2:
    latest_version = max(versions, key=lambda x: int(x.version))

    # Adicionar tag de advertência
    client.set_model_version_tag(
        name=MODEL_NAME,
        version=latest_version.version,
        key="status",
        value="testing"
    )

    print(f"⚠️ Version {latest_version.version} marked as 'testing'")
    print("   In production, this version should be monitored before promotion")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Salvar Histórico de Versões

# COMMAND ----------

# DBTITLE 1,Salvar histórico
# Atualizar lista de versões
versions_df = list_model_versions(MODEL_NAME)

# Converter para Spark e salvar
versions_spark = spark.createDataFrame(versions_df)
versions_spark.write.mode("overwrite").saveAsTable("model_version_history")

print("✅ Version history saved to 'model_version_history'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Versões do Modelo:
# MAGIC
# MAGIC | Versão | Parâmetros | Status |
# MAGIC |--------|------------|--------|
# MAGIC | v1 | k=5, temp=0.1 | champion |
# MAGIC | v2 | k=7, temp=0.05 | testing |
# MAGIC
# MAGIC ### Próximo Notebook: 03-aliases.py
