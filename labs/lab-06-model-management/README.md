# Lab 6: Model Management with MLflow & Unity Catalog

Este lab demonstra o gerenciamento completo do ciclo de vida de modelos usando MLflow e Unity Catalog.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Registrar modelos** no Unity Catalog com metadados
2. **Gerenciar versões** e comparar performance
3. **Usar aliases** para controlar promoção (champion/challenger)
4. **Implementar workflows** de governança de modelos

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 6: Governance** | 16% | Model registry, versioning, aliases, permissions |

## Pré-requisitos

- **Lab 5 completo:** Modelo registrado no Unity Catalog
- Permissão para gerenciar modelos no catálogo

## Estrutura do Lab

```
lab-06-model-management/
├── 01-register-model.py         # Registro e metadados
├── 02-versioning.py             # Versionamento e comparação
├── 03-aliases.py                # Aliases e promoção
└── README.md                    # Este arquivo
```

## Notebooks

### 1. Register Model (`01-register-model.py`)

**O que você vai aprender:**
- Adicionar descrição em Markdown ao modelo
- Configurar tags para categorização
- Adicionar notas de versão
- Explorar model lineage

**Tags recomendadas:**
```python
{
    "domain": "astronomy",
    "use_case": "question_answering",
    "model_type": "rag",
    "team": "nasa-gcn-pipeline"
}
```

### 2. Versioning (`02-versioning.py`)

**O que você vai aprender:**
- Criar novas versões com parâmetros diferentes
- Comparar parâmetros entre versões
- Simular A/B testing
- Implementar rollback

**Comparação de versões:**
| Parâmetro | v1 | v2 |
|-----------|----|----|
| retriever_k | 5 | 7 |
| temperature | 0.1 | 0.05 |
| max_tokens | 1024 | 1500 |

### 3. Aliases (`03-aliases.py`)

**O que você vai aprender:**
- Configurar aliases padrão
- Implementar workflow de promoção
- Validar antes de promover
- Carregar modelo por alias

**Aliases padrão:**
| Alias | Descrição |
|-------|-----------|
| @champion | Versão em produção |
| @challenger | Versão em testes |
| @archived | Versão histórica |

## Workflow de Promoção

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  New Model  │────▶│ @challenger │────▶│  @champion  │
│   Version   │     │  (Testing)  │     │(Production) │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  @archived  │
                                        │ (Previous)  │
                                        └─────────────┘
```

### Critérios de Promoção

```python
PROMOTION_CRITERIA = {
    "min_eval_precision": 0.80,
    "min_faithfulness": 0.85,
    "max_latency_p95_ms": 5000,
    "min_success_rate": 0.95,
    "required_tests": ["unit", "integration", "load"]
}
```

## Recursos Criados

| Recurso | Nome | Descrição |
|---------|------|-----------|
| Model | `sandbox.nasa_gcn_models.gcn_rag_assistant` | Modelo RAG registrado |
| Table | `model_registration_info` | Informações de registro |
| Table | `model_version_history` | Histórico de versões |
| Table | `model_alias_state` | Estado atual dos aliases |

## Comandos Úteis

### Listar versões
```python
from mlflow import MlflowClient
client = MlflowClient()
versions = client.search_model_versions("name='sandbox.nasa_gcn_models.gcn_rag_assistant'")
```

### Carregar por alias
```python
model = mlflow.pyfunc.load_model("models:/sandbox.nasa_gcn_models.gcn_rag_assistant@champion")
```

### Definir alias
```python
client.set_registered_model_alias(
    name="sandbox.nasa_gcn_models.gcn_rag_assistant",
    alias="champion",
    version="1"
)
```

### Ver permissões
```sql
SHOW GRANTS ON MODEL sandbox.nasa_gcn_models.gcn_rag_assistant;
```

### Conceder permissões
```sql
GRANT EXECUTE ON MODEL sandbox.nasa_gcn_models.gcn_rag_assistant TO `user@example.com`;
```

## Boas Práticas

1. **Sempre use aliases** em vez de versões hardcoded em produção
2. **Valide antes de promover** usando critérios objetivos
3. **Documente cada versão** com notas de release
4. **Mantenha @archived** para rollback rápido
5. **Use tags** para facilitar busca e auditoria

## Troubleshooting

### Erro: "Model not found"
```python
# Verificar nome correto
mlflow.set_registry_uri("databricks-uc")
models = client.search_registered_models()
```

### Erro: "Permission denied"
```sql
-- Verificar suas permissões
SHOW GRANTS ON MODEL sandbox.nasa_gcn_models.gcn_rag_assistant;
```

### Alias não encontrado
```python
# Listar aliases existentes
model = client.get_registered_model(MODEL_NAME)
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
for v in versions:
    print(f"v{v.version}: {v.aliases}")
```

## Próximos Passos

Após completar este lab, continue para:

- **Lab 7: Guardrails** - Proteção de PII e prompt injection
- **Lab 8: Monitoring** - Monitoramento de inferência

## Referências

- [Unity Catalog Models](https://docs.databricks.com/en/mlflow/unity-catalog.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [Model Aliases](https://docs.databricks.com/en/mlflow/model-registry.html#model-aliases)

---

*Última atualização: Fevereiro 2026*
