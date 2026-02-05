# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 6.3: Model Aliases and Promotion Workflow
# MAGIC
# MAGIC Este notebook demonstra o uso de aliases para gerenciar o ciclo de vida do modelo.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Configurar aliases (champion, challenger, archived)
# MAGIC 2. Implementar workflow de promoção
# MAGIC 3. Automatizar validação antes de promoção
# MAGIC 4. Documentar processo de governança
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 6: Governance (16%)
# MAGIC - Manage model aliases
# MAGIC - Implement promotion workflows

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
import mlflow
from mlflow import MlflowClient
import pandas as pd
from datetime import datetime

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"
MODEL_NAME = f"{CATALOG}.nasa_gcn_models.gcn_rag_assistant"

client = MlflowClient()
mlflow.set_registry_uri("databricks-uc")

print(f"⚙️ Model: {MODEL_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Entender Aliases

# COMMAND ----------

# DBTITLE 1,Listar aliases atuais
def get_model_aliases(model_name: str) -> dict:
    """Retorna aliases e suas versões."""
    aliases = {}
    try:
        model = client.get_registered_model(model_name)

        # Get all versions and check aliases
        versions = client.search_model_versions(f"name='{model_name}'")
        for v in versions:
            if hasattr(v, 'aliases') and v.aliases:
                for alias in v.aliases:
                    aliases[alias] = v.version
    except Exception as e:
        print(f"Error: {e}")

    return aliases


current_aliases = get_model_aliases(MODEL_NAME)
print("📋 Current Aliases:")
for alias, version in current_aliases.items():
    print(f"   @{alias} → v{version}")

if not current_aliases:
    print("   (No aliases set)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Definir Aliases Padrão

# COMMAND ----------

# DBTITLE 1,Configurar aliases
# Aliases padrão para o ciclo de vida
STANDARD_ALIASES = {
    "champion": "Versão em produção, estável e validada",
    "challenger": "Versão candidata, em testes",
    "archived": "Versão antiga, mantida para referência"
}

print("📋 Standard Aliases:")
for alias, description in STANDARD_ALIASES.items():
    print(f"   @{alias}: {description}")

# COMMAND ----------

# DBTITLE 1,Atribuir aliases às versões
# Get versions
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
sorted_versions = sorted(versions, key=lambda x: int(x.version))

if len(sorted_versions) >= 1:
    # Champion: versão 1 (ou a mais antiga estável)
    champion_version = sorted_versions[0].version
    try:
        client.set_registered_model_alias(MODEL_NAME, "champion", champion_version)
        print(f"✅ @champion → v{champion_version}")
    except Exception as e:
        print(f"⚠️ Could not set champion: {e}")

if len(sorted_versions) >= 2:
    # Challenger: versão mais recente
    challenger_version = sorted_versions[-1].version
    try:
        client.set_registered_model_alias(MODEL_NAME, "challenger", challenger_version)
        print(f"✅ @challenger → v{challenger_version}")
    except Exception as e:
        print(f"⚠️ Could not set challenger: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Workflow de Promoção

# COMMAND ----------

# DBTITLE 1,Definir critérios de promoção
PROMOTION_CRITERIA = {
    "min_eval_precision": 0.80,
    "min_faithfulness": 0.85,
    "max_latency_p95_ms": 5000,
    "min_success_rate": 0.95,
    "required_tests": ["unit", "integration", "load"],
    "required_approvals": 1
}

print("📋 Promotion Criteria:")
for k, v in PROMOTION_CRITERIA.items():
    print(f"   {k}: {v}")

# COMMAND ----------

# DBTITLE 1,Função de validação para promoção
def validate_for_promotion(model_name: str, version: str, criteria: dict) -> dict:
    """
    Valida se uma versão atende aos critérios de promoção.

    Returns:
        Dict com resultado da validação
    """
    results = {
        "version": version,
        "passed": True,
        "checks": [],
        "timestamp": datetime.now().isoformat()
    }

    try:
        version_info = client.get_model_version(model_name, version)
        run_id = version_info.run_id

        if run_id:
            run = client.get_run(run_id)
            metrics = run.data.metrics
            tags = {t.key: t.value for t in client.get_model_version(model_name, version).tags} if hasattr(version_info, 'tags') else {}

            # Check precision
            precision = float(tags.get("eval_precision", metrics.get("avg_keyword_precision", 0)))
            precision_pass = precision >= criteria["min_eval_precision"]
            results["checks"].append({
                "check": "min_eval_precision",
                "required": criteria["min_eval_precision"],
                "actual": precision,
                "passed": precision_pass
            })
            if not precision_pass:
                results["passed"] = False

            # Check faithfulness
            faithfulness = float(tags.get("eval_faithfulness", metrics.get("avg_faithfulness", 0)))
            faithfulness_pass = faithfulness >= criteria["min_faithfulness"]
            results["checks"].append({
                "check": "min_faithfulness",
                "required": criteria["min_faithfulness"],
                "actual": faithfulness,
                "passed": faithfulness_pass
            })
            if not faithfulness_pass:
                results["passed"] = False

            # Check tested tag
            tested = tags.get("tested", "false").lower() == "true"
            results["checks"].append({
                "check": "tested",
                "required": True,
                "actual": tested,
                "passed": tested
            })
            if not tested:
                results["passed"] = False

    except Exception as e:
        results["passed"] = False
        results["error"] = str(e)

    return results


# Validar challenger
if len(sorted_versions) >= 2:
    challenger_version = sorted_versions[-1].version
    validation = validate_for_promotion(MODEL_NAME, challenger_version, PROMOTION_CRITERIA)

    print(f"📊 Validation Results for v{challenger_version}:")
    print(f"   Overall: {'✅ PASSED' if validation['passed'] else '❌ FAILED'}")
    print()
    for check in validation.get("checks", []):
        status = "✅" if check["passed"] else "❌"
        print(f"   {status} {check['check']}: {check['actual']} (required: {check['required']})")

# COMMAND ----------

# DBTITLE 1,Função de promoção
def promote_to_champion(model_name: str, version: str, validate: bool = True) -> bool:
    """
    Promove uma versão para champion.

    Args:
        model_name: Nome do modelo
        version: Versão a promover
        validate: Se True, valida antes de promover

    Returns:
        True se promoção bem-sucedida
    """
    print(f"🔄 Promoting v{version} to @champion...")

    # Validar
    if validate:
        validation = validate_for_promotion(model_name, version, PROMOTION_CRITERIA)
        if not validation["passed"]:
            print(f"❌ Validation failed. Cannot promote.")
            return False
        print("✅ Validation passed")

    try:
        # Encontrar champion atual
        current_champion = None
        try:
            current_champion = client.get_model_version_by_alias(model_name, "champion")
        except:
            pass

        # Mover champion atual para archived
        if current_champion and current_champion.version != version:
            client.set_registered_model_alias(model_name, "archived", current_champion.version)
            print(f"   Moved v{current_champion.version} to @archived")

        # Remover challenger do novo champion
        try:
            client.delete_registered_model_alias(model_name, "challenger")
        except:
            pass

        # Promover nova versão
        client.set_registered_model_alias(model_name, "champion", version)
        print(f"✅ v{version} is now @champion")

        # Adicionar tag de promoção
        client.set_model_version_tag(
            model_name, version,
            "promoted_at", datetime.now().isoformat()
        )

        return True

    except Exception as e:
        print(f"❌ Promotion failed: {e}")
        return False


# Exemplo (não executar automaticamente)
print("""
📋 Para promover challenger para champion:

promote_to_champion(MODEL_NAME, challenger_version)

Isso irá:
1. Validar a versão challenger
2. Mover champion atual para @archived
3. Promover challenger para @champion
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Carregar Modelo por Alias

# COMMAND ----------

# DBTITLE 1,Carregar modelo usando alias
def load_model_by_alias(model_name: str, alias: str):
    """Carrega modelo pelo alias."""
    model_uri = f"models:/{model_name}@{alias}"
    print(f"📦 Loading model from: {model_uri}")

    try:
        model = mlflow.pyfunc.load_model(model_uri)
        print("✅ Model loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Failed to load: {e}")
        return None


# Exemplo
print("📋 Loading models by alias:")
print()

# Tentar carregar champion
champion_model = load_model_by_alias(MODEL_NAME, "champion")

# COMMAND ----------

# DBTITLE 1,Testar modelo carregado por alias
if champion_model:
    test_input = pd.DataFrame({
        "question": ["What is a gamma-ray burst?"]
    })

    print("🔍 Testing @champion model:")
    try:
        result = champion_model.predict(test_input)
        print(f"   Answer: {result['answer'].iloc[0][:200]}...")
        print(f"   Sources: {result['sources'].iloc[0]}")
    except Exception as e:
        print(f"   ⚠️ Prediction error: {e}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Automação com Databricks Jobs

# COMMAND ----------

# DBTITLE 1,Exemplo de job de promoção automatizada
job_config = """
# Databricks Job Configuration for Automated Promotion

name: nasa-gcn-model-promotion

tasks:
  - task_key: validate_challenger
    notebook_task:
      notebook_path: /Repos/nasa-gcn/labs/lab-06-model-management/validate_model
      base_parameters:
        model_name: "sandbox.nasa_gcn_models.gcn_rag_assistant"
        alias: "challenger"

  - task_key: run_eval_suite
    depends_on:
      - task_key: validate_challenger
    notebook_task:
      notebook_path: /Repos/nasa-gcn/labs/lab-04-rag-app/03-evaluation

  - task_key: promote_if_passed
    depends_on:
      - task_key: run_eval_suite
    notebook_task:
      notebook_path: /Repos/nasa-gcn/labs/lab-06-model-management/promote_model
      base_parameters:
        model_name: "sandbox.nasa_gcn_models.gcn_rag_assistant"
        source_alias: "challenger"
        target_alias: "champion"

schedule:
  quartz_cron_expression: "0 0 6 * * ?"  # Daily at 6 AM
  timezone_id: "UTC"

email_notifications:
  on_failure:
    - mlops-team@example.com
"""

print("📋 Example Job Configuration for Automated Promotion:")
print(job_config)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Documentar Estado Final

# COMMAND ----------

# DBTITLE 1,Resumo do estado dos aliases
# Atualizar aliases
final_aliases = get_model_aliases(MODEL_NAME)

# Criar tabela de estado
alias_state = []
for alias, version in final_aliases.items():
    version_info = client.get_model_version(MODEL_NAME, version)
    alias_state.append({
        "alias": f"@{alias}",
        "version": f"v{version}",
        "created": version_info.creation_timestamp,
        "run_id": version_info.run_id[:8] if version_info.run_id else "N/A"
    })

alias_df = pd.DataFrame(alias_state)

print("📋 Final Alias State:")
print(alias_df.to_string(index=False))

# Salvar estado
spark.createDataFrame(alias_df).write.mode("overwrite").saveAsTable("model_alias_state")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Aliases Configurados:
# MAGIC
# MAGIC | Alias | Uso | Descrição |
# MAGIC |-------|-----|-----------|
# MAGIC | @champion | Produção | Versão estável, validada |
# MAGIC | @challenger | Testes | Versão candidata em avaliação |
# MAGIC | @archived | Histórico | Versões anteriores |
# MAGIC
# MAGIC ### Workflow de Promoção:
# MAGIC
# MAGIC ```
# MAGIC challenger → [Validation] → [Approval] → champion
# MAGIC                                              ↓
# MAGIC                                          archived
# MAGIC ```
# MAGIC
# MAGIC ### Referência por Alias:
# MAGIC ```python
# MAGIC model = mlflow.pyfunc.load_model("models:/sandbox.nasa_gcn_models.gcn_rag_assistant@champion")
# MAGIC ```
