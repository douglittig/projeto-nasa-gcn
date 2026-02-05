# NASA GCN Labs - Plano de Adaptação dos Labs da Certificação

Este documento mapeia os labs originais da certificação Databricks GenAI Engineer para os dados da camada Silver do NASA GCN.

---

## Resumo dos Dados NASA GCN Disponíveis (Silver Layer)

| Tabela Silver | Conteúdo | Melhor Para | document_text |
|---------------|----------|-------------|---------------|
| `gcn_circulars` | Relatórios científicos escritos por astrônomos | **RAG textual**, Q&A científico | ✅ Formatado |
| `gcn_notices` | Alertas JSON de múltiplas missões (IceCube, Fermi, Swift) | Alertas estruturados, filtros | ✅ Formatado |
| `igwn_gwalert` | Alertas de ondas gravitacionais (LIGO/Virgo) | Classificação, probabilidades | ✅ Formatado |
| `gcn_classic_text` | Alertas legados em texto puro | Parsing de texto | ✅ Formatado |
| `gcn_classic_binary` | Dados binários parseados (160 bytes) | Dados estruturados, coordenadas | ❌ Numérico |
| `gcn_classic_voevent` | XML VOEvent | XML parsing, metadados | ⚠️ Parcial |

**Tabela principal para RAG: `gcn_circulars`** - Contém texto científico rico (~15k documentos)

---

## Mapeamento: Labs Originais → Labs NASA GCN

### Lab 2: Multi-Agent Workflow

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Insurance Claims Processing | **Tema:** GCN Alert Triage System |
| **Dados:** Claims table (synthetic) | **Dados:** `gcn_notices` + `gcn_circulars` |
| **Agentes:** extract_claim, validate_policy, assess_damage, finalize | **Agentes:** `classify_event`, `correlate_notices`, `summarize_circular`, `generate_report` |

**Cenário NASA:**
```
Input: Novo alerta de neutrino do IceCube
  ↓
Agent 1: classify_event() → Determina tipo (GRB, Supernova, etc.)
  ↓
Agent 2: correlate_notices() → Busca alertas correlatos (mesmo RA/Dec, ±1h)
  ↓
Agent 3: summarize_circular() → Resume circulars relacionados
  ↓
Agent 4: generate_report() → Gera relatório consolidado para astrônomos
```

---

### Lab 3: Chunking & Indexing for RAG

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Medical Documents (CDC/WHO PDFs) | **Tema:** GCN Circulars Scientific Reports |
| **Dados:** PDF files | **Dados:** `gcn_circulars.body` (texto) |
| **Chunking:** 200 words, 50 overlap | **Chunking:** 150 words, 30 overlap (textos mais curtos) |

**Cenário NASA:**
```sql
-- Source data
SELECT circular_id, event_id, subject, body, document_text, word_count
FROM sandbox.nasa_gcn_dev.gcn_circulars
WHERE word_count > 50  -- Filtrar muito curtos
```

**Pipeline:**
1. Extrair `body` dos circulars
2. Chunk com sentence tokenizer (NLTK)
3. Gerar embeddings com `databricks-bge-large-en`
4. Indexar no Vector Search

---

### Lab 4: Building Retrieval-Augmented GenAI App

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Enterprise Policy Q&A | **Tema:** Astronomical Event Q&A |
| **Perguntas:** "What is the vacation policy?" | **Perguntas:** "What caused GRB 251208B?" |
| **Retriever:** Vector Search on policies | **Retriever:** Vector Search on circulars |

**Cenário NASA - Perguntas de Exemplo:**
```
Q: "What observations were made for GRB 251208B?"
Q: "Which instruments detected the neutrino event on December 25?"
Q: "What is the significance of the S190425z gravitational wave?"
Q: "Were there any optical counterparts to the IceCube alert?"
```

**Prompt Template:**
```python
PROMPT = """You are an astrophysics assistant. Answer questions about astronomical events
using ONLY the provided GCN Circulars context.

Context from GCN Circulars:
{context}

Question: {question}

If the context doesn't contain the answer, say "I don't have information about this event
in the available GCN Circulars."
"""
```

