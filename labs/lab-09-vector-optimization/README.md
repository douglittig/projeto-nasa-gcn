# Lab 9: Vector Search & Retrieval Optimization

Este lab explora técnicas de otimização para Vector Search e retrieval em aplicações RAG.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Comparar modelos de embedding** e selecionar o mais adequado
2. **Configurar índices** para balance entre latência e qualidade
3. **Implementar filtros eficientes** para retrieval
4. **Executar benchmarks** de retrieval com métricas padrão

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 3: Application Development** | 30% | Embedding models, Vector Search config |
| **Section 4: Evaluation and Monitoring** | 18% | Retrieval metrics, benchmarking |

## Pré-requisitos

- Lab 3 completo (Vector Search index criado)
- Tabela `gcn_circulars_chunks` populada
- Acesso aos modelos de embedding do Databricks

## Estrutura do Lab

```
lab-09-vector-optimization/
├── 01-embedding-strategies.py   # Comparação de modelos de embedding
├── 02-index-tuning.py           # Configuração do índice
├── 03-benchmarking.py           # Benchmark de retrieval
└── README.md                    # Este arquivo
```

## Notebooks

### 1. Embedding Strategies (`01-embedding-strategies.py`)

**O que você vai aprender:**
- Modelos de embedding disponíveis no Databricks
- Batch processing para eficiência
- Comparação de qualidade (similaridade de cosseno)
- Trade-offs de performance

**Modelos comparados:**
| Modelo | Dimensões | Uso |
|--------|-----------|-----|
| databricks-bge-large-en | 1024 | Produção |
| databricks-gte-large-en | 1024 | Geral |
| databricks-e5-large-v2 | 1024 | Assimétrico |

### 2. Index Tuning (`02-index-tuning.py`)

**O que você vai aprender:**
- Tipos de índice (DELTA_SYNC vs DIRECT_ACCESS)
- Pipeline types (TRIGGERED vs CONTINUOUS)
- Estratégias de filtragem eficientes
- Sincronização e manutenção

**Configurações recomendadas:**
```python
{
    "index_type": "DELTA_SYNC",
    "pipeline_type": "TRIGGERED",
    "embedding_model": "databricks-bge-large-en",
    "recommended_k": 5
}
```

### 3. Benchmarking (`03-benchmarking.py`)

**O que você vai aprender:**
- Criar dataset de benchmark
- Calcular métricas de retrieval
- Comparar diferentes valores de K
- Gerar recomendações baseadas em dados

**Métricas implementadas:**
| Métrica | Descrição |
|---------|-----------|
| Keyword Precision | % keywords esperadas encontradas |
| Event Prefix Match | % resultados com tipo correto |
| MRR | Mean Reciprocal Rank |
| Latency | Tempo de resposta |

## Trade-offs de Otimização

```
                    Qualidade
                        ▲
                        │
            K=10 ●      │
                   ●    │     ● K=20
             K=7 ●      │
                        │
             K=5 ●──────┼──────────▶ Latência
                        │
             K=3 ●      │
                        │
```

### Recomendações por Caso de Uso

| Caso de Uso | K | Filtros | Latência Target |
|-------------|---|---------|-----------------|
| Alta precisão | 7-10 | Sim | <1000ms |
| Balanceado | 5 | Opcional | <500ms |
| Baixa latência | 3 | Sim | <200ms |

## Recursos Criados

| Recurso | Nome | Descrição |
|---------|------|-----------|
| Table | `embedding_benchmark_results` | Benchmark de embeddings |
| Table | `vs_optimized_config` | Configuração otimizada |
| Table | `retrieval_benchmark_results` | Benchmark de retrieval |
| Table | `retrieval_k_comparison` | Comparação por K |

## Comandos Úteis

### Gerar embeddings em batch
```python
def get_embeddings_batch(texts, model="databricks-bge-large-en", batch_size=20):
    # ...implementação
```

### Busca com filtro
```python
results = index.similarity_search(
    query_text="gamma-ray burst",
    columns=["chunk_id", "event_id", "chunk_text"],
    num_results=5,
    filters={"event_id LIKE": "GRB%"}
)
```

### Calcular MRR
```python
def calculate_mrr(results, expected_keywords):
    for i, r in enumerate(results, 1):
        if is_relevant(r, expected_keywords):
            return 1.0 / i
    return 0.0
```

## Métricas de Referência

### NASA GCN RAG (K=5)
| Métrica | Valor | Target |
|---------|-------|--------|
| Keyword Precision | >75% | >70% |
| MRR | >0.6 | >0.5 |
| Avg Latency | <400ms | <500ms |
| P95 Latency | <800ms | <1000ms |

## Boas Práticas

1. **Batch embedding**: Sempre processar em lotes (20-50 textos)
2. **Filtros indexados**: Usar colunas indexadas para filtros
3. **K apropriado**: Começar com K=5, ajustar baseado em métricas
4. **Monitorar**: Acompanhar MRR e latência em produção
5. **Delta Sync**: Usar TRIGGERED para balance custo/atualização

## Troubleshooting

### Embeddings lentos
- Aumentar batch_size
- Verificar rate limits
- Considerar cache para textos frequentes

### Baixa precisão
- Aumentar K
- Melhorar chunking (Lab 3)
- Considerar reranking

### Alta latência
- Reduzir K
- Adicionar filtros
- Verificar tamanho do índice

## Próximos Passos

Após completar este lab, continue para:

- **Lab 10: Readiness Assessment** - Checklist de produção

## Referências

- [Databricks Vector Search](https://docs.databricks.com/en/generative-ai/vector-search.html)
- [Embedding Models](https://docs.databricks.com/en/machine-learning/foundation-models/index.html)
- [Retrieval Metrics](https://www.pinecone.io/learn/retrieval-metrics/)

---

*Última atualização: Fevereiro 2026*
