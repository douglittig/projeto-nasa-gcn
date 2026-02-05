# Lab 3: Chunking & Indexing for RAG

Este lab implementa a preparação de dados para RAG (Retrieval-Augmented Generation) usando os GCN Circulars da NASA.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Extrair e filtrar documentos** para RAG de qualidade
2. **Aplicar estratégias de chunking** (caracteres, sentenças, parágrafos)
3. **Gerar embeddings** com modelos Databricks
4. **Criar e gerenciar índices Vector Search** com Delta Sync
5. **Testar retrieval semântico** e avaliar qualidade

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 2: Data Preparation** | 14% | Chunking strategies, document filtering, Delta Lake |
| **Section 3: Application Development** | 30% | Vector Search, embeddings, retrieval evaluation |

## Pré-requisitos

- Workspace Databricks com Unity Catalog
- Acesso à tabela `sandbox.nasa_gcn_dev.gcn_circulars`
- Permissão para criar Vector Search endpoints

## Estrutura do Lab

```
lab-03-chunking-indexing/
├── 01-extract-circulars.py    # Extração e filtragem de dados
├── 02-chunking.py             # Estratégias de chunking
├── 03-embeddings-vector-search.py  # Embeddings e Vector Search
└── README.md                  # Este arquivo
```

## Notebooks

### 1. Extract Circulars (`01-extract-circulars.py`)

**Duração:** ~15 minutos

**O que você vai aprender:**
- Conectar à camada Silver do NASA GCN
- Explorar estrutura dos GCN Circulars
- Aplicar filtros de qualidade (tamanho mínimo/máximo)
- Preparar dataset para chunking

**Output:** Tabela `gcn_circulars_prepared`

### 2. Chunking (`02-chunking.py`)

**Duração:** ~30 minutos

**O que você vai aprender:**
- Chunking por caracteres (simples, com overlap)
- Chunking por sentenças (regex - compatível com serverless)
- Chunking por parágrafos (semântico)
- **Comparar estratégias COM vs SEM overlap** e avaliar trade-offs
- **Analisar impacto do tamanho do chunk** (200, 400, 600, 800 chars)
- Estimar tokens para custo de embedding
- Conceitos-chave para o exame de certificação

**Output:** Tabela `gcn_circulars_chunks`

**Nota:** Usamos regex ao invés de NLTK para compatibilidade com clusters serverless.

### 3. Embeddings & Vector Search (`03-embeddings-vector-search.py`)

**Duração:** ~25 minutos

**O que você vai aprender:**
- Criar Vector Search endpoint
- Configurar Delta Sync index
- Gerar embeddings com `databricks-bge-large-en`
- Testar retrieval semântico
- Avaliar qualidade do retrieval

**Output:** Vector Search index `gcn_chunks_vs_index`

## Comandos Úteis

### Verificar tabelas criadas
```sql
SHOW TABLES IN sandbox.nasa_gcn_dev LIKE 'gcn_circulars*';
```

### Sincronizar índice manualmente
```python
from databricks.vector_search.client import VectorSearchClient
vsc = VectorSearchClient()
index = vsc.get_index("nasa_gcn_vs_endpoint", "sandbox.nasa_gcn_dev.gcn_chunks_vs_index")
index.sync()
```

### Testar retrieval
```python
index.similarity_search(
    query_text="gamma-ray burst observation",
    columns=["chunk_id", "event_id", "chunk_text"],
    num_results=5
)
```

## Recursos Criados

| Recurso | Nome Completo | Tipo |
|---------|---------------|------|
| Tabela preparada | `sandbox.nasa_gcn_dev.gcn_circulars_prepared` | Delta Table |
| Tabela de chunks | `sandbox.nasa_gcn_dev.gcn_circulars_chunks` | Delta Table (CDC enabled) |
| VS Endpoint | `nasa_gcn_vs_endpoint` | Vector Search Endpoint |
| VS Index | `sandbox.nasa_gcn_dev.gcn_chunks_vs_index` | Delta Sync Index |
| Config | `sandbox.nasa_gcn_dev.rag_config` | Delta Table |

## Parâmetros de Chunking

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| Estratégia | Sentence-based | Preserva contexto semântico |
| Max chunk size | 500 chars | ~125 tokens, bom para contexto |
| Overlap | 1 sentença | Evita perda de contexto em bordas |
| Min doc size | 100 chars | Filtra documentos muito curtos |

## Próximos Passos

Após completar este lab, continue para:

- **Lab 4: RAG App** - Construir aplicação de Q&A
- **Lab 5: Deployment** - Deploy do modelo como endpoint

## Troubleshooting

### Erro: "Endpoint not found"
```python
# Criar endpoint manualmente
vsc.create_endpoint(name="nasa_gcn_vs_endpoint", endpoint_type="STANDARD")
```

### Erro: "Change Data Feed not enabled"
```sql
ALTER TABLE sandbox.nasa_gcn_dev.gcn_circulars_chunks
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

### Índice não sincroniza
```python
# Verificar status
index_info = vsc.get_index("nasa_gcn_vs_endpoint", "sandbox.nasa_gcn_dev.gcn_chunks_vs_index")
print(index_info.get("status"))

# Forçar sync
index.sync()
```

## Referências

- [Databricks Vector Search Documentation](https://docs.databricks.com/en/generative-ai/vector-search.html)
- [Chunking Strategies for RAG](https://docs.databricks.com/en/generative-ai/tutorials/ai-cookbook/fundamentals-data-pipeline.html)
- [GCN Circulars Archive](https://gcn.gsfc.nasa.gov/gcn3_archive.html)