---

### Lab 5: End-to-End RAG System Deployment

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Enterprise RAG Deployment | **Tema:** NASA GCN Event Assistant Deployment |
| **Model:** PyFunc RAG | **Model:** `NASAGCNAssistant` PyFunc |
| **Endpoint:** Generic RAG | **Endpoint:** `nasa-gcn-rag-assistant` |

**Arquitetura:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Model Serving Endpoint                    │
│                   nasa-gcn-rag-assistant                     │
├─────────────────────────────────────────────────────────────┤
│  NASAGCNAssistant (MLflow PyFunc)                           │
│  ├── load_context(): Initialize VS client                   │
│  ├── predict():                                             │
│  │   ├── 1. Retrieve relevant circulars from Vector Search  │
│  │   ├── 2. Build context with event metadata               │
│  │   ├── 3. Generate answer with DBRX/Llama                 │
│  │   └── 4. Return with source citations                    │
│  └── Circuit breaker for resilience                         │
├─────────────────────────────────────────────────────────────┤
│  Vector Search Index: gcn_circulars_vs_index                │
│  Source Table: sandbox.nasa_gcn_dev.gcn_circulars           │
└─────────────────────────────────────────────────────────────┘
```

---

### Lab 6: Model Management with MLflow & Unity Catalog

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Model versioning & governance | **Tema:** NASA GCN RAG Model Governance |
| **Aliases:** Champion/Challenger | **Aliases:** `production`, `staging`, `archived` |
| **Artifacts:** Evaluation evidence | **Artifacts:** Sample Q&A pairs, latency metrics |

**Cenário NASA:**
```python
# Register model to Unity Catalog
mlflow.register_model(
    model_uri=f"runs:/{run_id}/nasa_gcn_rag",
    name="sandbox.nasa_gcn_models.gcn_event_assistant"
)

# Set alias
client.set_registered_model_alias(
    name="sandbox.nasa_gcn_models.gcn_event_assistant",
    alias="production",
    version=3
)
```

**Evaluation Dataset:**
```python
eval_data = [
    {"question": "What caused GRB 251208B?", "ground_truth": "Fermi GBM triggered..."},
    {"question": "What is S190425z?", "ground_truth": "Gravitational wave event..."},
    {"question": "IceCube neutrino energy?", "ground_truth": "High-energy neutrino..."},
]
```

---

### Lab 7: AI Guardrails

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Healthcare PII Masking | **Tema:** Astronomer PII Protection |
| **PII Types:** SSN, Email, Phone | **PII Types:** Email, Institution, Author name |
| **Source:** Synthetic patient data | **Source:** `gcn_circulars.submitter` field |

**Cenário NASA - PII nos Circulars:**
```
Original: "A. von Kienlin at MPE <azk@mpe.mpg.de> reports..."
Masked:   "[AUTHOR] at [INSTITUTION] <[EMAIL]> reports..."
```

**Guardrails Específicos:**
1. **Email Masking:** Regex para emails de astrônomos
2. **Institution Detection:** Universidades, observatórios
3. **Prompt Injection Protection:** Detectar tentativas de extração de dados sensíveis
4. **Rate Limiting:** Limitar queries por usuário

---

### Lab 8: LLM Evaluation & Monitoring

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Generic LLM Monitoring | **Tema:** NASA GCN RAG Performance Monitoring |
| **Metrics:** Latency, tokens | **Metrics:** Latency, retrieval precision, answer accuracy |
| **Alerts:** Generic thresholds | **Alerts:** Event-specific quality degradation |

**Métricas NASA-Específicas:**
```python
metrics = {
    "retrieval_precision": "% of relevant circulars retrieved",
    "answer_grounding": "% answers grounded in context",
    "event_coverage": "% event types correctly handled",
    "avg_context_length": "Average tokens in retrieved context",
    "citation_accuracy": "% correct source citations"
}
```

**Dashboard:**
```sql
-- Query inference table for monitoring
SELECT
    DATE(timestamp) as date,
    AVG(latency_ms) as avg_latency,
    COUNT(*) as total_requests,
    SUM(CASE WHEN response LIKE '%I don''t have information%' THEN 1 ELSE 0 END) as fallback_count
