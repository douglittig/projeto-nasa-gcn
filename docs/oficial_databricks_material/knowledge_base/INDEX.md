# Databricks Certified Generative AI Engineer Associate

## Knowledge Base - Guia de Estudos

Este repositório contém todo o material de estudo organizado de acordo com os **6 domínios oficiais** da certificação Databricks Generative AI Engineer Associate.

---

## Quick Start - Ebook Consolidado

**Comece aqui:** [study-guide/EBOOK-Databricks-GenAI-Study-Guide.md](study-guide/EBOOK-Databricks-GenAI-Study-Guide.md) - Material de estudo completo unificado (transcrições + livro O'Reilly) em um único documento.

---

## Informações do Exame

| Aspecto | Detalhes |
|---------|----------|
| **Questões** | 45 múltipla escolha/seleção |
| **Tempo** | 90 minutos |
| **Taxa** | $200 USD |
| **Método** | Online Proctored |
| **Validade** | 2 anos |
| **Pré-requisitos** | Nenhum (6+ meses de experiência recomendado) |

---

## Estrutura do Exame

| Seção | Domínio | Peso |
|-------|---------|------|
| 1 | [Design Applications](#section-1-design-applications) | ~14% |
| 2 | [Data Preparation](#section-2-data-preparation) | ~14% |
| 3 | [Application Development](#section-3-application-development) | ~30% |
| 4 | [Assembling and Deploying Applications](#section-4-assembling-and-deploying) | ~22% |
| 5 | [Governance](#section-5-governance) | ~8% |
| 6 | [Evaluation and Monitoring](#section-6-evaluation-and-monitoring) | ~12% |

---

## Section 1: Design Applications

**Objetivos:**
- Design a prompt that elicits a specifically formatted response
- Select model tasks to accomplish a given business requirement
- Select chain components for a desired model input and output
- Translate business use case goals into AI pipeline descriptions
- Define and order tools for multi-stage reasoning

### Material de Estudo

| Arquivo | Conteúdo |
|---------|----------|
| [01-Prompt-Engineering-Fundamentals.md](Section1-Design-Applications/01-Prompt-Engineering-Fundamentals.md) | Zero-shot, few-shot, chain-of-thought prompting |
| [01-Introduction-Compound-AI.md](Section1-Design-Applications/01-Introduction-Compound-AI.md) | Introdução a sistemas Compound AI |
| [02-Defining-Compound-AI-Systems.md](Section1-Design-Applications/02-Defining-Compound-AI-Systems.md) | Intents, tasks, pipelines |
| [03-Designing-Compound-AI-Systems.md](Section1-Design-Applications/03-Designing-Compound-AI-Systems.md) | Processo de design e decomposição |
| [01-Introduction-Reasoning-Chains.md](Section1-Design-Applications/01-Introduction-Reasoning-Chains.md) | Introdução a cadeias de raciocínio |
| [02-Multi-stage-Reasoning-Chains.md](Section1-Design-Applications/02-Multi-stage-Reasoning-Chains.md) | LangChain, LlamaIndex, DSPY |
| [DEMO-01-Deconstruct-Plan-Use-Case.md](Section1-Design-Applications/DEMO-01-Deconstruct-Plan-Use-Case.md) | Demo: planejamento de use case |
| [DEMO-01-Building-Reasoning-Chain.md](Section1-Design-Applications/DEMO-01-Building-Reasoning-Chain.md) | Demo: implementação de chains |

**Livro O'Reilly:** [2.-Designing-Generative-AI-Applications.md](00-OReilly-Book/2.-Designing-Generative-AI-Applications.md)

---

## Section 2: Data Preparation

**Objetivos:**
- Apply chunking strategy for document structure and model constraints
- Filter extraneous content that degrades RAG quality
- Choose appropriate Python package to extract document content
- Define operations to write chunked text into Delta Lake tables
- Identify source documents for RAG application quality
- Identify prompt/response pairs for model tasks
- Use tools and metrics to evaluate retrieval performance
- Design retrieval systems using advanced chunking strategies
- Explain the role of re-ranking in information retrieval

### Material de Estudo

| Arquivo | Conteúdo |
|---------|----------|
| [01-RAG-Architecture-Introduction.md](Section2-Data-Preparation/01-RAG-Architecture-Introduction.md) | Arquitetura RAG, workflow, benefícios |
| [02-Context-Engineering.md](Section2-Data-Preparation/02-Context-Engineering.md) | Context engineering, limitações de prompting |
| [03-Document-Parsing-Chunking.md](Section2-Data-Preparation/03-Document-Parsing-Chunking.md) | ai_parse_document, estratégias de chunking |
| [DEMO-01-Preparing-Data-for-RAG.md](Section2-Data-Preparation/DEMO-01-Preparing-Data-for-RAG.md) | Demo: preparação de dados |
| [DEMO-02-Assembling-and-Evaluating-RAG.md](Section2-Data-Preparation/DEMO-02-Assembling-and-Evaluating-RAG.md) | Demo: montagem de RAG |

**Livro O'Reilly:** [3.-Preparing-and-Chunking-Data-for-RAG-Applications.md](00-OReilly-Book/3.-Preparing-and-Chunking-Data-for-RAG-Applications.md)

---

## Section 3: Application Development

**Objetivos:**
- Create tools for data retrieval needs
- Select LangChain/similar tools for GenAI applications
- Identify how prompt formats change model outputs
- Qualitatively assess responses for quality and safety issues
- Select chunking strategy based on evaluation
- Augment prompts with additional context
- Implement LLM guardrails to prevent negative outcomes
- Write metaprompts that minimize hallucinations
- Build agent prompt templates exposing available functions
- Select best LLM and embedding model based on requirements
- Utilize Agent Framework for developing agentic systems

### Material de Estudo

| Arquivo | Conteúdo |
|---------|----------|
| [01-Mosaic-AI-Vector-Search.md](Section3-Application-Development/01-Mosaic-AI-Vector-Search.md) | Configuração Mosaic AI Vector Search |
| [02-Vector-Store-Algorithms.md](Section3-Application-Development/02-Vector-Store-Algorithms.md) | HNSW, Product Quantization, reranking |
| [03-Embeddings-Similarity.md](Section3-Application-Development/03-Embeddings-Similarity.md) | Modelos de embedding, métricas de similaridade |
| [01-Introduction-Agents.md](Section3-Application-Development/01-Introduction-Agents.md) | Introdução a agentes |
| [02-Agents-Fundamentals.md](Section3-Application-Development/02-Agents-Fundamentals.md) | ReAct pattern, tools, multi-agent |
| [03-Agent-Bricks-Framework.md](Section3-Application-Development/03-Agent-Bricks-Framework.md) | Agent Bricks framework |
| [DEMO-01-Create-Vector-Search.md](Section3-Application-Development/DEMO-01-Create-Vector-Search.md) | Demo: criação de vector search |
| [DEMO-02-Building-Vector-Search.md](Section3-Application-Development/DEMO-02-Building-Vector-Search.md) | Demo: construção de vector search |
| [DEMO-01-Agent-Design-Databricks.md](Section3-Application-Development/DEMO-01-Agent-Design-Databricks.md) | Demo: design de agentes |
| [DEMO-02-Clean-Transform-Chunk.md](Section3-Application-Development/DEMO-02-Clean-Transform-Chunk.md) | Demo: transformação de dados |
| [DEMO-03-Building-and-Logging-Retrieval-Agent.md](Section3-Application-Development/DEMO-03-Building-and-Logging-Retrieval-Agent.md) | Demo: retrieval agent com LangChain |
| [DEMO-04-Building-Knowledge-Assistant-Agent-Bricks.md](Section3-Application-Development/DEMO-04-Building-Knowledge-Assistant-Agent-Bricks.md) | Demo: Agent Bricks |

**Livro O'Reilly:** [4.-Building-GenAI-Applications-with-Python-and-LangChain.md](00-OReilly-Book/4.-Building-GenAI-Applications-with-Python-and-LangChain.md)

---

## Section 4: Assembling and Deploying

**Objetivos:**
- Code a chain using pyfunc model with pre/post-processing
- Control access to resources from model serving endpoints
- Code simple chains using LangChain
- Choose basic elements for RAG: model flavor, embedding, retriever, dependencies
- Register model to Unity Catalog using MLflow
- Sequence steps to deploy endpoint for RAG application
- Create and query Vector Search index
- Serve LLM application leveraging Foundation Model APIs
- Identify batch inference workloads and apply ai_query()

### Material de Estudo

| Arquivo | Conteúdo |
|---------|----------|
| [01-MLflow-for-RAG.md](Section4-Assembling-Deploying/01-MLflow-for-RAG.md) | MLflow para RAG, tracking, registry |
| [02-Model-Deployment-Fundamentals.md](Section4-Assembling-Deploying/02-Model-Deployment-Fundamentals.md) | Fundamentos de deployment, Unity Catalog |
| [03-MLflow-Agent-Development.md](Section4-Assembling-Deploying/03-MLflow-Agent-Development.md) | MLflow Tracing, experimentos, flavors |
| [01-Batch-Deployment.md](Section4-Assembling-Deploying/01-Batch-Deployment.md) | Batch inference, ai_query() |
| [02-Real-Time-Deployment.md](Section4-Assembling-Deploying/02-Real-Time-Deployment.md) | Model Serving, endpoints |
| [DEMO-01-Batch-Deployment.md](Section4-Assembling-Deploying/DEMO-01-Batch-Deployment.md) | Demo: deployment em batch |
| [DEMO-02-Real-Time-Deployment.md](Section4-Assembling-Deploying/DEMO-02-Real-Time-Deployment.md) | Demo: deployment real-time |

**Livro O'Reilly:** [5.-Deploying-and-Integrating-RAG-Systems-on-Databricks.md](00-OReilly-Book/5.-Deploying-and-Integrating-RAG-Systems-on-Databricks.md)

---

## Section 5: Governance

**Objetivos:**
- Use masking techniques as guardrails to meet performance objectives
- Select guardrail techniques to protect against malicious user inputs
- Recommend alternatives for problematic text mitigation in data sources
- Use legal/licensing requirements to avoid legal risk

### Material de Estudo

| Arquivo | Conteúdo |
|---------|----------|
| [01-Securing-and-Governing-GenAI.md](Section5-Governance/01-Securing-and-Governing-GenAI.md) | DASF framework, Llama Guard, Unity Catalog |
| [DEMO-01-Prompt-Safety.md](Section5-Governance/DEMO-01-Prompt-Safety.md) | Demo: segurança de prompts |
| [DEMO-02-Implementing-Guardrails.md](Section5-Governance/DEMO-02-Implementing-Guardrails.md) | Demo: implementação de guardrails |
| [DEMO-03-Parse-Documents.md](Section5-Governance/DEMO-03-Parse-Documents.md) | Demo: parsing seguro de documentos |

---

## Section 6: Evaluation and Monitoring

**Objetivos:**
- Select LLM choice based on quantitative evaluation metrics
- Select key metrics to monitor for specific LLM deployment scenario
- Evaluate model performance in RAG application using MLflow
- Use inference logging to assess deployed RAG application performance
- Use Databricks features to control LLM costs
- Use inference tables and Agent Monitoring to track live LLM endpoint
- Identify evaluation judges that require ground truth
- Compare evaluation and monitoring phases of GenAI application lifecycle

### Material de Estudo

| Arquivo | Conteúdo |
|---------|----------|
| [01-Evaluating-RAG-Applications.md](Section6-Evaluation-Monitoring/01-Evaluating-RAG-Applications.md) | Métricas RAG: faithfulness, relevance |
| [02-Importance-of-Evaluation.md](Section6-Evaluation-Monitoring/02-Importance-of-Evaluation.md) | Importância da avaliação, data legality |
| [03-Evaluation-Techniques.md](Section6-Evaluation-Monitoring/03-Evaluation-Techniques.md) | BLEU, ROUGE, LLM-as-Judge |
| [04-End-to-End-Evaluation.md](Section6-Evaluation-Monitoring/04-End-to-End-Evaluation.md) | Avaliação end-to-end |
| [01-AI-System-Monitoring.md](Section6-Evaluation-Monitoring/01-AI-System-Monitoring.md) | Lakehouse Monitoring, drift detection |
| [02-LLMOps-Concepts.md](Section6-Evaluation-Monitoring/02-LLMOps-Concepts.md) | MLOps/LLMOps, DABs, CI/CD |
| [DEMO-01-Exploring-Evaluation.md](Section6-Evaluation-Monitoring/DEMO-01-Exploring-Evaluation.md) | Demo: exploração de avaliação |
| [DEMO-02-Benchmarking.md](Section6-Evaluation-Monitoring/DEMO-02-Benchmarking.md) | Demo: benchmarking |
| [DEMO-03-LLM-as-Judge.md](Section6-Evaluation-Monitoring/DEMO-03-LLM-as-Judge.md) | Demo: LLM como avaliador |
| [DEMO-01-Online-Monitoring.md](Section6-Evaluation-Monitoring/DEMO-01-Online-Monitoring.md) | Demo: monitoramento online |

---

## Recursos Adicionais

### Exam Guide Oficial
- [databricks-certified-generative-ai-engineer-associate-guide.pdf](00-Exam-Guide/databricks-certified-generative-ai-engineer-associate-guide.pdf)

### Livro O'Reilly - Study Guide Completo
| Capítulo | Conteúdo |
|----------|----------|
| [1.-Exam-Details-and-Resources.md](00-OReilly-Book/1.-Exam-Details-and-Resources.md) | Detalhes do exame, setup do workspace |
| [2.-Designing-Generative-AI-Applications.md](00-OReilly-Book/2.-Designing-Generative-AI-Applications.md) | Design de aplicações GenAI |
| [3.-Preparing-and-Chunking-Data-for-RAG-Applications.md](00-OReilly-Book/3.-Preparing-and-Chunking-Data-for-RAG-Applications.md) | Preparação de dados e chunking |
| [4.-Building-GenAI-Applications-with-Python-and-LangChain.md](00-OReilly-Book/4.-Building-GenAI-Applications-with-Python-and-LangChain.md) | Construção com Python e LangChain |
| [5.-Deploying-and-Integrating-RAG-Systems-on-Databricks.md](00-OReilly-Book/5.-Deploying-and-Integrating-RAG-Systems-on-Databricks.md) | Deploy e integração de RAG |

### Repositório GitHub
- [Databricks-Certified-Generative-AI-Engineer-Associate-Study-Guide-main](Databricks-Certified-Generative-AI-Engineer-Associate-Study-Guide-main/)

---

## Tecnologias-Chave

| Tecnologia | Uso no Exame |
|------------|--------------|
| **MLflow** | Tracking, Model Registry, Tracing, Evaluation |
| **Unity Catalog** | Governance, access control, model registration |
| **Mosaic AI Vector Search** | Semantic search, embeddings storage |
| **Model Serving** | Real-time inference, Foundation Model APIs |
| **LangChain** | Chains, agents, tools |
| **Delta Lake** | Data storage for RAG applications |

---

## Dicas de Estudo

1. **Foco em Application Development (30%)** - Maior peso no exame
2. **Pratique com código** - Use o Databricks workspace para hands-on
3. **Entenda MLflow** - Aparece em múltiplas seções
4. **Domine chunking strategies** - Fundamental para RAG
5. **Conheça guardrails** - Importante para governance e safety

---

*Última atualização: Fevereiro 2026*
