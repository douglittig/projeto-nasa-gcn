# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 5.1: Creating a PyFunc RAG Model
# MAGIC
# MAGIC Este notebook cria um modelo MLflow PyFunc que encapsula todo o sistema RAG.
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Criar classe PyFunc para RAG
# MAGIC 2. Implementar load_context e predict
# MAGIC 3. Logar modelo com MLflow
# MAGIC 4. Testar modelo localmente
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 5: Assembling and Deploying Applications (22%)
# MAGIC - Create custom PyFunc model for deployment
# MAGIC - Log model with MLflow including dependencies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# DBTITLE 1,Instalar dependências
# MAGIC %pip install databricks-vectorsearch langchain langchain-community mlflow -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Imports
import mlflow
from mlflow.pyfunc import PythonModel, PythonModelContext
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec
import pandas as pd
import json

# Configuração
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Carregar config do Lab 3
config_df = spark.table("rag_config").collect()
config = {row.key: row.value for row in config_df}

VS_ENDPOINT = config.get("VS_ENDPOINT", "nasa_gcn_vs_endpoint")
VS_INDEX = config.get("VS_INDEX", f"{CATALOG}.{SCHEMA}.gcn_chunks_vs_index")
EMBEDDING_MODEL = config.get("EMBEDDING_MODEL", "databricks-bge-large-en")

print(f"""
⚙️ Configuração:
  - VS Endpoint: {VS_ENDPOINT}
  - VS Index: {VS_INDEX}
  - Embedding Model: {EMBEDDING_MODEL}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Definir Classe PyFunc

# COMMAND ----------

# DBTITLE 1,NASAGCNRagModel PyFunc
class NASAGCNRagModel(PythonModel):
    """
    MLflow PyFunc model for NASA GCN RAG system.

    This model encapsulates the complete RAG pipeline:
    - Vector Search retrieval
    - Context formatting
    - LLM generation with citations
    """

    def __init__(self):
        """Initialize model parameters."""
        self.retriever = None
        self.llm = None
        self.vs_endpoint = None
        self.vs_index = None

    def load_context(self, context: PythonModelContext):
        """
        Load model artifacts and initialize components.

        This method is called once when the model is loaded.
        """
        from databricks.vector_search.client import VectorSearchClient
        from langchain_community.vectorstores import DatabricksVectorSearch
        from langchain_community.chat_models import ChatDatabricks

        # Load configuration from artifacts
        config_path = context.artifacts.get("config")
        if config_path:
            with open(config_path, "r") as f:
                config = json.load(f)
        else:
            # Default configuration
            config = {
                "vs_endpoint": "nasa_gcn_vs_endpoint",
                "vs_index": "sandbox.nasa_gcn_dev.gcn_chunks_vs_index",
                "llm_endpoint": "databricks-meta-llama-3-1-70b-instruct",
                "retriever_k": 5,
                "temperature": 0.1,
                "max_tokens": 1024
            }

        self.vs_endpoint = config["vs_endpoint"]
        self.vs_index = config["vs_index"]

        # Initialize Vector Search retriever
        vsc = VectorSearchClient()
        dvs = DatabricksVectorSearch(
            endpoint=self.vs_endpoint,
            index_name=self.vs_index,
            text_column="chunk_text",
            columns=["chunk_id", "event_id", "subject", "chunk_text", "chunk_index"]
        )
        self.retriever = dvs.as_retriever(search_kwargs={"k": config["retriever_k"]})

        # Initialize LLM
        self.llm = ChatDatabricks(
            endpoint=config["llm_endpoint"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )

        # Store config for reference
        self.config = config

    def _format_context(self, docs) -> str:
        """Format retrieved documents into context string."""
        formatted = []
        for doc in docs:
            event_id = doc.metadata.get("event_id", "Unknown")
            subject = doc.metadata.get("subject", "No subject")
            formatted.append(f"[{event_id}] {subject}\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)

    def _extract_citations(self, docs) -> list:
        """Extract unique event IDs from documents."""
        event_ids = set()
        for doc in docs:
            event_id = doc.metadata.get("event_id")
            if event_id:
                event_ids.add(event_id)
        return sorted(list(event_ids))

    def _generate_response(self, question: str, context: str) -> str:
        """Generate response using LLM."""
        from langchain_core.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert astrophysics assistant specializing in transient astronomical events.
Answer questions about gamma-ray bursts (GRBs), gravitational waves (GW), neutrino detections,
and other astronomical transients using ONLY the provided GCN Circulars context.

Guidelines:
1. Base your answers ONLY on the provided context
2. If the context doesn't contain enough information, say "I don't have sufficient information"
3. Always cite the source event_id when referencing specific observations
4. Be precise with coordinates, times, and measurements

Context from GCN Circulars:
{context}"""),
            ("human", "{question}")
        ])

        messages = prompt.format_messages(context=context, question=question)
        response = self.llm.invoke(messages)
        return response.content

    def predict(self, context: PythonModelContext, model_input: pd.DataFrame) -> pd.DataFrame:
        """
        Generate RAG responses for input questions.

        Args:
            context: MLflow context (unused in predict, already loaded)
            model_input: DataFrame with 'question' column

        Returns:
            DataFrame with 'answer', 'sources', and 'num_docs' columns
        """
        results = []

        for _, row in model_input.iterrows():
            question = row.get("question", "")

            if not question:
                results.append({
                    "answer": "Error: No question provided",
                    "sources": [],
                    "num_docs": 0
                })
                continue

            try:
                # Retrieve relevant documents
                docs = self.retriever.invoke(question)

                # Format context
                context_str = self._format_context(docs)

                # Extract citations
                citations = self._extract_citations(docs)

                # Generate response
                answer = self._generate_response(question, context_str)

                results.append({
                    "answer": answer,
                    "sources": json.dumps(citations),
                    "num_docs": len(docs)
                })

            except Exception as e:
                results.append({
                    "answer": f"Error generating response: {str(e)}",
                    "sources": "[]",
                    "num_docs": 0
                })

        return pd.DataFrame(results)


