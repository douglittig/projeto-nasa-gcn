# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 5.2: Deploying RAG Model to Serving Endpoint
# MAGIC
# MAGIC Este notebook faz o deploy do modelo RAG como um Model Serving endpoint.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Criar Model Serving endpoint
# MAGIC 2. Configurar scaling e compute
# MAGIC 3. Aguardar endpoint ficar pronto
# MAGIC 4. Validar deployment
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 5: Assembling and Deploying Applications (22%)
# MAGIC - Deploy model to Model Serving endpoint
# MAGIC - Configure endpoint scaling and compute

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
    EndpointCoreConfigInput,
    ServedEntityInput,
    AutoCaptureConfigInput,
    TrafficConfig,
    Route
)
import time
import requests
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Carregar info do modelo
model_info_df = spark.table("rag_model_info").collect()
model_info = {row.key: row.value for row in model_info_df}

MODEL_NAME = model_info.get("model_name")
MODEL_VERSION = model_info.get("model_version")

# Endpoint name
ENDPOINT_NAME = "nasa-gcn-rag-assistant"

print(f"""
⚙️ Configuração:
  - Model: {MODEL_NAME}
  - Version: {MODEL_VERSION}
  - Endpoint: {ENDPOINT_NAME}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Criar Workspace Client

# COMMAND ----------

# DBTITLE 1,Inicializar SDK client
# Initialize Databricks SDK client
w = WorkspaceClient()

print("✅ Workspace client initialized")
print(f"   Host: {w.config.host}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Verificar se Endpoint Existe

# COMMAND ----------

# DBTITLE 1,Verificar endpoints existentes
# List existing endpoints
existing_endpoints = list(w.serving_endpoints.list())
endpoint_names = [ep.name for ep in existing_endpoints]

print(f"📋 Endpoints existentes: {len(endpoint_names)}")
for name in endpoint_names[:10]:
    print(f"   - {name}")

endpoint_exists = ENDPOINT_NAME in endpoint_names
print(f"\n{'✅' if endpoint_exists else '❌'} Endpoint '{ENDPOINT_NAME}' {'existe' if endpoint_exists else 'não existe'}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Criar ou Atualizar Endpoint

# COMMAND ----------

# DBTITLE 1,Configuração do Endpoint
# Served entity configuration
served_entity = ServedEntityInput(
    entity_name=MODEL_NAME,
    entity_version=MODEL_VERSION,
    workload_size="Small",  # Small, Medium, Large
    scale_to_zero_enabled=True,  # Scale to zero when not in use
    workload_type="CPU"  # CPU or GPU
)

# Endpoint configuration
endpoint_config = EndpointCoreConfigInput(
    served_entities=[served_entity],
    auto_capture_config=AutoCaptureConfigInput(
        catalog_name=CATALOG,
        schema_name=SCHEMA,
        table_name_prefix="rag_inference_"
    )
)

print(f"""
📦 Endpoint Configuration:
  - Entity: {MODEL_NAME}
  - Version: {MODEL_VERSION}
  - Workload: Small (CPU)
  - Scale to zero: Enabled
  - Inference logging: {CATALOG}.{SCHEMA}.rag_inference_*
""")

# COMMAND ----------

# DBTITLE 1,Criar ou atualizar endpoint
if endpoint_exists:
    print(f"🔄 Atualizando endpoint '{ENDPOINT_NAME}'...")
    w.serving_endpoints.update_config(
        name=ENDPOINT_NAME,
        served_entities=[served_entity],
        traffic_config=TrafficConfig(
            routes=[Route(served_model_name=f"{MODEL_NAME}-{MODEL_VERSION}", traffic_percentage=100)]
        )
    )
    print("✅ Endpoint atualizado")
else:
    print(f"🔄 Criando endpoint '{ENDPOINT_NAME}'...")
    w.serving_endpoints.create(
        name=ENDPOINT_NAME,
        config=endpoint_config
    )
    print("✅ Endpoint criado")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Aguardar Endpoint Ficar Pronto

# COMMAND ----------

# DBTITLE 1,Monitor endpoint status
def wait_for_endpoint_ready(client, endpoint_name, timeout_minutes=30):
    """
    Aguarda endpoint ficar pronto.

    Args:
        client: WorkspaceClient
        endpoint_name: Nome do endpoint
        timeout_minutes: Timeout em minutos

    Returns:
        True se pronto, False se timeout
    """
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    while True:
        try:
            endpoint = client.serving_endpoints.get(endpoint_name)
            state = endpoint.state

            elapsed = time.time() - start_time
            print(f"  [{elapsed/60:.1f}min] State: {state.ready}, Config: {state.config_update}")

            if state.ready == "READY":
                return True

            if state.ready == "NOT_READY" and state.config_update == "UPDATE_FAILED":
                print(f"❌ Deployment failed")
                return False

            if elapsed > timeout_seconds:
                print("⏰ Timeout")
                return False

            time.sleep(30)

        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(30)


print("⏳ Aguardando endpoint ficar pronto...")
is_ready = wait_for_endpoint_ready(w, ENDPOINT_NAME, timeout_minutes=20)

if is_ready:
    print("✅ Endpoint pronto!")
else:
    print("⚠️ Endpoint não está pronto. Verifique o status no UI.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Obter Informações do Endpoint

# COMMAND ----------

# DBTITLE 1,Endpoint details
endpoint = w.serving_endpoints.get(ENDPOINT_NAME)

print(f"""
📊 Endpoint Details:
─────────────────────
Name:           {endpoint.name}
State:          {endpoint.state.ready}
Creator:        {endpoint.creator}
Creation Time:  {endpoint.creation_timestamp}

Served Entities:
""")

for entity in endpoint.config.served_entities:
    print(f"  - {entity.entity_name} v{entity.entity_version}")
    print(f"    Workload: {entity.workload_size}")
    print(f"    Scale to zero: {entity.scale_to_zero_enabled}")

# Get endpoint URL
endpoint_url = f"{w.config.host}/serving-endpoints/{ENDPOINT_NAME}/invocations"
print(f"\n🔗 Endpoint URL: {endpoint_url}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Testar Endpoint

# COMMAND ----------

# DBTITLE 1,Teste via SDK
# Testar usando o SDK
from databricks.sdk.service.serving import DataframeSplitInput

# Prepare input
test_input = {
    "dataframe_split": {
        "columns": ["question"],
        "data": [["What observations were made for gamma-ray bursts detected by Fermi?"]]
    }
}

print("🔍 Testando endpoint via SDK...")
print("-" * 60)

try:
    response = w.serving_endpoints.query(
        name=ENDPOINT_NAME,
        dataframe_split=DataframeSplitInput(
            columns=["question"],
            data=[["What observations were made for gamma-ray bursts detected by Fermi?"]]
        )
    )

    # Parse response
    if hasattr(response, 'predictions'):
        predictions = response.predictions
        if predictions:
            print(f"\n📝 Response:")
            print(f"   Answer: {predictions[0].get('answer', 'N/A')[:300]}...")
            print(f"   Sources: {predictions[0].get('sources', '[]')}")
    else:
        print(f"Response: {response}")

except Exception as e:
    print(f"❌ Error: {e}")

# COMMAND ----------

# DBTITLE 1,Teste via REST API
import os

# Get token
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
host = spark.conf.get("spark.databricks.workspaceUrl")

# Endpoint URL
url = f"https://{host}/serving-endpoints/{ENDPOINT_NAME}/invocations"

# Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Request body
payload = {
    "dataframe_split": {
        "columns": ["question"],
        "data": [["What high-energy neutrino events were detected by IceCube?"]]
    }
}

print("🔍 Testando endpoint via REST API...")
print(f"   URL: {url}")
print("-" * 60)

try:
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    predictions = result.get("predictions", [])

    if predictions:
        print(f"\n📝 Response:")
        print(f"   Answer: {predictions[0].get('answer', 'N/A')[:300]}...")
        print(f"   Sources: {predictions[0].get('sources', '[]')}")
        print(f"   Status: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"❌ Request error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Salvar Endpoint Info

# COMMAND ----------

# DBTITLE 1,Salvar informações do endpoint
# Save endpoint info for testing notebook
endpoint_info = {
    "endpoint_name": ENDPOINT_NAME,
    "endpoint_url": endpoint_url,
    "model_name": MODEL_NAME,
    "model_version": MODEL_VERSION,
    "workspace_host": w.config.host
}

endpoint_info_df = spark.createDataFrame([
    (k, str(v)) for k, v in endpoint_info.items()
], ["key", "value"])

endpoint_info_df.write.mode("overwrite").saveAsTable("rag_endpoint_info")

print("✅ Endpoint info saved to 'rag_endpoint_info'")
spark.table("rag_endpoint_info").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Configurar Permissões (Opcional)

# COMMAND ----------

# DBTITLE 1,Configurar permissões do endpoint
# Exemplo de como configurar permissões
# (Descomentar e ajustar conforme necessário)

# from databricks.sdk.service.serving import EndpointPermissions, EndpointPermissionLevel

# # Grant permissions to specific users/groups
# w.serving_endpoints.set_permissions(
#     serving_endpoint_id=ENDPOINT_NAME,
#     access_control_list=[
#         {
#             "user_name": "user@example.com",
#             "permission_level": EndpointPermissionLevel.CAN_QUERY
#         },
#         {
#             "group_name": "data-scientists",
#             "permission_level": EndpointPermissionLevel.CAN_MANAGE
#         }
#     ]
# )

print("""
📋 Para configurar permissões:

1. Via UI: Workspace > Serving > Endpoint > Permissions
2. Via SDK:
   w.serving_endpoints.set_permissions(
       serving_endpoint_id=ENDPOINT_NAME,
       access_control_list=[...]
   )

Permission levels:
  - CAN_QUERY: Pode fazer queries
  - CAN_VIEW: Pode visualizar
  - CAN_MANAGE: Pode gerenciar
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo e Próximos Passos
# MAGIC
# MAGIC ### O que foi criado:
# MAGIC
# MAGIC | Componente | Valor |
# MAGIC |------------|-------|
# MAGIC | **Endpoint Name** | `nasa-gcn-rag-assistant` |
# MAGIC | **Model** | `{MODEL_NAME}` |
# MAGIC | **Workload** | Small (CPU) |
# MAGIC | **Scale to Zero** | Enabled |
# MAGIC | **Inference Logging** | `{CATALOG}.{SCHEMA}.rag_inference_*` |
# MAGIC
# MAGIC ### Endpoint URL:
# MAGIC ```
# MAGIC https://<workspace>/serving-endpoints/nasa-gcn-rag-assistant/invocations
# MAGIC ```
# MAGIC
# MAGIC ### Próximo Notebook: 03-test-endpoint.py
# MAGIC
# MAGIC No próximo notebook, testaremos o endpoint:
# MAGIC 1. Testes de carga
# MAGIC 2. Monitorar latência
# MAGIC 3. Verificar inference logs
# MAGIC 4. Exemplo de integração com aplicação