FROM inference_logs.nasa_gcn_rag_assistant
GROUP BY DATE(timestamp)
```

---

### Lab 9: Vector Search & Retrieval Optimization

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Technical Docs Retrieval | **Tema:** GCN Circulars Retrieval Optimization |
| **Optimization:** Batch size, embedding dim | **Optimization:** Event-type filtering, temporal decay |

**Otimizações Específicas NASA:**
1. **Filtro por Tipo de Evento:** Pre-filter por `event_type` (GRB, GW, SN)
2. **Temporal Decay:** Priorizar circulars mais recentes para eventos ativos
3. **Multi-Index Strategy:** Índices separados por missão (Fermi, IceCube, LIGO)
4. **Hybrid Search:** Combinar keyword (event_id) + semantic (body)

**Benchmark:**
```python
test_queries = [
    {"query": "GRB 251208B optical observations", "expected_ids": [43046, 43047]},
    {"query": "IceCube neutrino energy spectrum", "expected_ids": [...]}
]
```

---

### Lab 10: GenAI Readiness Assessment

| Original | NASA GCN Adaptado |
|----------|-------------------|
| **Tema:** Enterprise Readiness Checklist | **Tema:** NASA GCN RAG Production Readiness |
| **Assessment:** Generic checklist | **Assessment:** Astronomy-specific requirements |

**Checklist NASA GCN:**

| Categoria | Item | Status |
|-----------|------|--------|
| **Data Quality** | Circulars têm `document_text` formatado | ✅ |
| **Data Quality** | Eventos têm coordenadas válidas (RA/Dec) | ✅ |
| **Vector Search** | Índice criado e sincronizado | ⏳ |
| **Model Serving** | Endpoint deployed com auth | ⏳ |
| **Guardrails** | PII masking implementado | ⏳ |
| **Monitoring** | Inference logging ativo | ⏳ |
| **Evaluation** | Ground truth dataset criado | ⏳ |
| **Governance** | Modelo registrado no Unity Catalog | ⏳ |

---

## Estrutura Proposta dos Labs

```
labs/
├── lab-02-multi-agent-triage/
│   ├── 01-setup.py
│   ├── 02-agents.py
│   └── 03-orchestration.py
├── lab-03-chunking-indexing/
│   ├── 01-extract-circulars.py
│   ├── 02-chunking.py
│   └── 03-embeddings.py
├── lab-04-rag-app/
│   ├── 01-retriever.py
│   ├── 02-rag-chain.py
│   └── 03-evaluation.py
├── lab-05-deployment/
│   ├── 01-pyfunc-model.py
│   ├── 02-deploy-endpoint.py
│   └── 03-test-endpoint.py
├── lab-06-model-management/
│   ├── 01-register-model.py
│   ├── 02-versioning.py
│   └── 03-aliases.py
├── lab-07-guardrails/
│   ├── 01-pii-detection.py
│   ├── 02-masking.py
│   └── 03-audit-logging.py
├── lab-08-monitoring/
│   ├── 01-inference-tables.py
│   ├── 02-metrics-dashboard.py
│   └── 03-alerting.py
├── lab-09-vector-optimization/
│   ├── 01-batch-embeddings.py
│   ├── 02-index-tuning.py
│   └── 03-benchmarking.py
└── lab-10-readiness/
    ├── 01-checklist.py
    ├── 02-simulation.py
    └── 03-report.py
```

---

## Próximos Passos

1. [ ] Criar estrutura de pastas `labs/`
2. [ ] Implementar Lab 3 (Chunking) - Fundação para os outros
3. [ ] Implementar Lab 4 (RAG App) - Core functionality
4. [ ] Implementar Lab 5 (Deployment) - Production path
5. [ ] Adicionar Labs 7-10 (Governance, Monitoring)
6. [ ] Lab 2 (Multi-Agent) por último - mais complexo

---

*Última atualização: Fevereiro 2026*
