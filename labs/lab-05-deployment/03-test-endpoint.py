# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 5.3: Testing and Monitoring the RAG Endpoint
# MAGIC
# MAGIC Este notebook testa o endpoint RAG e monitora seu desempenho.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Testar endpoint com múltiplas queries
# MAGIC 2. Medir latência e throughput
# MAGIC 3. Verificar inference logs
# MAGIC 4. Criar dashboard de monitoramento
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 4: Evaluation and Monitoring (18%)
# MAGIC - Monitor model serving endpoint performance
# MAGIC - Analyze inference logs

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Imports
import requests
import time
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from databricks.sdk import WorkspaceClient

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Carregar endpoint info
endpoint_info_df = spark.table("rag_endpoint_info").collect()
endpoint_info = {row.key: row.value for row in endpoint_info_df}

ENDPOINT_NAME = endpoint_info.get("endpoint_name")
ENDPOINT_URL = endpoint_info.get("endpoint_url")

print(f"""
⚙️ Configuração:
  - Endpoint: {ENDPOINT_NAME}
  - URL: {ENDPOINT_URL}
""")

# COMMAND ----------

# DBTITLE 1,Setup authentication
# Get token for API calls
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
host = spark.conf.get("spark.databricks.workspaceUrl")

# Base URL
base_url = f"https://{host}/serving-endpoints/{ENDPOINT_NAME}/invocations"

# Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print(f"🔗 Endpoint URL: {base_url}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Função de Query

# COMMAND ----------

# DBTITLE 1,Query function
def query_endpoint(question: str, timeout: int = 120) -> dict:
    """
    Query the RAG endpoint.

    Args:
        question: Question to ask
        timeout: Request timeout in seconds

    Returns:
        Dict with answer, sources, latency_ms, and status
    """
    payload = {
        "dataframe_split": {
            "columns": ["question"],
            "data": [[question]]
        }
    }

    start_time = time.time()

    try:
        response = requests.post(
            base_url,
            headers=headers,
            json=payload,
            timeout=timeout
        )

        latency_ms = (time.time() - start_time) * 1000
        response.raise_for_status()

        result = response.json()
        predictions = result.get("predictions", [{}])

        return {
            "question": question,
            "answer": predictions[0].get("answer", ""),
            "sources": predictions[0].get("sources", "[]"),
            "num_docs": predictions[0].get("num_docs", 0),
            "latency_ms": latency_ms,
            "status": "success",
            "status_code": response.status_code
        }

    except requests.exceptions.Timeout:
        return {
            "question": question,
            "answer": "",
            "sources": "[]",
            "num_docs": 0,
            "latency_ms": timeout * 1000,
            "status": "timeout",
            "status_code": 408
        }

    except requests.exceptions.RequestException as e:
        latency_ms = (time.time() - start_time) * 1000
        return {
            "question": question,
            "answer": str(e),
            "sources": "[]",
            "num_docs": 0,
            "latency_ms": latency_ms,
            "status": "error",
            "status_code": getattr(e.response, 'status_code', 500) if hasattr(e, 'response') else 500
        }

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Teste Individual

# COMMAND ----------

# DBTITLE 1,Single query test
# Teste com uma pergunta
test_question = "What observations were made for gamma-ray bursts detected by Fermi GBM?"

print(f"🔍 Testing: {test_question}")
print("-" * 60)

result = query_endpoint(test_question)

