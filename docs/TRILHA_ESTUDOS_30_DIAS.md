# Trilha de Estudos 30 Dias - Databricks GenAI Engineer Associate

## Metodologia: Ultralearning

Esta trilha aplica os 9 princípios do Ultralearning de Scott Young:

1. **Metalearning** - Entender a estrutura do exame antes de estudar
2. **Focus** - Sessões intensas de 90min sem distrações
3. **Directness** - Praticar no Databricks desde o Dia 1
4. **Drill** - Isolar e praticar pontos fracos
5. **Retrieval** - Testar conhecimento ativamente (não apenas reler)
6. **Feedback** - Usar practice questions como feedback loop
7. **Retention** - Revisão espaçada a cada semana
8. **Intuition** - Construir entendimento profundo via projetos
9. **Experimentation** - Variar abordagens e modelos

---

## Estrutura do Exame

| Seção | Peso | Foco Principal |
|-------|------|----------------|
| **Section 1: Design Applications** | 14% | Prompt engineering, Compound AI, Reasoning chains |
| **Section 2: Data Preparation** | 14% | Chunking, RAG data prep, Document parsing |
| **Section 3: Application Development** | 30% | Vector Search, Agents, LangChain, Embeddings |
| **Section 4: Assembling & Deploying** | 22% | MLflow, Model Serving, Pyfunc, Deployment |
| **Section 5: Governance** | 8% | Guardrails, PII, Security |
| **Section 6: Evaluation & Monitoring** | 12% | Metrics, LLM-as-Judge, Monitoring |

**Total:** 45 questões | 90 minutos | ~70% para passar | $200 USD

---

## Visão Geral das 4 Semanas

| Semana | Foco | Horas Estimadas | Insumo YouTube |
|--------|------|-----------------|----------------|
| **1** | Foundations (Sections 1-2) | 15h | 3 vídeos |
| **2** | Core Development (Section 3) | 18h | 4 vídeos |
| **3** | Deployment & Governance (Sections 4-5) | 15h | 3 vídeos |
| **4** | Evaluation, Review & Exam Prep | 12h | 2 vídeos |

---

# SEMANA 1: Foundations (Dias 1-7)

## Dia 1: Metalearning & Setup

### Objetivos
- [ ] Entender estrutura completa do exame
- [ ] Configurar ambiente Databricks
- [ ] Mapear gaps de conhecimento

### Estudo (2h)
1. **Ler** (45min): `00-OReilly-Book/1.-Exam-Details-and-Resources.md`
2. **Explorar** (30min): Exam Guide PDF
3. **Setup** (45min):
   - Criar workspace Databricks
   - Testar conexão com MLflow
   - Verificar acesso ao Vector Search

### Retrieval Test
Sem consulta, responda:
1. Quais são as 6 seções do exame e seus pesos?
2. Qual seção tem maior peso?
3. Qual é o tempo e número de questões?

### Insumo YouTube
**Tema:** "Guia Completo: Certificação Databricks GenAI Engineer"
- Estrutura do exame
- Recursos de estudo
- Dicas de preparação

---

## Dia 2: Prompt Engineering Fundamentals

### Objetivos
- [ ] Dominar zero-shot, few-shot e chain-of-thought
- [ ] Criar prompts estruturados
- [ ] Entender task types (classification, extraction, transformation)

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section1/01-Prompt-Engineering-Fundamentals.md`
   - `00-OReilly-Book/2.-Designing-Generative-AI-Applications.md` (seção Crafting Prompts)

2. **Praticar** (60min): No Databricks notebook, implementar:
   ```python
   # Zero-shot
   prompt_zero = "Classify the sentiment: 'Great product!'"

   # Few-shot
   prompt_few = """
   Example 1: "Love it!" -> Positive
   Example 2: "Terrible!" -> Negative
   Classify: "Amazing service!" ->
   """

   # Chain-of-thought
   prompt_cot = """
   Question: Is this compliant?
   Let's think step by step:
   1. First, identify the regulation...
   """
   ```

3. **Watch DEMO** (30min): `DEMO-01-Deconstruct-Plan-Use-Case.md`

### Drill: Task Type Matching
Para cada use case, identifique o task type correto:
| Use Case | Task Type |
|----------|-----------|
| Resumir relatório financeiro | ? |
| Extrair ICD-10 de nota médica | ? |
| Classificar ticket como billing/technical | ? |
| Converter query para SQL | ? |

**Respostas:** Text Generation, Extraction, Classification, Transformation

### Flashcards para Anki
1. **Q:** O que é few-shot prompting? **A:** Fornecer exemplos no prompt para guiar o modelo
2. **Q:** Quando usar chain-of-thought? **A:** Para tarefas que requerem raciocínio multi-step
3. **Q:** Qual a diferença entre extraction e classification? **A:** Extraction extrai campos estruturados; Classification atribui categorias

---

## Dia 3: Compound AI Systems & Reasoning Chains

### Objetivos
- [ ] Entender arquitetura de Compound AI Systems
- [ ] Implementar reasoning chains com LangChain
- [ ] Diferenciar chains estáticas vs agents dinâmicos

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section1/01-Introduction-Compound-AI.md`
   - `Section1/02-Multi-stage-Reasoning-Chains.md`
   - `Section1/03-Designing-Compound-AI-Systems.md`

