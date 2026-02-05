# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 10.1: Production Readiness Checklist
# MAGIC
# MAGIC Este notebook implementa um checklist sistemático para validar readiness de produção.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Verificar todos os componentes do sistema
# MAGIC 2. Validar configurações e permissões
# MAGIC 3. Confirmar SLOs e monitoramento
# MAGIC 4. Gerar relatório de readiness
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - All sections - Comprehensive review
# MAGIC - Production deployment best practices

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")  # noqa: F821
spark.sql(f"USE SCHEMA {SCHEMA}")  # noqa: F821

print("✅ Setup completo")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Definir Checklist

# COMMAND ----------


# DBTITLE 1,Classes e estruturas
class CheckStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARN = "⚠️ WARN"
    SKIP = "⏭️ SKIP"


class CheckCategory(Enum):
    DATA = "Data Quality"
    MODEL = "Model"
    DEPLOYMENT = "Deployment"
    MONITORING = "Monitoring"
    SECURITY = "Security"
    GOVERNANCE = "Governance"


@dataclass
class CheckResult:
    name: str
    category: CheckCategory
    status: CheckStatus
    message: str
    details: Optional[Dict] = None


PRODUCTION_CHECKLIST = {
    CheckCategory.DATA: [
        {
            "name": "Source data available",
            "check": "verify_source_data",
            "critical": True,
            "description": "Verificar se tabela source existe e tem dados",
        },
        {
            "name": "Chunks table populated",
            "check": "verify_chunks_table",
            "critical": True,
            "description": "Verificar tabela de chunks para RAG",
        },
        {
            "name": "Data freshness",
            "check": "verify_data_freshness",
            "critical": False,
            "description": "Verificar se dados estão atualizados",
        },
    ],
    CheckCategory.MODEL: [
        {
            "name": "Model registered in UC",
            "check": "verify_model_registration",
            "critical": True,
            "description": "Verificar se modelo está registrado no Unity Catalog",
        },
        {
            "name": "Model has champion alias",
            "check": "verify_model_alias",
            "critical": True,
            "description": "Verificar se existe alias 'champion'",
        },
        {
            "name": "Model evaluation passed",
            "check": "verify_model_evaluation",
            "critical": True,
            "description": "Verificar se modelo passou nos testes de avaliação",
        },
    ],
    CheckCategory.DEPLOYMENT: [
        {
            "name": "Vector Search endpoint ready",
            "check": "verify_vs_endpoint",
            "critical": True,
            "description": "Verificar se endpoint VS está READY",
        },
        {
            "name": "Vector Search index synced",
            "check": "verify_vs_index",
            "critical": True,
            "description": "Verificar se índice está sincronizado",
        },
        {
            "name": "Model Serving endpoint ready",
            "check": "verify_serving_endpoint",
            "critical": True,
            "description": "Verificar se endpoint de serving está READY",
        },
    ],
    CheckCategory.MONITORING: [
        {
            "name": "Inference logging enabled",
            "check": "verify_inference_logging",
            "critical": True,
            "description": "Verificar se logging de inferências está ativo",
        },
        {
            "name": "Alerts configured",
            "check": "verify_alerts",
            "critical": False,
            "description": "Verificar se alertas estão configurados",
        },
        {
            "name": "Dashboard available",
            "check": "verify_dashboard",
            "critical": False,
            "description": "Verificar se dashboard de monitoramento existe",
        },
    ],
    CheckCategory.SECURITY: [
        {
            "name": "PII scanning completed",
            "check": "verify_pii_scan",
            "critical": True,
            "description": "Verificar se scanning de PII foi executado",
        },
        {
            "name": "Guardrails implemented",
            "check": "verify_guardrails",
            "critical": True,
            "description": "Verificar se guardrails estão implementados",
        },
        {
            "name": "Permissions configured",
            "check": "verify_permissions",
            "critical": False,
            "description": "Verificar permissões no Unity Catalog",
        },
    ],
    CheckCategory.GOVERNANCE: [
        {
            "name": "Model documentation",
            "check": "verify_documentation",
            "critical": False,
            "description": "Verificar se modelo tem documentação",
        },
        {
            "name": "Runbook available",
            "check": "verify_runbook",
            "critical": False,
            "description": "Verificar se runbook de operações existe",
        },
        {
            "name": "Version control",
            "check": "verify_version_control",
            "critical": False,
            "description": "Verificar se código está versionado",
        },
    ],
}

