# Lab 5: End-to-End RAG System Deployment

Este lab faz o deploy completo do sistema RAG como um Model Serving endpoint no Databricks.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Criar modelos PyFunc** personalizados para RAG
2. **Logar modelos** com MLflow incluindo artifacts e signature
3. **Registrar modelos** no Unity Catalog com aliases
4. **Fazer deploy** como Model Serving endpoint
5. **Testar e monitorar** endpoints em produção

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 5: Assembling and Deploying Applications** | 22% | PyFunc, MLflow, Model Serving |
| **Section 4: Evaluation and Monitoring** | 18% | Inference logging, latency monitoring |

## Pré-requisitos

- **Lab 4 completo:** RAG chain testada e funcionando
- Tabelas `rag_config` e `rag_test_questions`
- Permissão para criar Model Serving endpoints

## Estrutura do Lab

```
lab-05-deployment/
├── 01-pyfunc-model.py           # Criar e logar modelo PyFunc
├── 02-deploy-endpoint.py        # Deploy como Model Serving
├── 03-test-endpoint.py          # Testar e monitorar endpoint
└── README.md                    # Este arquivo
```

## Notebooks

### 1. PyFunc Model (`01-pyfunc-model.py`)

**O que você vai aprender:**
- Criar classe `NASAGCNRagModel` com `load_context` e `predict`
- Definir Model Signature (input/output schema)
- Logar modelo com MLflow
- Registrar no Unity Catalog com alias

**Estrutura do PyFunc:**

```python
class NASAGCNRagModel(PythonModel):
    def load_context(self, context):
        # Inicializar retriever e LLM
        # Carregar config dos artifacts

    def predict(self, context, model_input):
        # Recuperar documentos
        # Gerar resposta
        # Retornar answer + citations
```

### 2. Deploy Endpoint (`02-deploy-endpoint.py`)

**O que você vai aprender:**
- Usar Databricks SDK para criar endpoint
- Configurar scaling (scale-to-zero)
- Habilitar inference logging
- Aguardar endpoint ficar ready

**Configuração do Endpoint:**

| Parâmetro | Valor |
|-----------|-------|
| Workload Size | Small |
| Scale to Zero | Enabled |
| Workload Type | CPU |
| Auto Capture | Enabled |

### 3. Test Endpoint (`03-test-endpoint.py`)

**O que você vai aprender:**
- Testar endpoint via REST API
- Medir latência e throughput
- Rodar testes de carga concorrentes
- Verificar inference logs

**Métricas monitoradas:**

| Métrica | Descrição |
|---------|-----------|
| Latency (ms) | Tempo de resposta |
| Throughput | Queries por segundo |
| Success Rate | % de queries bem-sucedidas |
| P95 Latency | Percentil 95 da latência |

## Arquitetura de Deploy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Databricks Model Serving                      │
│                   nasa-gcn-rag-assistant                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  NASAGCNRagModel (PyFunc)                  │ │
│  │                                                            │ │
│  │  load_context():                                           │ │
│  │    ├── Load config from artifacts                         │ │
│  │    ├── Initialize VectorSearchClient                      │ │
│  │    ├── Create LangChain retriever                         │ │
│  │    └── Initialize ChatDatabricks LLM                      │ │
│  │                                                            │ │
│  │  predict(question):                                        │ │
│  │    ├── Retrieve relevant chunks from Vector Search        │ │
│  │    ├── Format context with event metadata                 │ │
│  │    ├── Generate answer using Llama 3.1 70B               │ │
│  │    └── Return {answer, sources, num_docs}                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Inference Logging → sandbox.nasa_gcn_dev.rag_inference_*       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Vector Search Index                         │
│            sandbox.nasa_gcn_dev.gcn_chunks_vs_index             │
└─────────────────────────────────────────────────────────────────┘
```

## Recursos Criados

| Recurso | Nome | Tipo |
|---------|------|------|
| MLflow Model | `sandbox.nasa_gcn_models.gcn_rag_assistant` | UC Model |
| Serving Endpoint | `nasa-gcn-rag-assistant` | Model Serving |
| Model Info | `rag_model_info` | Delta Table |
| Endpoint Info | `rag_endpoint_info` | Delta Table |
| Test Results | `rag_endpoint_test_results` | Delta Table |
| Load Results | `rag_endpoint_load_test_results` | Delta Table |

## Comandos Úteis

### Verificar status do endpoint
```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
endpoint = w.serving_endpoints.get("nasa-gcn-rag-assistant")
print(f"Status: {endpoint.state.ready}")
```

### Query via REST API
```bash
curl -X POST \
  "https://<workspace>/serving-endpoints/nasa-gcn-rag-assistant/invocations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["question"], "data": [["What is a GRB?"]]}}'
```

### Ver inference logs
```sql
SELECT *
FROM sandbox.nasa_gcn_dev.rag_inference_payload
ORDER BY timestamp DESC
LIMIT 10;
```

### Atualizar modelo no endpoint
```python
w.serving_endpoints.update_config(
    name="nasa-gcn-rag-assistant",
    served_entities=[ServedEntityInput(
        entity_name="sandbox.nasa_gcn_models.gcn_rag_assistant",
        entity_version="2",
        workload_size="Small"
    )]
)
```

## Troubleshooting

### Endpoint não inicia
```python
# Verificar logs do endpoint
endpoint = w.serving_endpoints.get("nasa-gcn-rag-assistant")
print(endpoint.state)
print(endpoint.pending_config)  # Ver config pendente
```

### Erro de dependências
```python
# Verificar se todas as deps estão no pip_requirements
pip_requirements = [
    "databricks-vectorsearch",
    "langchain==0.1.0",  # Fixar versão
    "langchain-community==0.0.20",
    "mlflow"
]
```

### Timeout nas queries
1. Aumentar timeout no cliente
2. Verificar se Vector Search está respondendo
3. Considerar usar workload_size="Medium"

### Model não encontra artifacts
```python
# Verificar se config foi logado corretamente
mlflow.artifacts.download_artifacts(
    run_id="<run_id>",
    artifact_path="nasa_gcn_rag"
)
```

## Exemplo de Client Python

```python
class NASAGCNRagClient:
    def __init__(self, endpoint_url: str, token: str):
        self.endpoint_url = endpoint_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def ask(self, question: str) -> dict:
        payload = {
            "dataframe_split": {
                "columns": ["question"],
                "data": [[question]]
            }
        }
        response = requests.post(
            self.endpoint_url,
            headers=self.headers,
            json=payload
        )
        return response.json()["predictions"][0]

# Usage
client = NASAGCNRagClient(url, token)
result = client.ask("What is a gamma-ray burst?")
print(result["answer"])
```

## Próximos Passos

Após completar este lab, continue para:

- **Lab 6: Model Management** - Versionamento, aliases, A/B testing
- **Lab 7: Guardrails** - PII detection, prompt injection protection

## Referências

- [Model Serving Documentation](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
- [MLflow PyFunc Models](https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html)
- [Unity Catalog Models](https://docs.databricks.com/en/mlflow/unity-catalog.html)

---

*Última atualização: Fevereiro 2026*