2. **Praticar** (60min): Implementar no Databricks:
   ```python
   from langchain.prompts import PromptTemplate
   from langchain.chains import LLMChain, SimpleSequentialChain

   # Chain 1: Extract key terms
   extract_prompt = PromptTemplate.from_template(
       "Extract financial terms from: {input}"
   )
   extract_chain = LLMChain(llm=llm, prompt=extract_prompt)

   # Chain 2: Summarize
   summary_prompt = PromptTemplate.from_template(
       "Summarize implications of: {input}"
   )
   summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

   # Sequential chain
   pipeline = SimpleSequentialChain(
       chains=[extract_chain, summary_chain]
   )
   ```

3. **Watch DEMO** (30min): `DEMO-01-Building-Reasoning-Chain.md`

### Drill: Design Exercise
Desenhe um pipeline para um "Insurance Claim Validator":
1. Document Parser (OCR)
2. Claim Classifier (medical/auto/property)
3. Policy Validator
4. Resolution Generator

### Insumo YouTube
**Tema:** "Compound AI Systems na Prática"
- O que são sistemas compostos
- Quando usar chains vs agents
- Demo: Pipeline de validação de claims

---

## Dia 4: RAG Architecture & Data Preparation

### Objetivos
- [ ] Entender arquitetura RAG completa
- [ ] Dominar Context Engineering
- [ ] Preparar dados para RAG

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section2/01-RAG-Architecture-Introduction.md`
   - `Section2/02-Context-Engineering.md`
   - `00-OReilly-Book/3.-Preparing-and-Chunking-Data-for-RAG-Applications.md` (primeiras seções)

2. **Lab NASA GCN** (90min): Executar `lab-03-chunking-indexing/01-extract-circulars.py`
   - Conectar à tabela `gcn_circulars`
   - Explorar estrutura dos dados
   - Aplicar filtros de qualidade

### Conceitos-Chave
```
RAG Pipeline:
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   User      │ → │  Retriever  │ → │    LLM      │
│   Query     │   │  (Vector    │   │  (Generate  │
│             │   │   Search)   │   │   Answer)   │
└─────────────┘   └─────────────┘   └─────────────┘
                         ↑
                  ┌─────────────┐
                  │  Document   │
                  │   Store     │
                  │  (Chunks +  │
                  │  Embeddings)│
                  └─────────────┘
```

### Flashcards
1. **Q:** O que é RAG? **A:** Retrieval-Augmented Generation - combina busca + geração
2. **Q:** Por que chunking é importante? **A:** LLMs têm limite de contexto; chunks permitem retrieval granular
3. **Q:** O que é context window? **A:** Quantidade máxima de tokens que o modelo processa

---

## Dia 5: Chunking Strategies Deep Dive

### Objetivos
- [ ] Dominar 5 estratégias de chunking
- [ ] Entender trade-offs de granularidade e overlap
- [ ] Implementar chunking no projeto NASA GCN

### Estudo (2.5h)
1. **Ler** (45min):
   - `Section2/03-Document-Parsing-Chunking.md`
   - `00-OReilly-Book/3.-Preparing-and-Chunking-Data-for-RAG-Applications.md` (seção Chunking Strategies)

2. **Lab NASA GCN** (90min): Executar `lab-03-chunking-indexing/02-chunking.py`
   - Implementar chunking por caracteres
   - Implementar chunking por sentenças
   - Comparar estratégias

3. **Análise** (15min): Documentar resultados no notebook

### Tabela de Estratégias de Chunking

| Estratégia | Melhor Para | Prós | Contras |
|------------|-------------|------|---------|
| **Fixed-Length** | Logs, dados estruturados | Simples, rápido | Pode quebrar contexto |
| **Sentence-Level** | FAQs, artigos | Preserva gramática | Contexto limitado |
| **Paragraph-Based** | Reports, blogs | Legível, fácil | Tamanhos inconsistentes |
| **Sliding Window** | QA, documentos legais | Mantém continuidade | Mais recursos |
| **Semantic** | Transcrições, livros | Adaptativo, significativo | Complexo implementar |

### Drill: Escolha a Estratégia
| Documento | Melhor Estratégia | Por quê? |
|-----------|-------------------|----------|
| Server logs | ? | ? |
| Contrato legal | ? | ? |
| FAQ de produto | ? | ? |
| Transcrição de reunião | ? | ? |

### Insumo YouTube
**Tema:** "Chunking para RAG: O Guia Definitivo"
- 5 estratégias explicadas
- Quando usar cada uma
- Demo com dados NASA GCN

---

## Dia 6: Content Filtering & Document Extraction

### Objetivos
- [ ] Filtrar ruído e redundância de documentos
- [ ] Extrair texto de PDFs e imagens
- [ ] Converter para formato Delta

### Estudo (2h)
1. **Ler** (45min):
   - `DEMO-01-Preparing-Data-for-RAG.md`
   - O'Reilly Chapter 3: Content Filtering and Extraction

2. **Praticar** (75min):
   ```python
   import re

   def clean_text(text):
       # Remove HTML tags
       text = re.sub(r'<[^>]+>', '', text)
       # Remove footers
       text = re.sub(r'Page \d+ of \d+', '', text)
       # Remove timestamps
       text = re.sub(r'Last updated: .*?\n', '', text)
       return text

   # Extrair de PDF
   from PyPDF2 import PdfReader
   reader = PdfReader("document.pdf")
   text = "".join([page.extract_text() for page in reader.pages])

   # Salvar em Delta
   df.write.format("delta").mode("overwrite").save("/mnt/delta/chunks")
   ```

### Retrieval Test
1. Quais são as fontes comuns de ruído em documentos?
2. Qual biblioteca usar para OCR em imagens?
3. Por que usar Delta Lake para armazenar chunks?

---

## Dia 7: Revisão Semanal + Practice Questions

### Objetivos
- [ ] Consolidar aprendizado da semana
- [ ] Identificar gaps
- [ ] Resolver practice questions

### Revisão (1.5h)
1. **Revisão Espaçada** (30min): Revisar flashcards dos dias 2-6
2. **Resumo Visual** (30min): Criar mapa mental de Section 1-2
3. **Practice Questions** (30min): Resolver questões do O'Reilly Chapter 2-3

### Practice Questions - Section 1 & 2

**Q1.** What is the main purpose of using a PromptTemplate in LangChain?
- A. Speed up LLM inference
- B. Control token length
- C. Define reusable, parameterized prompts ✓
- D. Deploy models to REST API

**Q2.** Which chunking strategy preserves context across boundaries?
- A. Fixed-length
- B. Sentence-level
- C. Sliding window ✓
- D. Paragraph-based

**Q3.** What causes retrieval gaps in RAG systems?
- A. Ineffective chunking ✓
- B. Too many documents
- C. Fast query processing
- D. High precision scores

### Auto-Avaliação Semanal
| Tópico | Confiança (1-5) | Ação se < 4 |
|--------|-----------------|-------------|
| Prompt Engineering | _ | Reler Day 2 |
| Compound AI Systems | _ | Reler Day 3 |
| RAG Architecture | _ | Reler Day 4 |
| Chunking Strategies | _ | Refazer Lab 03 |
| Content Filtering | _ | Reler Day 6 |

---

# SEMANA 2: Application Development - Section 3 (Dias 8-14)

*Esta é a seção mais importante: 30% do exame!*

## Dia 8: Vector Search Fundamentals

### Objetivos
- [ ] Entender arquitetura do Mosaic AI Vector Search
- [ ] Criar e configurar Vector Search endpoint
- [ ] Dominar tipos de índices (Delta Sync, Direct Access)

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section3/01-Mosaic-AI-Vector-Search.md`
   - `Section3/02-Vector-Store-Algorithms.md`