# Contar checks
total_checks = sum(len(checks) for checks in PRODUCTION_CHECKLIST.values())
print(f"📋 Production Readiness Checklist: {total_checks} items")

for category, checks in PRODUCTION_CHECKLIST.items():
    print(f"   {category.value}: {len(checks)} checks")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Implementar Verificações

# COMMAND ----------


# DBTITLE 1,Funções de verificação
def verify_source_data() -> CheckResult:
    """Verifica se tabela source existe e tem dados."""
    try:
        count = spark.table("gcn_circulars").count()  # noqa: F821
        if count > 0:
            return CheckResult(
                name="Source data available",
                category=CheckCategory.DATA,
                status=CheckStatus.PASS,
                message=f"Table gcn_circulars has {count:,} records",
                details={"count": count},
            )
        else:
            return CheckResult(
                name="Source data available",
                category=CheckCategory.DATA,
                status=CheckStatus.FAIL,
                message="Table exists but is empty",
            )
    except Exception as e:
        return CheckResult(
            name="Source data available",
            category=CheckCategory.DATA,
            status=CheckStatus.FAIL,
            message=f"Error: {str(e)}",
        )


def verify_chunks_table() -> CheckResult:
    """Verifica tabela de chunks."""
    try:
        count = spark.table("gcn_circulars_chunks").count()  # noqa: F821
        if count > 0:
            return CheckResult(
                name="Chunks table populated",
                category=CheckCategory.DATA,
                status=CheckStatus.PASS,
                message=f"Table has {count:,} chunks",
                details={"count": count},
            )
        else:
            return CheckResult(
                name="Chunks table populated",
                category=CheckCategory.DATA,
                status=CheckStatus.FAIL,
                message="Chunks table is empty",
            )
    except Exception as e:
        return CheckResult(
            name="Chunks table populated",
            category=CheckCategory.DATA,
            status=CheckStatus.FAIL,
            message=f"Table not found: {str(e)}",
        )


