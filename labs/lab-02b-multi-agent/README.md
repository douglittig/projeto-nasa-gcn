# Lab 2B: Multi-Agent Workflows with LangChain

Este lab implementa workflows multi-agente usando LangChain e LangGraph para processar GCN Circulars com agentes especializados.

## Objetivos de Aprendizado

Apos completar este lab, voce sera capaz de:

1. **Projetar workflows multi-estagio** com agentes especializados
2. **Implementar prompt-task alignment** para cada etapa do pipeline
3. **Criar tools** que agentes podem invocar dinamicamente
4. **Usar LangGraph** para orquestracao de agentes
5. **Aplicar ReAct pattern** (Reasoning + Acting)

## Topicos do Exame Cobertos

| Secao | Peso | Topicos |
|-------|------|---------|
| **Section 1: Design** | 22% | Multi-stage workflows, prompt-task alignment, tool composition |
| **Section 3: Application Development** | 30% | LangChain agents, tool ordering, modular design |

## Pre-requisitos

- Workspace Databricks com Foundation Model APIs
- Tabela `sandbox.nasa_gcn_dev.gcn_circulars` disponivel
- Acesso ao modelo `databricks-meta-llama-3-1-70b-instruct`

## Estrutura do Lab

```
lab-02b-multi-agent/
├── 01-multi-agent-workflow.py   # Workflow completo com 4 agentes
└── README.md                    # Este arquivo
```

## Notebooks

### 1. Multi-Agent Workflow (`01-multi-agent-workflow.py`)

**Duracao:** ~40 minutos

**O que voce vai aprender:**
- Definir tools com `@tool` decorator
- Criar prompts estruturados para cada estagio
- Usar `create_agent` para orquestracao
- Implementar workflow de analise de GCN

**Workflow implementado:**

```
GCN Circular Input
       |
       v
+------------------+
| 1. EXTRACTION    |  Extrair campos estruturados
|    Agent         |  (event_type, coordinates, instruments)
+--------+---------+
         |
         v
+------------------+
| 2. VALIDATION    |  Validar dados extraidos
|    Agent         |  (formato, ranges, completude)
+--------+---------+
         |
         v
+------------------+
| 3. ENRICHMENT    |  Enriquecer com context adicional
|    Agent         |  (classificar evento, calcular distancia)
+--------+---------+
         |
         v
+------------------+
| 4. SUMMARY       |  Gerar resumo estruturado
|    Agent         |  para consumo downstream
+------------------+
```

## Conceitos-Chave para o Exame

### Prompt-Task Alignment

Cada agente deve ter um prompt especializado para sua tarefa:

| Agente | Task Type | Prompt Focus |
|--------|-----------|--------------|
| Extraction | Information Extraction | Structured output, field mapping |
| Validation | Classification | Pass/Fail criteria, error messages |
| Enrichment | Reasoning | Domain knowledge, calculations |
| Summary | Generation | Concise format, key highlights |

### Tool Composition

```python
@tool
def extract_coordinates(text: str) -> dict:
    """Extract RA/Dec coordinates from GCN text."""
    # Agente decide quando chamar esta tool
    ...
```

### ReAct Pattern

```
1. REASON: Analisar input e decidir proxima acao
2. ACT: Invocar tool apropriada
3. OBSERVE: Processar resultado da tool
4. REPEAT: Continuar ate completar tarefa
```

## Arquitetura Multi-Agente

```
┌─────────────────────────────────────────────────────────────┐
│                    NASA GCN Multi-Agent System               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ORCHESTRATOR (LangGraph)                 │   │
│  │                                                       │   │
│  │  Input: GCN Circular Text                            │   │
│  │                                                       │   │
│  │  ┌─────────────┐    ┌─────────────┐                  │   │
│  │  │ Extraction  │───▶│ Validation  │                  │   │
│  │  │   Agent     │    │   Agent     │                  │   │
│  │  │             │    │             │                  │   │
│  │  │ Tools:      │    │ Tools:      │                  │   │
│  │  │ - extract_  │    │ - validate_ │                  │   │
│  │  │   coords    │    │   coords    │                  │   │
│  │  │ - extract_  │    │ - validate_ │                  │   │
│  │  │   event     │    │   format    │                  │   │
│  │  └─────────────┘    └──────┬──────┘                  │   │
│  │                            │                          │   │
│  │                            ▼                          │   │
│  │  ┌─────────────┐    ┌─────────────┐                  │   │
│  │  │  Summary    │◀───│ Enrichment  │                  │   │
│  │  │   Agent     │    │   Agent     │                  │   │
│  │  │             │    │             │                  │   │
│  │  │ Tools:      │    │ Tools:      │                  │   │
│  │  │ - format_   │    │ - classify_ │                  │   │
│  │  │   summary   │    │   event     │                  │   │
│  │  │ - highlight │    │ - lookup_   │                  │   │
│  │  │   key_facts │    │   catalog   │                  │   │
│  │  └─────────────┘    └─────────────┘                  │   │
│  │                                                       │   │
│  │  Output: Structured Analysis Result                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Recursos Criados

| Recurso | Nome | Descricao |
|---------|------|-----------|
| Table | `gcn_agent_analysis` | Resultados das analises |
| MLflow Experiment | `nasa_gcn_multi_agent` | Tracking de execucoes |

## Comandos Uteis

### Inicializar LLM
```python
from langchain_community.chat_models import ChatDatabricks

llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0
)
```

### Criar Tool
```python
from langchain_core.tools import tool

@tool
def extract_event_type(text: str) -> str:
    """Extract event type (GRB, GW, Neutrino) from GCN text."""
    # Implementation
    ...
```

### Criar Agente
```python
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=[extract_event_type, extract_coordinates],
    system_prompt="You are a GCN analysis specialist..."
)
```

## Boas Praticas

1. **Separation of Concerns**: Cada agente tem uma responsabilidade clara
2. **Composability**: Tools podem ser reutilizadas entre agentes
3. **Testability**: Cada componente pode ser testado independentemente
4. **Observability**: Logging verbose para debugging
5. **Scalability**: Design stateless para processamento paralelo

## Troubleshooting

### Agente nao chama tool esperada
- Verifique docstring da tool (agente usa para decidir)
- Ajuste system prompt para ser mais diretivo
- Reduza temperatura para 0

### Timeout nas execucoes
- Limite numero de iteracoes do agente
- Use `max_iterations` parameter
- Simplifique prompts

### Respostas inconsistentes
- Use structured output com Pydantic
- Adicione few-shot examples no prompt
- Force format com output parser

## Proximos Passos

Apos completar este lab, continue para:

- **Lab 3: Chunking & Indexing** - Preparar dados para RAG
- **Lab 4: RAG App** - Construir aplicacao de Q&A

## Referencias

- [LangChain Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Databricks Foundation Models](https://docs.databricks.com/en/machine-learning/foundation-models/index.html)

---

*Ultima atualizacao: Fevereiro 2026*