2. **Lab NASA GCN** (90min): Executar `lab-03-chunking-indexing/03-embeddings-vector-search.py`
   - Criar Vector Search endpoint
   - Configurar Delta Sync index
   - Testar similarity search

### Conceitos-Chave
```python
from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

# Criar endpoint
vsc.create_endpoint(name="nasa_gcn_vs_endpoint", endpoint_type="STANDARD")

# Criar índice Delta Sync
vsc.create_delta_sync_index(
    endpoint_name="nasa_gcn_vs_endpoint",
    index_name="gcn_chunks_vs_index",
    source_table_name="sandbox.nasa_gcn_dev.gcn_circulars_chunks",
    primary_key="chunk_id",
    embedding_source_column="chunk_text",
    embedding_model_endpoint_name="databricks-bge-large-en"
)
```

### Flashcards
1. **Q:** Diferença entre Delta Sync e Direct Access index? **A:** Delta Sync sincroniza automaticamente com Delta Table; Direct Access requer upserts manuais
2. **Q:** O que é HNSW? **A:** Hierarchical Navigable Small World - algoritmo de ANN para busca vetorial rápida
3. **Q:** Qual embedding model padrão do Databricks? **A:** databricks-bge-large-en

---

## Dia 9: Embeddings & Similarity

### Objetivos
- [ ] Entender modelos de embedding e dimensionalidade
- [ ] Dominar métricas de similaridade (cosine, euclidean, dot product)
- [ ] Implementar reranking para melhorar relevância

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section3/03-Embeddings-Similarity.md`
   - `DEMO-02-Building-Vector-Search.md`

2. **Praticar** (90min):
   ```python
   # Gerar embeddings
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')

   embeddings = model.encode([
       "What is a gamma-ray burst?",
       "GRBs are cosmic explosions..."
   ])

   # Calcular similaridade
   from sklearn.metrics.pairwise import cosine_similarity
   similarity = cosine_similarity([embeddings[0]], [embeddings[1]])

   # Reranking com cross-encoder
   from transformers import pipeline
   reranker = pipeline("text-classification",
                       model="cross-encoder/ms-marco-MiniLM-L-6-v2")
   ```

### Drill: Similarity Metrics

| Métrica | Fórmula | Melhor Para |
|---------|---------|-------------|
| Cosine | cos(θ) = A·B / (||A|| ||B||) | Textos de tamanhos diferentes |
| Euclidean | √Σ(Ai-Bi)² | Quando magnitude importa |
| Dot Product | A·B | Vetores normalizados |

### Insumo YouTube
**Tema:** "Vector Search do Zero ao Deploy no Databricks"
- Conceitos de embeddings
- Criando índices
- Demo com NASA GCN data

---

## Dia 10: Agents Fundamentals

### Objetivos
- [ ] Entender arquitetura de agents (ReAct pattern)
- [ ] Diferenciar agents de chains
- [ ] Implementar agent básico com tools

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section3/01-Introduction-Agents.md`
   - `Section3/02-Agents-Fundamentals.md`
   - O'Reilly Chapter 4: LangChain Agents Overview