print("✅ NASAGCNRagModel class defined")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Testar Modelo Localmente

# COMMAND ----------

# DBTITLE 1,Teste local do modelo
# Criar instância para teste
test_model = NASAGCNRagModel()

# Simular load_context com config manual
class MockContext:
    def __init__(self):
        self.artifacts = {}

# Criar config temporário
import tempfile
import os

config = {
    "vs_endpoint": VS_ENDPOINT,
    "vs_index": VS_INDEX,
    "llm_endpoint": "databricks-meta-llama-3-1-70b-instruct",
    "retriever_k": 5,
    "temperature": 0.1,
    "max_tokens": 1024
}

# Salvar config como artifact
config_path = "/tmp/rag_config.json"
with open(config_path, "w") as f:
    json.dump(config, f)

# Mock context com artifact
mock_context = MockContext()
mock_context.artifacts = {"config": config_path}

# Load context
print("🔄 Loading model context...")
test_model.load_context(mock_context)
print("✅ Model loaded")

# COMMAND ----------

# DBTITLE 1,Testar predict
# Criar input de teste
test_input = pd.DataFrame({
    "question": [
        "What observations were made for gamma-ray bursts?",
        "What is the position error for recent GRB detections?"
    ]
})

print("🔍 Testing predict...")
print("-" * 60)

results = test_model.predict(None, test_input)