print(f"\n📊 Results:")
print(f"   Status: {result['status']}")
print(f"   Latency: {result['latency_ms']:.0f}ms")
print(f"   Sources: {result['sources']}")
print(f"\n📝 Answer:\n{result['answer'][:500]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Batch Testing

# COMMAND ----------

# DBTITLE 1,Test questions dataset
# Conjunto de perguntas para teste
TEST_QUESTIONS = [
    # GRB Questions
    "What observations were made for gamma-ray bursts detected by Fermi GBM?",
    "What are the typical durations of short gamma-ray bursts?",
    "What is the position accuracy of Swift BAT localizations?",

    # Neutrino Questions
    "What high-energy neutrino events were detected by IceCube?",
    "What is the typical energy of IceCube neutrino alerts?",

    # Follow-up Questions
    "What optical telescopes conducted follow-up observations?",
    "What magnitude did the optical counterpart have?",

    # X-ray Questions
    "What X-ray afterglows were detected by Swift XRT?",
    "What is the typical flux of X-ray afterglows?",

    # Gravitational Wave Questions
    "What gravitational wave events were detected by LIGO?",
]

print(f"📋 {len(TEST_QUESTIONS)} questions prepared for testing")

# COMMAND ----------

# DBTITLE 1,Run batch test
print("🔄 Running batch test...")
print("-" * 60)

results = []

for i, question in enumerate(TEST_QUESTIONS):
    print(f"  [{i+1}/{len(TEST_QUESTIONS)}] {question[:50]}...")
    result = query_endpoint(question)
    results.append(result)
    print(f"      → {result['status']}, {result['latency_ms']:.0f}ms")

print(f"\n✅ Batch test complete: {len(results)} queries")

# COMMAND ----------

# DBTITLE 1,Analyze batch results
# Convert to DataFrame
results_df = pd.DataFrame(results)

# Statistics
print("📊 Batch Test Statistics:")
print("-" * 40)
print(f"Total queries:     {len(results_df)}")
print(f"Successful:        {len(results_df[results_df['status'] == 'success'])}")
print(f"Errors:            {len(results_df[results_df['status'] != 'success'])}")
print()
print(f"Latency (ms):")
print(f"  - Min:     {results_df['latency_ms'].min():.0f}")
print(f"  - Mean:    {results_df['latency_ms'].mean():.0f}")
print(f"  - Median:  {results_df['latency_ms'].median():.0f}")
print(f"  - Max:     {results_df['latency_ms'].max():.0f}")
print(f"  - P95:     {results_df['latency_ms'].quantile(0.95):.0f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Concurrent Load Test

# COMMAND ----------

# DBTITLE 1,Concurrent query function
def run_concurrent_test(questions: list, num_workers: int = 3) -> list:
    """
    Run concurrent queries to test endpoint under load.

    Args:
        questions: List of questions
        num_workers: Number of concurrent workers

    Returns:
        List of results
    """
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_question = {
            executor.submit(query_endpoint, q): q
            for q in questions
        }

        for future in as_completed(future_to_question):
            result = future.result()
            results.append(result)

    return results

# COMMAND ----------

# DBTITLE 1,Run load test
# Multiplicar perguntas para teste de carga
load_test_questions = TEST_QUESTIONS * 2  # 20 queries

print(f"🔄 Running load test with {len(load_test_questions)} queries, 3 concurrent workers...")
print("-" * 60)

start_time = time.time()
load_results = run_concurrent_test(load_test_questions, num_workers=3)
total_time = time.time() - start_time

# Statistics
load_df = pd.DataFrame(load_results)
successful = len(load_df[load_df['status'] == 'success'])

print(f"\n📊 Load Test Results:")
print(f"   Total queries:      {len(load_results)}")
print(f"   Successful:         {successful}")
print(f"   Success rate:       {successful/len(load_results)*100:.1f}%")
print(f"   Total time:         {total_time:.1f}s")
print(f"   Throughput:         {len(load_results)/total_time:.2f} queries/sec")
print(f"   Avg latency:        {load_df['latency_ms'].mean():.0f}ms")
print(f"   P95 latency:        {load_df['latency_ms'].quantile(0.95):.0f}ms")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Verificar Inference Logs

# COMMAND ----------

# DBTITLE 1,Check inference tables
# List inference tables
inference_tables = spark.sql(f"""
    SHOW TABLES IN {CATALOG}.{SCHEMA} LIKE 'rag_inference*'
""").collect()

if inference_tables:
    print("📋 Inference Tables:")
    for table in inference_tables:
        print(f"   - {table.tableName}")

    # Try to read latest inference log
    try:
        inference_df = spark.sql(f"""
            SELECT *
            FROM {CATALOG}.{SCHEMA}.{inference_tables[0].tableName}
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        print(f"\n📊 Latest inferences from {inference_tables[0].tableName}:")
        inference_df.show(truncate=50)
    except Exception as e:
        print(f"⚠️ Could not read inference table: {e}")
else:
    print("⚠️ No inference tables found yet. They will be created after the first queries.")
    print("   Tables are created with prefix: rag_inference_*")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Salvar Resultados do Teste

# COMMAND ----------

# DBTITLE 1,Save test results
# Save batch results
batch_results_spark = spark.createDataFrame(results_df)
batch_results_spark.write.mode("overwrite").saveAsTable("rag_endpoint_test_results")

# Save load test results
load_results_spark = spark.createDataFrame(load_df)
load_results_spark.write.mode("append").saveAsTable("rag_endpoint_load_test_results")

print("✅ Test results saved:")
print(f"   - Batch results: rag_endpoint_test_results")
print(f"   - Load results: rag_endpoint_load_test_results")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Create Monitoring Summary

# COMMAND ----------

# DBTITLE 1,Monitoring dashboard
print("""
╔══════════════════════════════════════════════════════════════╗
║           NASA GCN RAG Endpoint - Monitoring Summary         ║
╠══════════════════════════════════════════════════════════════╣
""")

print(f"  📍 Endpoint: {ENDPOINT_NAME}")
print(f"  🔗 URL: {base_url}")
print()

# Batch test summary
print("  📊 Batch Test (Sequential):")
print(f"     Queries:     {len(results_df)}")
print(f"     Success:     {len(results_df[results_df['status'] == 'success'])}/{len(results_df)}")
print(f"     Avg Latency: {results_df['latency_ms'].mean():.0f}ms")
print()

# Load test summary
print("  📊 Load Test (Concurrent):")
print(f"     Queries:     {len(load_df)}")
print(f"     Success:     {successful}/{len(load_df)}")
print(f"     Throughput:  {len(load_results)/total_time:.2f} qps")
print(f"     P95 Latency: {load_df['latency_ms'].quantile(0.95):.0f}ms")

print("""
╠══════════════════════════════════════════════════════════════╣
║  Tables Created:                                             ║
║    - rag_endpoint_test_results                               ║
║    - rag_endpoint_load_test_results                          ║
╚══════════════════════════════════════════════════════════════╝
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Exemplo de Integração

# COMMAND ----------

# DBTITLE 1,Example: Python client
# Exemplo de código para integração em aplicação Python

example_code = '''
# Example Python client for NASA GCN RAG endpoint

import requests

class NASAGCNRagClient:
    """Client for NASA GCN RAG endpoint."""

    def __init__(self, endpoint_url: str, token: str):
        self.endpoint_url = endpoint_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def ask(self, question: str) -> dict:
        """
        Ask a question about astronomical events.

        Args:
            question: Question string

        Returns:
            Dict with answer, sources, and metadata
        """
        payload = {
            "dataframe_split": {
                "columns": ["question"],
                "data": [[question]]
            }
        }

        response = requests.post(
            self.endpoint_url,
            headers=self.headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()
        prediction = result.get("predictions", [{}])[0]

        return {
            "answer": prediction.get("answer", ""),
            "sources": prediction.get("sources", "[]"),
            "num_docs": prediction.get("num_docs", 0)
        }


# Usage example:
# client = NASAGCNRagClient(
#     endpoint_url="https://<workspace>/serving-endpoints/nasa-gcn-rag-assistant/invocations",
#     token="<your-token>"
# )
# result = client.ask("What is a gamma-ray burst?")
# print(result["answer"])
'''

print("📝 Example Python Client:")
print("-" * 60)
print(example_code)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo e Próximos Passos
# MAGIC
# MAGIC ### Testes Realizados:
# MAGIC
# MAGIC | Teste | Queries | Success Rate | Latência Média |
# MAGIC |-------|---------|--------------|----------------|
# MAGIC | Batch (Sequential) | 10 | 100% | ~Xms |
# MAGIC | Load (Concurrent) | 20 | ~100% | ~Xms |
# MAGIC
# MAGIC ### Tabelas Criadas:
# MAGIC
# MAGIC | Tabela | Descrição |
# MAGIC |--------|-----------|
# MAGIC | `rag_endpoint_test_results` | Resultados do teste batch |
# MAGIC | `rag_endpoint_load_test_results` | Resultados do teste de carga |
# MAGIC | `rag_inference_*` | Logs de inferência (auto-capture) |
# MAGIC
# MAGIC ### Próximo Lab: 06-model-management
# MAGIC
# MAGIC No próximo lab, gerenciaremos versões do modelo:
# MAGIC 1. Versionamento com aliases
# MAGIC 2. A/B testing
# MAGIC 3. Rollback procedures