2. **Lab** (90min): Implementar agent
   ```python
   from langchain.agents import initialize_agent, Tool
   from langchain.llms import OpenAI

   # Define tools
   def search_circulars(query):
       return "Found: GRB 260101A detected by Swift..."

   tools = [
       Tool(
           name="SearchCirculars",
           func=search_circulars,
           description="Search GCN circulars for astronomical events"
       )
   ]

   # Initialize agent
   agent = initialize_agent(
       tools=tools,
       llm=llm,
       agent="zero-shot-react-description",
       verbose=True
   )

   agent.run("What was detected on January 1, 2026?")
   ```

### Comparação: Chains vs Agents

| Aspecto | Chains | Agents |
|---------|--------|--------|
| Fluxo | Predefinido, estático | Dinâmico, step-by-step |
| Flexibilidade | Limitada | Alta |
| Tool Integration | Explícita | Runtime selection |
| Use Case | Tarefas previsíveis | Tarefas complexas/variáveis |

---

## Dia 11: Agent Bricks Framework

### Objetivos
- [ ] Dominar Knowledge Assistants
- [ ] Entender Multi-Agent Supervisors
- [ ] Implementar agent com Databricks tools

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section3/03-Agent-Bricks-Framework.md`
   - `DEMO-04-Building-Knowledge-Assistant-Agent-Bricks.md`

2. **Lab NASA GCN** (90min): Executar `lab-04-rag-app/01-retriever.py`
   - Criar retriever sobre Vector Search
   - Testar queries semânticas

### Agent Bricks Types

| Type | Use Case | Key Features |
|------|----------|--------------|
| **Knowledge Assistant** | Q&A sobre documentos | Vector Search + LLM |
| **Genie Space** | SQL exploration | Natural language to SQL |
| **Multi-Agent Supervisor** | Orquestração complexa | Coordena múltiplos agents |

### Prática: Knowledge Assistant
```python
# Usando Databricks SDK
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Criar Knowledge Assistant
ka = w.knowledge_assistants.create(
    name="gcn_assistant",
    vector_search_endpoint="nasa_gcn_vs_endpoint",
    vector_search_index="gcn_chunks_vs_index",
    llm_endpoint="databricks-dbrx-instruct"
)
```

---

## Dia 12: RAG Chain Implementation

### Objetivos
- [ ] Implementar RAG chain completa
- [ ] Integrar retriever + prompt + LLM
- [ ] Testar e avaliar qualidade

### Estudo (2.5h)
1. **Ler** (45min):
   - `DEMO-02-Assembling-and-Evaluating-RAG.md`
   - O'Reilly Chapter 4: Retrieval Integration with Chains

2. **Lab NASA GCN** (105min): Executar `lab-04-rag-app/02-rag-chain.py`
   - Construir RAG chain
   - Testar com queries reais
   - Avaliar respostas

### Implementação RAG Chain
```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import DatabricksVectorSearch
from langchain.chat_models import ChatDatabricks