for i, row in results.iterrows():
    print(f"\n📝 Question {i+1}:")
    print(f"   Answer: {row['answer'][:200]}...")
    print(f"   Sources: {row['sources']}")
    print(f"   Docs used: {row['num_docs']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Definir Model Signature

# COMMAND ----------

# DBTITLE 1,Model Signature
# Define input schema
input_schema = Schema([
    ColSpec("string", "question")
])

# Define output schema
output_schema = Schema([
    ColSpec("string", "answer"),
    ColSpec("string", "sources"),  # JSON array of event_ids
    ColSpec("integer", "num_docs")
])

# Create signature
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

print("✅ Model signature defined")
print(f"   Input: {input_schema}")
print(f"   Output: {output_schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Logar Modelo com MLflow

# COMMAND ----------

# DBTITLE 1,Configurar experimento
# Set experiment
experiment_name = f"/Users/{spark.sql('SELECT current_user()').collect()[0][0]}/nasa_gcn_rag_model"
mlflow.set_experiment(experiment_name)

print(f"✅ Experiment: {experiment_name}")

# COMMAND ----------

# DBTITLE 1,Logar modelo
# Salvar config como artifact
config_artifact_path = "/tmp/model_config.json"
with open(config_artifact_path, "w") as f:
    json.dump(config, f, indent=2)

# Definir dependências
pip_requirements = [
    "databricks-vectorsearch",
    "langchain",
    "langchain-community",
    "mlflow"
]

# Log model
with mlflow.start_run(run_name="nasa_gcn_rag_v1") as run:
    # Log parameters
    mlflow.log_params({
        "vs_endpoint": VS_ENDPOINT,
        "vs_index": VS_INDEX,
        "llm_endpoint": "databricks-meta-llama-3-1-70b-instruct",
        "retriever_k": 5,
        "temperature": 0.1
    })

    # Log model
    mlflow.pyfunc.log_model(
        artifact_path="nasa_gcn_rag",
        python_model=NASAGCNRagModel(),
        artifacts={"config": config_artifact_path},
        signature=signature,
        pip_requirements=pip_requirements,
        input_example=pd.DataFrame({"question": ["What is a gamma-ray burst?"]})
    )

    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/nasa_gcn_rag"

    print(f"✅ Model logged successfully")
    print(f"   Run ID: {run_id}")
    print(f"   Model URI: {model_uri}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Testar Modelo Logado

# COMMAND ----------

# DBTITLE 1,Carregar e testar modelo do MLflow
# Load model from MLflow
loaded_model = mlflow.pyfunc.load_model(model_uri)

# Test prediction
test_df = pd.DataFrame({
    "question": ["What optical telescopes observed GRB afterglows?"]
})

print("🔍 Testing loaded model...")
result = loaded_model.predict(test_df)

print(f"\n📝 Answer: {result['answer'].iloc[0][:300]}...")
print(f"📚 Sources: {result['sources'].iloc[0]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Registrar no Unity Catalog

# COMMAND ----------

# DBTITLE 1,Registrar modelo no UC
# Register model in Unity Catalog
MODEL_NAME = f"{CATALOG}.nasa_gcn_models.gcn_rag_assistant"

# Create schema if not exists
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.nasa_gcn_models")

# Register model
registered_model = mlflow.register_model(
    model_uri=model_uri,
    name=MODEL_NAME
)

print(f"✅ Model registered in Unity Catalog")
print(f"   Name: {MODEL_NAME}")
print(f"   Version: {registered_model.version}")

# COMMAND ----------

# DBTITLE 1,Adicionar alias 'champion'
from mlflow import MlflowClient

client = MlflowClient()

# Set alias
client.set_registered_model_alias(
    name=MODEL_NAME,
    alias="champion",
    version=registered_model.version
)

print(f"✅ Alias 'champion' set for version {registered_model.version}")

# COMMAND ----------

# DBTITLE 1,Adicionar descrição do modelo
# Update model description
client.update_registered_model(
    name=MODEL_NAME,
    description="""
NASA GCN RAG Assistant

A Retrieval-Augmented Generation model for answering questions about astronomical events
using GCN Circulars as the knowledge base.

**Capabilities:**
- Answer questions about gamma-ray bursts (GRBs)
- Provide information on gravitational wave events
- Retrieve neutrino detection details
- Include source citations (event_ids)

**Input:** Question string
**Output:** Answer, source citations, number of documents used
"""
)

print("✅ Model description updated")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Salvar Informações para Próximo Notebook

# COMMAND ----------

# DBTITLE 1,Salvar model info
# Save model info for deployment notebook
model_info = {
    "model_name": MODEL_NAME,
    "model_version": registered_model.version,
    "model_uri": model_uri,
    "run_id": run_id,
    "vs_endpoint": VS_ENDPOINT,
    "vs_index": VS_INDEX
}

# Save to table
model_info_df = spark.createDataFrame([
    (k, str(v)) for k, v in model_info.items()
], ["key", "value"])

model_info_df.write.mode("overwrite").saveAsTable("rag_model_info")

print("✅ Model info saved to 'rag_model_info'")
spark.table("rag_model_info").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo e Próximos Passos
# MAGIC
# MAGIC ### O que foi criado:
# MAGIC
# MAGIC | Componente | Descrição |
# MAGIC |------------|-----------|
# MAGIC | **NASAGCNRagModel** | Classe PyFunc com load_context e predict |
# MAGIC | **MLflow Run** | Modelo logado com artifacts e signature |
# MAGIC | **Unity Catalog Model** | Modelo registrado com alias 'champion' |
# MAGIC
# MAGIC ### Model URI:
# MAGIC ```
# MAGIC models:/{MODEL_NAME}@champion
# MAGIC ```
# MAGIC
# MAGIC ### Próximo Notebook: 02-deploy-endpoint.py
# MAGIC
# MAGIC No próximo notebook, faremos o deploy:
# MAGIC 1. Criar Model Serving endpoint
# MAGIC 2. Configurar scaling e compute
# MAGIC 3. Testar endpoint via REST API