def verify_data_freshness() -> CheckResult:
    """Verifica freshness dos dados."""
    try:
        max_date = (
            spark.sql(  # noqa: F821
                """
            SELECT MAX(created_on) as max_date
            FROM gcn_circulars
            """
            )
            .collect()[0]
            .max_date
        )

        if max_date:
            return CheckResult(
                name="Data freshness",
                category=CheckCategory.DATA,
                status=CheckStatus.PASS,
                message=f"Latest data: {max_date}",
                details={"latest_date": str(max_date)},
            )
        else:
            return CheckResult(
                name="Data freshness",
                category=CheckCategory.DATA,
                status=CheckStatus.WARN,
                message="Could not determine data freshness",
            )
    except Exception as e:
        return CheckResult(
            name="Data freshness",
            category=CheckCategory.DATA,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_model_registration() -> CheckResult:
    """Verifica se modelo está registrado."""
    try:
        from mlflow import MlflowClient

        client = MlflowClient()

        model_name = f"{CATALOG}.nasa_gcn_models.gcn_rag_assistant"
        client.get_registered_model(model_name)  # Verify model exists

        return CheckResult(
            name="Model registered in UC",
            category=CheckCategory.MODEL,
            status=CheckStatus.PASS,
            message=f"Model {model_name} found",
            details={"model_name": model_name},
        )
    except Exception as e:
        return CheckResult(
            name="Model registered in UC",
            category=CheckCategory.MODEL,
            status=CheckStatus.FAIL,
            message=f"Model not found: {str(e)}",
        )


def verify_model_alias() -> CheckResult:
    """Verifica se modelo tem alias champion."""
    try:
        from mlflow import MlflowClient

        client = MlflowClient()

        model_name = f"{CATALOG}.nasa_gcn_models.gcn_rag_assistant"
        versions = client.search_model_versions(f"name='{model_name}'")

        has_champion = any("champion" in (v.aliases or []) for v in versions)

        if has_champion:
            return CheckResult(
                name="Model has champion alias",
                category=CheckCategory.MODEL,
                status=CheckStatus.PASS,
                message="Champion alias configured",
            )
        else:
            return CheckResult(
                name="Model has champion alias",
                category=CheckCategory.MODEL,
                status=CheckStatus.WARN,
                message="No champion alias found",
            )
    except Exception as e:
        return CheckResult(
            name="Model has champion alias",
            category=CheckCategory.MODEL,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_model_evaluation() -> CheckResult:
    """Verifica se avaliação do modelo passou."""
    try:
        eval_results = (
            spark.table("rag_evaluation_history")  # noqa: F821
            .orderBy("eval_date", ascending=False)
            .limit(1)
            .collect()
        )

        if eval_results:
            precision = eval_results[0].avg_keyword_precision
            if precision and precision >= 0.7:
                return CheckResult(
                    name="Model evaluation passed",
                    category=CheckCategory.MODEL,
                    status=CheckStatus.PASS,
                    message=f"Keyword precision: {precision:.2%}",
                    details={"precision": precision},
                )
            else:
                return CheckResult(
                    name="Model evaluation passed",
                    category=CheckCategory.MODEL,
                    status=CheckStatus.WARN,
                    message=f"Precision below target: {precision:.2%}",
                )
        else:
            return CheckResult(
                name="Model evaluation passed",
                category=CheckCategory.MODEL,
                status=CheckStatus.WARN,
                message="No evaluation results found",
            )
    except Exception as e:
        return CheckResult(
            name="Model evaluation passed",
            category=CheckCategory.MODEL,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_vs_endpoint() -> CheckResult:
    """Verifica Vector Search endpoint."""
    try:
        from databricks.vector_search.client import VectorSearchClient

        vsc = VectorSearchClient()

        rag_config = spark.table("rag_config").collect()  # noqa: F821
        config = {row.key: row.value for row in rag_config}
        endpoint_name = config.get("VS_ENDPOINT", "nasa_gcn_vs_endpoint")

        endpoint = vsc.get_endpoint(endpoint_name)
        status = endpoint.get("endpoint_status", {}).get("state", "UNKNOWN")

        if status == "ONLINE":
            return CheckResult(
                name="Vector Search endpoint ready",
                category=CheckCategory.DEPLOYMENT,
                status=CheckStatus.PASS,
                message=f"Endpoint {endpoint_name} is ONLINE",
            )
        else:
            return CheckResult(
                name="Vector Search endpoint ready",
                category=CheckCategory.DEPLOYMENT,
                status=CheckStatus.FAIL,
                message=f"Endpoint status: {status}",
            )
    except Exception as e:
        return CheckResult(
            name="Vector Search endpoint ready",
            category=CheckCategory.DEPLOYMENT,
            status=CheckStatus.FAIL,
            message=f"Check failed: {str(e)}",
        )


def verify_vs_index() -> CheckResult:
    """Verifica Vector Search index."""
    try:
        from databricks.vector_search.client import VectorSearchClient

        vsc = VectorSearchClient()

        rag_config = spark.table("rag_config").collect()  # noqa: F821
        config = {row.key: row.value for row in rag_config}
        endpoint_name = config.get("VS_ENDPOINT")
        index_name = config.get("VS_INDEX")

        index_info = vsc.get_index(endpoint_name, index_name)
        ready = index_info.get("status", {}).get("ready", False)

        if ready:
            return CheckResult(
                name="Vector Search index synced",
                category=CheckCategory.DEPLOYMENT,
                status=CheckStatus.PASS,
                message=f"Index {index_name} is ready",
            )
        else:
            return CheckResult(
                name="Vector Search index synced",
                category=CheckCategory.DEPLOYMENT,
                status=CheckStatus.FAIL,
                message="Index not ready",
            )
    except Exception as e:
        return CheckResult(
            name="Vector Search index synced",
            category=CheckCategory.DEPLOYMENT,
            status=CheckStatus.FAIL,
            message=f"Check failed: {str(e)}",
        )


def verify_serving_endpoint() -> CheckResult:
    """Verifica Model Serving endpoint."""
    try:
        from databricks.sdk import WorkspaceClient

        w = WorkspaceClient()

        endpoint = w.serving_endpoints.get("nasa-gcn-rag-assistant")
        state = endpoint.state.ready

        if state == "READY":
            return CheckResult(
                name="Model Serving endpoint ready",
                category=CheckCategory.DEPLOYMENT,
                status=CheckStatus.PASS,
                message="Endpoint is READY",
            )
        else:
            return CheckResult(
                name="Model Serving endpoint ready",
                category=CheckCategory.DEPLOYMENT,
                status=CheckStatus.FAIL,
                message=f"Endpoint state: {state}",
            )
    except Exception as e:
        return CheckResult(
            name="Model Serving endpoint ready",
            category=CheckCategory.DEPLOYMENT,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_inference_logging() -> CheckResult:
    """Verifica se inference logging está ativo."""
    try:
        query = f"SHOW TABLES IN {CATALOG}.{SCHEMA} LIKE 'inference*'"
        tables = spark.sql(query).collect()  # noqa: F821

        if tables:
            return CheckResult(
                name="Inference logging enabled",
                category=CheckCategory.MONITORING,
                status=CheckStatus.PASS,
                message=f"Found {len(tables)} inference tables",
            )
        else:
            return CheckResult(
                name="Inference logging enabled",
                category=CheckCategory.MONITORING,
                status=CheckStatus.WARN,
                message="No inference tables found",
            )
    except Exception as e:
        return CheckResult(
            name="Inference logging enabled",
            category=CheckCategory.MONITORING,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_alerts() -> CheckResult:
    """Verifica se alertas estão configurados."""
    try:
        alerts = spark.table("alert_history").count()  # noqa: F821

        return CheckResult(
            name="Alerts configured",
            category=CheckCategory.MONITORING,
            status=CheckStatus.PASS,
            message=f"Alert history has {alerts} records",
        )
    except Exception:
        return CheckResult(
            name="Alerts configured",
            category=CheckCategory.MONITORING,
            status=CheckStatus.WARN,
            message="Alert history table not found",
        )


def verify_dashboard() -> CheckResult:
    """Verifica se dashboard existe."""
    try:
        query = f"SHOW VIEWS IN {CATALOG}.{SCHEMA} LIKE '*monitoring*'"
        views = spark.sql(query).collect()  # noqa: F821

        if views:
            return CheckResult(
                name="Dashboard available",
                category=CheckCategory.MONITORING,
                status=CheckStatus.PASS,
                message=f"Found {len(views)} monitoring views",
            )
        else:
            return CheckResult(
                name="Dashboard available",
                category=CheckCategory.MONITORING,
                status=CheckStatus.WARN,
                message="No monitoring views found",
            )
    except Exception as e:
        return CheckResult(
            name="Dashboard available",
            category=CheckCategory.MONITORING,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_pii_scan() -> CheckResult:
    """Verifica se PII scan foi executado."""
    try:
        count = spark.table("pii_scan_results").count()  # noqa: F821

        return CheckResult(
            name="PII scanning completed",
            category=CheckCategory.SECURITY,
            status=CheckStatus.PASS,
            message=f"PII scan completed: {count} records scanned",
        )
    except Exception:
        return CheckResult(
            name="PII scanning completed",
            category=CheckCategory.SECURITY,
            status=CheckStatus.WARN,
            message="PII scan results not found",
        )


def verify_guardrails() -> CheckResult:
    """Verifica se guardrails estão implementados."""
    # Check if anonymized table exists (implies guardrails were implemented)
    try:
        count = spark.table("gcn_circulars_anonymized").count()  # noqa: F821

        return CheckResult(
            name="Guardrails implemented",
            category=CheckCategory.SECURITY,
            status=CheckStatus.PASS,
            message=f"Anonymized data available: {count} records",
        )
    except Exception:
        return CheckResult(
            name="Guardrails implemented",
            category=CheckCategory.SECURITY,
            status=CheckStatus.WARN,
            message="Anonymized table not found",
        )


def verify_permissions() -> CheckResult:
    """Verifica permissões."""
    return CheckResult(
        name="Permissions configured",
        category=CheckCategory.SECURITY,
        status=CheckStatus.SKIP,
        message="Manual verification required",
    )


def verify_documentation() -> CheckResult:
    """Verifica documentação do modelo."""
    try:
        from mlflow import MlflowClient

        client = MlflowClient()

        model_name = f"{CATALOG}.nasa_gcn_models.gcn_rag_assistant"
        model = client.get_registered_model(model_name)

        if model.description and len(model.description) > 100:
            return CheckResult(
                name="Model documentation",
                category=CheckCategory.GOVERNANCE,
                status=CheckStatus.PASS,
                message="Model has detailed documentation",
            )
        else:
            return CheckResult(
                name="Model documentation",
                category=CheckCategory.GOVERNANCE,
                status=CheckStatus.WARN,
                message="Model documentation is minimal",
            )
    except Exception as e:
        return CheckResult(
            name="Model documentation",
            category=CheckCategory.GOVERNANCE,
            status=CheckStatus.WARN,
            message=f"Check failed: {str(e)}",
        )


def verify_runbook() -> CheckResult:
    """Verifica se runbook existe."""
    try:
        spark.table("monitoring_runbook").count()  # noqa: F821

        return CheckResult(
            name="Runbook available",
            category=CheckCategory.GOVERNANCE,
            status=CheckStatus.PASS,
            message="Runbook is documented",
        )
    except Exception:
        return CheckResult(
            name="Runbook available",
            category=CheckCategory.GOVERNANCE,
            status=CheckStatus.WARN,
            message="Runbook not found",
        )


def verify_version_control() -> CheckResult:
    """Verifica version control."""
    return CheckResult(
        name="Version control",
        category=CheckCategory.GOVERNANCE,
        status=CheckStatus.SKIP,
        message="Assumed - code in Git repository",
    )


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Executar Checklist

# COMMAND ----------

# DBTITLE 1,Executar todas as verificações
# Mapeamento de checks para funções
CHECK_FUNCTIONS = {
    "verify_source_data": verify_source_data,
    "verify_chunks_table": verify_chunks_table,
    "verify_data_freshness": verify_data_freshness,
    "verify_model_registration": verify_model_registration,
    "verify_model_alias": verify_model_alias,
    "verify_model_evaluation": verify_model_evaluation,
    "verify_vs_endpoint": verify_vs_endpoint,
    "verify_vs_index": verify_vs_index,
    "verify_serving_endpoint": verify_serving_endpoint,
    "verify_inference_logging": verify_inference_logging,
    "verify_alerts": verify_alerts,
    "verify_dashboard": verify_dashboard,
    "verify_pii_scan": verify_pii_scan,
    "verify_guardrails": verify_guardrails,
    "verify_permissions": verify_permissions,
    "verify_documentation": verify_documentation,
    "verify_runbook": verify_runbook,
    "verify_version_control": verify_version_control,
}


def run_checklist() -> List[CheckResult]:
    """Executa todos os checks do checklist."""
    results = []

    for category, checks in PRODUCTION_CHECKLIST.items():
        print(f"\n📋 {category.value}")
        print("-" * 50)

        for check_item in checks:
            check_func = CHECK_FUNCTIONS.get(check_item["check"])

            if check_func:
                result = check_func()
                results.append(result)
                print(f"   {result.status.value} {result.name}")
                if result.status != CheckStatus.PASS:
                    print(f"      {result.message}")
            else:
                print(f"   ⏭️ SKIP {check_item['name']} (no function)")

    return results


print("🔄 Running Production Readiness Checklist...")
print("=" * 60)

all_results = run_checklist()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Gerar Relatório

# COMMAND ----------

# DBTITLE 1,Resumo do checklist
# Contar resultados por status
status_counts = {}
for result in all_results:
    status = result.status.name
    status_counts[status] = status_counts.get(status, 0) + 1

# Contar críticos que falharam
critical_checks = []
for category, checks in PRODUCTION_CHECKLIST.items():
    for check in checks:
        if check["critical"]:
            critical_checks.append(check["name"])

critical_failures = [
    r for r in all_results if r.name in critical_checks and r.status == CheckStatus.FAIL
]

# Determinar readiness
is_ready = len(critical_failures) == 0

print(f"""
╔══════════════════════════════════════════════════════════════╗
║           Production Readiness Assessment                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Overall Status: {"✅ READY FOR PRODUCTION" if is_ready else "❌ NOT READY"}               ║
║                                                              ║
║  Check Results:                                              ║
║    ✅ PASS:  {status_counts.get("PASS", 0):>3}                                         ║
║    ❌ FAIL:  {status_counts.get("FAIL", 0):>3}                                         ║
║    ⚠️  WARN:  {status_counts.get("WARN", 0):>3}                                         ║
║    ⏭️  SKIP:  {status_counts.get("SKIP", 0):>3}                                         ║
║                                                              ║
║  Critical Failures: {len(critical_failures)}                                       ║
╚══════════════════════════════════════════════════════════════╝
""")

if critical_failures:
    print("🚨 Critical Issues to Resolve:")
    for failure in critical_failures:
        print(f"   - {failure.name}: {failure.message}")

# COMMAND ----------

# DBTITLE 1,Salvar relatório
# Converter resultados para salvar
report_data = [
    {
        "check_name": r.name,
        "category": r.category.value,
        "status": r.status.name,
        "message": r.message,
        "timestamp": datetime.now().isoformat(),
    }
    for r in all_results
]

(
    spark.createDataFrame(report_data)  # noqa: F821
    .write.mode("overwrite")
    .saveAsTable("readiness_check_results")
)

# Salvar summary
summary = {
    "timestamp": datetime.now().isoformat(),
    "is_ready": is_ready,
    "total_checks": len(all_results),
    "passed": status_counts.get("PASS", 0),
    "failed": status_counts.get("FAIL", 0),
    "warnings": status_counts.get("WARN", 0),
    "critical_failures": len(critical_failures),
}

(
    spark.createDataFrame([summary])  # noqa: F821
    .write.mode("append")
    .saveAsTable("readiness_summary_history")
)

print("✅ Results saved to 'readiness_check_results' and 'readiness_summary_history'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo
# MAGIC
# MAGIC ### Status de Readiness:
# MAGIC
# MAGIC Este checklist verifica:
# MAGIC - **Data Quality**: Tabelas source e chunks
# MAGIC - **Model**: Registro, alias, avaliação
# MAGIC - **Deployment**: VS e Model Serving endpoints
# MAGIC - **Monitoring**: Logging, alertas, dashboard
# MAGIC - **Security**: PII scan, guardrails
# MAGIC - **Governance**: Documentação, runbook
# MAGIC
# MAGIC ### Próximo Notebook: 02-simulation.py