# Setup components
vectorstore = DatabricksVectorSearch(
    endpoint="nasa_gcn_vs_endpoint",
    index_name="gcn_chunks_vs_index"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = ChatDatabricks(endpoint="databricks-dbrx-instruct")

# Build chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Query
result = qa_chain("What was GRB 260101A?")
print(result["result"])
print("Sources:", result["source_documents"])
```

### Insumo YouTube
**Tema:** "Building RAG Applications com LangChain e Databricks"
- Arquitetura RAG passo a passo
- Integration patterns
- Demo: Q&A sobre dados NASA

---

## Dia 13: Guardrails & Prompt Safety

### Objetivos
- [ ] Implementar guardrails para segurança
- [ ] Detectar e mitigar hallucinations
- [ ] Aplicar prompt augmentation

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section5/01-Securing-and-Governing-GenAI.md`
   - `DEMO-02-Implementing-Guardrails.md`
   - O'Reilly Chapter 4: Quality and Safety Mechanisms

2. **Lab NASA GCN** (90min): Executar `lab-07-guardrails/01-pii-detection.py`

### Técnicas de Segurança

| Técnica | Descrição | Exemplo |
|---------|-----------|---------|
| **Role Specification** | Define papel do modelo | "You are a factual summarizer..." |
| **Context Enrichment** | Adiciona dados verificados | Incluir fontes no prompt |
| **Output Constraints** | Limita formato de saída | "Respond in JSON with keys..." |
| **Fallback Instructions** | Comportamento quando incerto | "If unsure, say 'I don't know'" |

### Implementação Guardrails
```python
from guardrails import Guard
from guardrails.validators import ValidChoices

guard = Guard.from_string("""
output:
    type: string
    validators:
        - name: ValidChoices
          choices: ["Yes", "No", "Uncertain"]
          on_fail: filter
""")

# Validate response
response = llm.predict("Is this compliant?")
validated = guard.parse(response)
```

---

## Dia 14: Revisão Semanal + Lab Completo

### Objetivos
- [ ] Consolidar Section 3 (30% do exame!)
- [ ] Completar Lab 4 evaluation
- [ ] Resolver practice questions

### Revisão (1h)
1. Revisar flashcards da semana
2. Criar resumo visual de Vector Search + Agents + RAG

### Lab Completo (1.5h)
Executar `lab-04-rag-app/03-evaluation.py`:
- Criar evaluation dataset
- Calcular métricas de retrieval
- Documentar resultados

### Practice Questions - Section 3

**Q1.** When using LangChain agents, what advantage do they provide over fixed chains?
- A. Agents require fewer resources
- B. Agents execute only pre-defined prompts
- C. Agents dynamically select tools based on user requests ✓
- D. Agents remove the need for retrieval

**Q2.** Which retrieval approach ensures an LLM uses external knowledge for up-to-date answers?
- A. Relying solely on training data
- B. Using RAG with a vector store retriever ✓
- C. Storing conversations in buffer memory
- D. Restricting with fallback instructions

**Q3.** What is the purpose of reranking in vector search?
- A. Reduce index size
- B. Improve ranking quality using semantic scoring ✓
- C. Speed up embedding generation
- D. Filter duplicates

### Insumo YouTube
**Tema:** "Agents e Multi-Agent Systems no Databricks"
- ReAct pattern explicado
- Tools e integrations
- Demo: Agent com NASA data

---

# SEMANA 3: Deployment & Governance (Dias 15-21)

## Dia 15: MLflow Fundamentals

### Objetivos
- [ ] Dominar MLflow tracking e logging
- [ ] Entender Model Registry e versioning
- [ ] Registrar modelo no Unity Catalog

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section4/01-MLflow-for-RAG.md`
   - `Section4/03-MLflow-Agent-Development.md`
   - O'Reilly Chapter 5: MLflow Tracking and Registration

2. **Lab NASA GCN** (90min): Executar `lab-06-model-management/01-register-model.py`

### MLflow Workflow
```python
import mlflow
from mlflow.models.signature import infer_signature

with mlflow.start_run() as run:
    # Log parameters
    mlflow.log_param("retriever.top_k", 5)
    mlflow.log_param("llm.temperature", 0.1)

    # Log metrics
    mlflow.log_metric("retrieval_precision", 0.85)
    mlflow.log_metric("faithfulness", 0.92)

    # Log model
    signature = infer_signature(sample_input, sample_output)
    mlflow.pyfunc.log_model(
        artifact_path="rag_model",
        python_model=RAGModel(),
        signature=signature,
        registered_model_name="gcn_rag_model"
    )
```

### Flashcards
1. **Q:** Qual a diferença entre tracking e registry? **A:** Tracking captura experimentos; Registry gerencia versões e stages
2. **Q:** O que é model signature? **A:** Definição de input/output schema do modelo
3. **Q:** Quais são os stages no Model Registry? **A:** None, Staging, Production, Archived

---

## Dia 16: PyFunc Models & Chain Assembly

### Objetivos
- [ ] Estruturar modelo PyFunc para RAG
- [ ] Empacotar LangChain em modelo servível
- [ ] Entender artifacts e dependencies

### Estudo (2.5h)
1. **Ler** (60min):
   - O'Reilly Chapter 5: Pyfunc Model Structure
   - O'Reilly Chapter 5: LangChain Chain to Serveable Model

2. **Praticar** (90min):
   ```python
   import mlflow.pyfunc

   class RAGModelWrapper(mlflow.pyfunc.PythonModel):
       def load_context(self, context):
           # Load artifacts
           config_path = context.artifacts["rag_config"]
           self.chain = build_chain(config_path)

       def predict(self, context, model_input):
           # Pre-processing
           query = model_input["query"].iloc[0]

           # Inference
           result = self.chain.invoke({"query": query})

           # Post-processing
           return pd.DataFrame({"response": [result]})

   # Save model
   mlflow.pyfunc.save_model(
       path="rag_model",
       python_model=RAGModelWrapper(),
       artifacts={"rag_config": "/path/to/config.json"},
       conda_env="conda.yaml"
   )
   ```

### Estrutura PyFunc Model
```
rag_model/
├── MLmodel              # Metadata
├── conda.yaml           # Dependencies
├── python_model.pkl     # Serialized model class
└── artifacts/
    ├── rag_config.json  # Configuration
    └── prompt_template.txt
```

---

## Dia 17: Model Serving Deployment

### Objetivos
- [ ] Deploy para Model Serving endpoint
- [ ] Configurar autoscaling e recursos
- [ ] Testar endpoint via REST API

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section4/02-Real-Time-Deployment.md`
   - `DEMO-02-Real-Time-Deployment.md`
   - O'Reilly Chapter 5: Deploying to Model Serving Endpoints

2. **Lab NASA GCN** (90min): Executar `lab-05-deployment/02-deploy-endpoint.py`

### Deployment Flow
```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promote to Production
client.transition_model_version_stage(
    name="gcn_rag_model",
    version="1",
    stage="Production"
)

# Create serving endpoint (via REST API)
import requests

endpoint_config = {
    "name": "gcn-rag-endpoint",
    "config": {
        "served_models": [{
            "model_name": "gcn_rag_model",
            "model_version": "1",
            "workload_size": "Small",
            "scale_to_zero_enabled": True
        }]
    }
}

response = requests.post(
    f"{databricks_url}/api/2.0/serving-endpoints",
    headers={"Authorization": f"Bearer {token}"},
    json=endpoint_config
)
```

### Insumo YouTube
**Tema:** "Deploy de RAG no Databricks: Do Notebook ao Endpoint"
- MLflow tracking e registry
- PyFunc model patterns
- Demo: Deploy completo

---

## Dia 18: Model Versioning & Aliases

### Objetivos
- [ ] Gerenciar versões de modelo
- [ ] Usar aliases (champion/challenger)
- [ ] Implementar rollback strategy

### Estudo (2h)
1. **Ler** (45min):
   - `Section4/02-Model-Deployment-Fundamentals.md`
   - Lab 6 README

2. **Lab NASA GCN** (75min): Executar `lab-06-model-management/02-versioning.py` e `03-aliases.py`

### Alias Strategy
```python
from mlflow import MlflowClient

client = MlflowClient()

# Set champion alias
client.set_registered_model_alias(
    name="gcn_rag_model",
    alias="champion",
    version="2"
)

# Set challenger for A/B testing
client.set_registered_model_alias(
    name="gcn_rag_model",
    alias="challenger",
    version="3"
)

# Get model by alias
champion_uri = "models:/gcn_rag_model@champion"
model = mlflow.pyfunc.load_model(champion_uri)
```

---

## Dia 19: Governance & Security

### Objetivos
- [ ] Implementar PII detection e masking
- [ ] Configurar access controls
- [ ] Entender compliance requirements

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section5/01-Securing-and-Governing-GenAI.md`
   - `DEMO-01-Prompt-Safety.md`
   - `DEMO-03-Parse-Documents.md`

2. **Lab NASA GCN** (90min): Executar `lab-07-guardrails/02-masking.py` e `03-prompt-protection.py`

### Governance Techniques

| Técnica | Objetivo | Implementação |
|---------|----------|---------------|
| **PII Detection** | Identificar dados sensíveis | Presidio, regex patterns |
| **Masking** | Ocultar dados sensíveis | [EMAIL], [PHONE] substitution |
| **Access Control** | Limitar quem acessa | Unity Catalog permissions |
| **Audit Logging** | Rastrear uso | MLflow tracking, inference tables |
| **Guardrails** | Prevenir outputs nocivos | Llama Guard, custom validators |

### Implementação PII Detection
```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = "Contact john.doe@email.com or call 555-1234"
results = analyzer.analyze(text=text, language="en")

anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
print(anonymized.text)  # "Contact [EMAIL] or call [PHONE]"
```

---

## Dia 20: Monitoring & Inference Tables

### Objetivos
- [ ] Configurar inference logging
- [ ] Criar métricas de monitoramento
- [ ] Implementar alertas

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section6/01-AI-System-Monitoring.md`
   - `DEMO-01-Online-Monitoring.md`

2. **Lab NASA GCN** (90min): Executar `lab-08-monitoring/01-inference-tables.py`

### Monitoring Components
```sql
-- Query inference table
SELECT
    timestamp,
    request,
    response,
    latency_ms,
    token_count
FROM gcn_rag_model_inference_log
WHERE timestamp > current_date() - INTERVAL 7 DAYS
ORDER BY timestamp DESC
```

### Key Metrics to Monitor

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Latency P95** | 95th percentile response time | > 5s |
| **Error Rate** | % of failed requests | > 5% |
| **Token Usage** | Tokens per request | > budget |
| **Drift** | Input distribution change | Statistical test |

### Insumo YouTube
**Tema:** "Governança e Monitoramento de GenAI no Databricks"
- PII detection patterns
- Inference tables
- Alerting strategies

---

## Dia 21: Revisão Semanal + Lab Monitoring

### Objetivos
- [ ] Consolidar Sections 4-5
- [ ] Completar Lab 8
- [ ] Resolver practice questions

### Revisão (1h)
1. Revisar flashcards da semana
2. Criar checklist de deployment

### Lab Completo (1.5h)
Executar:
- `lab-08-monitoring/02-metrics-dashboard.py`
- `lab-08-monitoring/03-alerting.py`

### Practice Questions - Sections 4-5

**Q1.** Which step ensures a model can be reproduced with the same environment?
- A. Rate limiting
- B. Registering model with dependencies in Unity Catalog ✓
- C. Autoscaling policies
- D. Storing responses in Delta

**Q2.** What is the primary benefit of using aliases in Model Registry?
- A. Faster inference
- B. Point endpoints to logical names instead of versions ✓
- C. Reduce storage costs
- D. Enable batch processing

**Q3.** Which governance control prevents a single team from exhausting serving capacity?
- A. RBAC
- B. Rate limiting
- C. Quota management ✓
- D. Autoscaling

---

# SEMANA 4: Evaluation, Review & Exam Prep (Dias 22-30)

## Dia 22: Evaluation Metrics Deep Dive

### Objetivos
- [ ] Dominar métricas de RAG (faithfulness, relevance, groundedness)
- [ ] Implementar evaluation pipeline
- [ ] Usar mlflow.evaluate()

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section6/01-Evaluating-RAG-Applications.md`
   - `Section6/02-Importance-of-Evaluation.md`
   - `Section6/03-Evaluation-Techniques.md`

2. **Lab NASA GCN** (90min): Executar `lab-09-vector-optimization/03-benchmarking.py`

### RAG Evaluation Metrics

| Metric | Measures | Formula/Method |
|--------|----------|----------------|
| **Faithfulness** | Respostas baseadas no contexto | LLM judge |
| **Answer Relevance** | Resposta endereça a pergunta | Semantic similarity |
| **Context Relevance** | Contexto recuperado é útil | Precision@K |
| **Groundedness** | Afirmações são suportadas | Citation verification |

### MLflow Evaluate
```python
import mlflow

# Define evaluation dataset
eval_data = pd.DataFrame({
    "question": ["What is GRB 260101A?", ...],
    "ground_truth": ["A gamma-ray burst detected...", ...],
    "context": [retrieved_contexts]
})

# Run evaluation
results = mlflow.evaluate(
    model=rag_chain,
    data=eval_data,
    targets="ground_truth",
    model_type="question-answering",
    evaluators=["default"]
)

print(results.metrics)
```

---

## Dia 23: LLM-as-Judge

### Objetivos
- [ ] Implementar LLM-as-Judge evaluation
- [ ] Criar custom scorers
- [ ] Entender evaluation datasets

### Estudo (2.5h)
1. **Ler** (60min):
   - `Section6/04-End-to-End-Evaluation.md`
   - `DEMO-03-LLM-as-Judge.md`

2. **Praticar** (90min):
   ```python
   from mlflow.genai.scorers import Guidelines, Correctness

   # Define guidelines scorer
   guidelines_scorer = Guidelines(
       guidelines="Response must cite sources. "
                  "Response must be factual. "
                  "Response must be in English."
   )

   # Custom scorer
   @mlflow.genai.scorer
   def astronomy_accuracy(response, context):
       """Check if response is astronomically accurate."""
       prompt = f"""
       Context: {context}
       Response: {response}

       Is this response astronomically accurate?
       Answer: True or False
       """
       return llm_judge(prompt)

   # Evaluate
   results = mlflow.evaluate(
       model=rag_chain,
       data=eval_data,
       evaluators=[guidelines_scorer, astronomy_accuracy]
   )
   ```

### Insumo YouTube
**Tema:** "Avaliação de RAG: Métricas e LLM-as-Judge"
- Métricas essenciais explicadas
- Implementando LLM-as-Judge
- Demo: Evaluation pipeline completo

---

## Dia 24: Production Readiness

### Objetivos
- [ ] Executar production readiness checklist
- [ ] Simular carga de produção
- [ ] Validar SLOs

### Estudo (2.5h)
1. **Ler** (30min): Lab 10 README completamente

2. **Lab NASA GCN** (2h): Executar `lab-10-readiness/01-checklist.py` e `02-simulation.py`

### Production Readiness Checklist

| Category | Check | Critical? |
|----------|-------|-----------|
| **Data Quality** | Source data available | Yes |
| **Data Quality** | Chunks table populated | Yes |
| **Model** | Registered in Unity Catalog | Yes |
| **Model** | Champion alias set | Yes |
| **Model** | Evaluation passed | Yes |
| **Deployment** | VS endpoint ready | Yes |
| **Deployment** | VS index synced | Yes |
| **Deployment** | Model Serving ready | Yes |
| **Monitoring** | Inference logging enabled | Yes |
| **Security** | PII scanning completed | Yes |
| **Security** | Guardrails implemented | Yes |

---

## Dia 25: Review Intensivo - Sections 1-2

### Objetivos
- [ ] Revisar todos os conceitos de Design e Data Prep
- [ ] Resolver practice questions
- [ ] Identificar gaps finais

### Revisão (2.5h)
1. **Ler Resumos** (45min): Revisar notes dos Dias 2-6
2. **Flashcards** (30min): Todas as flashcards de Section 1-2
3. **Practice Questions** (75min): O'Reilly Chapter 2-3 questions

### Quick Reference - Section 1
- Zero-shot: Prompt direto sem exemplos
- Few-shot: Prompt com exemplos
- Chain-of-thought: Raciocínio step-by-step
- Task types: Generation, Classification, Extraction, Transformation
- Compound AI: Sistemas com múltiplos componentes

### Quick Reference - Section 2
- Chunking: Fixed, Sentence, Paragraph, Sliding, Semantic
- Overlap: Preserva contexto entre chunks
- Filtering: Remove ruído, duplicatas, boilerplate
- Delta Lake: Storage otimizado para RAG data

---

## Dia 26: Review Intensivo - Section 3

### Objetivos
- [ ] Revisar Application Development (30% do exame!)
- [ ] Dominar Vector Search e Agents
- [ ] Praticar intensivamente

### Revisão (3h)
1. **Ler Resumos** (60min): Revisar notes dos Dias 8-13
2. **Flashcards** (30min): Todas as flashcards de Section 3
3. **Practice Questions** (90min): O'Reilly Chapter 4 questions

### Quick Reference - Section 3
```
Vector Search:
- Delta Sync Index: Auto-sync com Delta table
- Direct Access Index: Manual upserts
- Embedding: databricks-bge-large-en
- Similarity: cosine, euclidean, dot product

Agents:
- ReAct: Reason + Act pattern
- Tools: Custom functions agents podem chamar
- Memory: Buffer, Window, KG (Knowledge Graph)

RAG Chain:
- Retriever → Prompt Template → LLM → Response
- RetrievalQA.from_chain_type()
- Return source documents for citations
```

---

## Dia 27: Review Intensivo - Sections 4-6

### Objetivos
- [ ] Revisar Deployment, Governance, Evaluation
- [ ] Dominar MLflow workflow
- [ ] Completar todas as practice questions

### Revisão (3h)
1. **Ler Resumos** (60min): Revisar notes dos Dias 15-23
2. **Flashcards** (30min): Todas as flashcards de Sections 4-6
3. **Practice Questions** (90min): O'Reilly Chapter 5 questions + all remaining

### Quick Reference - Sections 4-6
```
MLflow (Section 4):
- mlflow.start_run() → log_param, log_metric
- mlflow.pyfunc.log_model() → save model
- Model Registry: None → Staging → Production
- Aliases: champion, challenger

Governance (Section 5):
- PII: Presidio, regex patterns
- Guardrails: Llama Guard, validators
- Access: Unity Catalog permissions

Evaluation (Section 6):
- Metrics: faithfulness, relevance, groundedness
- LLM-as-Judge: Custom scorers
- mlflow.evaluate(): End-to-end evaluation
```

### Insumo YouTube (Final)
**Tema:** "Preparação Final: Databricks GenAI Certification"
- Resumo de todas as seções
- Dicas de exame
- Últimos conselhos

---

## Dia 28: Simulado Completo #1

### Objetivos
- [ ] Simular condições reais do exame
- [ ] 45 questões em 90 minutos
- [ ] Identificar pontos fracos finais

### Simulado (2h)
1. **Setup** (5min): Timer de 90 minutos, sem consulta
2. **Resolver** (90min): Todas as practice questions dos chapters
3. **Review** (25min): Verificar respostas e anotar erros

### Após o Simulado
Para cada erro:
1. Identificar tópico
2. Reler material relevante
3. Criar flashcard adicional

---

## Dia 29: Simulado Completo #2 + Gap Analysis

### Objetivos
- [ ] Segundo simulado para validar melhorias
- [ ] Focus nos pontos fracos do Day 28
- [ ] Preparação mental final

### Simulado (2h)
1. **Resolver** (90min): Questões restantes + revisitar erros
2. **Gap Analysis** (30min):
   - Quais tópicos ainda causam dúvida?
   - Criar lista final de revisão

### Checklist de Conhecimento Final
| Tópico | Confiança (1-5) | Ação |
|--------|-----------------|------|
| Prompt Engineering | _ | |
| Chunking Strategies | _ | |
| Vector Search | _ | |
| Agents & Tools | _ | |
| RAG Implementation | _ | |
| MLflow & Registry | _ | |
| Model Serving | _ | |
| Governance | _ | |
| Evaluation Metrics | _ | |

---

## Dia 30: Revisão Final + Dia do Exame

### Manhã: Revisão Leve (2h)
1. **Quick Review** (60min): Ler resumos rápidos
2. **Flashcards** (30min): Apenas os mais difíceis
3. **Relaxar** (30min): Não estudar nada novo

### Dicas para o Exame
1. **Time Management**: 2 min/questão máximo, flag e volte
2. **Read Carefully**: Atenção a "NOT", "EXCEPT", "BEST"
3. **Eliminate Wrong**: Remova opções claramente erradas
4. **Trust Your Prep**: Você estudou 30 dias!

### Durante o Exame
- Leia a pergunta inteira antes das opções
- Para scenario questions, identifique o objetivo principal
- Não mude respostas sem razão clara
- Use todo o tempo disponível

---

## Anexo: Insumos YouTube - Resumo

| Dia | Tema do Vídeo | Duração Sugerida |
|-----|---------------|------------------|
| 1 | Guia Completo: Certificação Databricks GenAI Engineer | 15-20min |
| 3 | Compound AI Systems na Prática | 12-15min |
| 5 | Chunking para RAG: O Guia Definitivo | 15-18min |
| 9 | Vector Search do Zero ao Deploy no Databricks | 18-20min |
| 12 | Building RAG Applications com LangChain e Databricks | 15-18min |
| 14 | Agents e Multi-Agent Systems no Databricks | 15-18min |
| 17 | Deploy de RAG no Databricks: Do Notebook ao Endpoint | 18-20min |
| 20 | Governança e Monitoramento de GenAI no Databricks | 15-18min |
| 23 | Avaliação de RAG: Métricas e LLM-as-Judge | 12-15min |
| 27 | Preparação Final: Databricks GenAI Certification | 10-12min |

**Total: 10-12 vídeos | ~2.5h de conteúdo**

---

## Anexo: Recursos Adicionais

### Documentação Oficial
- [Databricks GenAI Documentation](https://docs.databricks.com/en/generative-ai/index.html)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [LangChain Documentation](https://python.langchain.com/docs/)

### Labs NASA GCN
```
labs/
├── lab-03-chunking-indexing/    # Data preparation
├── lab-04-rag-app/              # RAG implementation
├── lab-05-deployment/           # Model serving
├── lab-06-model-management/     # MLflow & versioning
├── lab-07-guardrails/           # Security & governance
├── lab-08-monitoring/           # Inference tracking
├── lab-09-vector-optimization/  # Performance tuning
└── lab-10-readiness/            # Production checklist
```

### Knowledge Base
```
docs/oficial_databricks_material/knowledge_base/
├── 00-OReilly-Book/             # 5 chapters
├── Section1-Design-Applications/
├── Section2-Data-Preparation/
├── Section3-Application-Development/
├── Section4-Assembling-Deploying/
├── Section5-Governance/
└── Section6-Evaluation-Monitoring/
```

---

*Última atualização: Fevereiro 2026*
*Criado para preparação da certificação Databricks Certified Generative AI Engineer Associate*
