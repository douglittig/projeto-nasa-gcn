# 🎯 Study Roadmap - Databricks Generative AI Engineer Associate

**Period:** February 1 - March 1, 2026 (28 days)
**Daily Commitment:** 1h30 per day (42 hours total)
**Exam Date:** March 1, 2026
**Hands-on Project:** NASA GCN Pipeline

---

## 📊 Schedule Overview

| Week | Period | Course | Main Focus | Hours |
|:----:|:-------|:-------|:-----------|:-----:|
| **1** | Feb 1-7 | Course 1 | RAG Architecture & Vector Search | 10.5h |
| **2** | Feb 8-14 | Course 2 | Compound AI Systems & Agents | 10.5h |
| **3** | Feb 15-21 | Course 3 | Deployment & Monitoring | 10.5h |
| **4** | Feb 22-28 | Course 4 | Evaluation & Governance | 10.5h |
| **Final** | Mar 1 | Review | Final Mock Exam | - |

---

## 🗓️ WEEK 1: RAG Solution Development (Course 1)
**Goal:** Master RAG fundamentals, data preparation, and Vector Search

### 📅 Day 1 - Sunday, February 1, 2026 (1h30)
**Module 01: Prompt Engineering & RAG Basics (Part 1)**

**Theory (45 min):**
- 📖 Lecture: Prompt Engineering Primer
  - Zero-shot vs Few-shot prompting
  - Context learning strategies
  - Hallucination mitigation
- 📖 Lecture: Introduction to RAG
  - RAG Architecture: Retrieval + Generation
  - Why RAG? (vs fine-tuning)
  - Components: Chunking, Embedding, Retrieval, Generation

**Practice (45 min):**
- 💻 Demo: `1.1 - In Context Learning with AI Playground.py`
  - Use Databricks AI Playground
  - Test different prompts
  - Observe context impact

**🔗 NASA GCN Connection:**
- Think about using RAG to query astronomical alerts
- Example: "What supernova events occurred in the last week?"

**📝 Deliverable:** Notes on differences between tested prompting techniques

---

### 📅 Day 2 - Monday, February 2, 2026 (1h30)
**Module 01: Prompt Engineering & RAG Basics (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `1.LAB - In Context Learning with AI Playground.py`
  - Implement prompts for real use cases
  - Test with different models (GPT-3.5, GPT-4)
  - Document best-performing strategies

**🔗 NASA GCN Connection:**
- Create prompts to extract information from GCN Circulars
- Test: "Summarize the 5 most critical events this week"

**📝 Deliverable:** Notebook with 5 optimized prompt examples

---

### 📅 Day 3 - Tuesday, February 3, 2026 (1h30)
**Module 02: Data Preparation for RAG (Part 1)**

**Theory (40 min):**
- 📖 Lecture: Preparing Data for RAG Solutions
  - Data chunking strategies
  - Document parsing (PDF, JSON, text)
  - Metadata extraction
  - Data quality checks

**Practice (50 min):**
- 💻 Demo: `2.1 - Preparing Data for RAG.py`
  - Load example dataset
  - Implement chunking strategy
  - Extract metadata

**🔗 NASA GCN Connection:**
- Analyze GCN Circulars structure (JSON + text)
- Plan chunking: by event type? by timestamp?

**📝 Deliverable:** Chunking strategy for GCN data

---

### 📅 Day 4 - Wednesday, February 4, 2026 (1h30)
**Module 02: Data Preparation for RAG (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `2.LAB - Preparing Data for RAG.py`
  - Implement complete preparation pipeline
  - Test different chunk sizes (256, 512, 1024 tokens)
  - Evaluate quality metrics

**🔗 NASA GCN Connection:**
- Implement chunking for project's `gcn_circulars` table
- Add metadata: event_type, timestamp, coordinates

**📝 Deliverable:** GCN data preparation code for RAG

---

### 📅 Day 5 - Thursday, February 5, 2026 (1h30)
**Module 03: Vector Search (Part 1)**

**Theory (50 min):**
- 📖 Lecture: Introduction to Vector Stores
  - What are embeddings?
  - Distance metrics (cosine, euclidean, dot product)
  - Vector databases (Pinecone, Chroma, FAISS)
- 📖 Lecture: Introduction to Mosaic AI Vector Search
  - Mosaic AI Vector Search architecture
  - Self-managed vs Managed indexes
  - Delta Sync Protocol

**Practice (40 min):**
- 💻 Demo: `3.1 - Create Self-managed Vector Search Index.py`
  - Create embeddings with sentence-transformers
  - Index documents
  - Test semantic search

**🔗 NASA GCN Connection:**
- Plan vector index for GCN Circulars
- Decide: self-managed or managed?

**📝 Deliverable:** Self-managed vs managed comparison for GCN use case

---

### 📅 Day 6 - Friday, February 6, 2026 (1h30)
**Module 03: Vector Search (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `3.LAB - Create Managed Vector Search Index.py`
  - Create managed index with Delta Sync
  - Configure embedding endpoint
  - Test semantic queries
  - Analyze performance metrics

**🔗 NASA GCN Connection:**
- Implement Vector Search for `gcn_circulars`
- Test: "Find events similar to supernova SN2024A"

**📝 Deliverable:** Functional Vector Search index for GCN

---

### 📅 Day 7 - Saturday, February 7, 2026 (1h30)
**Module 04: RAG Assembly + Week 1 Review**

**Theory (20 min):**
- 📖 Lecture: Assembling a RAG Application
  - Complete architecture: Retrieval → Reranking → Generation
  - Prompt templates for RAG
  - Handling context overflow
  - Evaluation metrics

**Practice (40 min):**
- 💻 Demo: `4.1 - Assembling and Evaluating a RAG Application.py`
  - Connect Vector Search + LLM
  - Implement RAG chain
  - Evaluate response quality

**Mock Exam (30 min):**
- 🎯 Practice questions on Week 1 topics:
  - Prompt Engineering techniques
  - RAG architecture components
  - Data preparation strategies
  - Vector embeddings and similarity search
  - Mosaic AI Vector Search (self-managed vs managed)

**🔗 NASA GCN Connection:**
- Prototype RAG for GCN alert queries
- Example: "Explain today's detected GRB events"

**📝 Deliverable:** Functional RAG prototype for GCN + Mock exam score

---

## 🗓️ WEEK 2: Application Development (Course 2)
**Goal:** Master Compound AI Systems, Multi-stage Reasoning, and Agents

### 📅 Day 8 - Sunday, February 8, 2026 (1h30)
**Module 01: Compound AI Systems (Part 1)**

**Theory (50 min):**
- 📖 Lecture: Defining Compound AI Systems
  - What are Compound AI Systems?
  - Single-model vs compound systems
  - Components: Router, Retriever, Reasoner, Executor
  - Design patterns: Sequential, Parallel, Conditional
- 📖 Lecture: Designing Compound AI Systems
  - Complex problem decomposition
  - Trade-offs: latency vs quality
  - Error handling in compound systems

**Practice (40 min):**
- 💻 Demo: `1.1 - Deconstruct and Plan a Use Case.py`
  - Analyze complex use case
  - Decompose into sub-tasks
  - Design system architecture

**🔗 NASA GCN Connection:**
- Plan compound system for GCN alert analysis:
  - Component 1: Event type classifier
  - Component 2: Coordinate extractor
  - Component 3: Report generator

**📝 Deliverable:** Compound AI architecture diagram for GCN

---

### 📅 Day 9 - Monday, February 9, 2026 (1h30)
**Module 01: Compound AI Systems (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `1.LAB - Planning an AI System for Product Quality Complaints.py`
  - Implement complete compound system
  - Orchestrate multiple models
  - Test conditional flows

**🔗 NASA GCN Connection:**
- Implement pipeline:
  1. Classify alert (GRB, Supernova, etc.)
  2. Extract features (magnitude, coordinates)
  3. Generate summary for astronomers

**📝 Deliverable:** GCN compound system code

---

### 📅 Day 10 - Tuesday, February 10, 2026 (1h30)
**Module 02: Multi-stage Reasoning (Part 1)**

**Theory (40 min):**
- 📖 Lecture: Introduction to Multi-stage Reasoning Chains
  - Chain-of-Thought (CoT) prompting
  - ReAct: Reasoning + Acting
  - Self-Consistency
  - Tree of Thoughts

**Practice (50 min):**
- 💻 Demo: `2.1 - Building Multi-stage Reasoning Chain in Databricks.py`
  - Implement CoT for complex problem
  - Use LangChain for orchestration
  - Visualize reasoning steps

**🔗 NASA GCN Connection:**
- Apply CoT for correlated multi-alert analysis
- Example: "GRB detected at t0, then optical alert at t0+30s. What happened?"

**📝 Deliverable:** Reasoning chain for multi-messenger event analysis

---

### 📅 Day 11 - Wednesday, February 11, 2026 (1h30)
**Module 02: Multi-stage Reasoning (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `2.LAB - Building Multi-stage AI System.py`
  - Implement system with 3+ stages
  - Add error handling
  - Optimize latency

**🔗 NASA GCN Connection:**
- 3-stage analysis system:
  1. Retrieval of similar alerts
  2. Reasoning about patterns
  3. Scientific hypothesis generation

**📝 Deliverable:** Multi-stage system for GCN scientific analysis

---

### 📅 Day 12 - Thursday, February 12, 2026 (1h30)
**Module 03: Agents & Cognitive Architectures (Part 1)**

**Theory (45 min):**
- 📖 Lecture: Introduction to Agents
  - What are AI Agents?
  - Components: Perception, Planning, Action, Memory
  - Tool use and function calling
  - Agent loops: observe → think → act

**Practice (45 min):**
- 💻 Demo: `3.1 - Agent Design in Databricks.py`
  - Create simple agent with LangChain
  - Give agent tools (calculator, search)
  - Test autonomy

**🔗 NASA GCN Connection:**
- Plan agent for alert monitoring:
  - Tools: query_database, calculate_distance, generate_plot

**📝 Deliverable:** Agent design for GCN monitoring

---

### 📅 Day 13 - Friday, February 13, 2026 (1h30)
**Module 03: Agents & Cognitive Architectures (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `3.LAB - Create a ReAct Agent.py`
  - Implement complete ReAct agent
  - Add custom tools
  - Test on complex tasks
  - Analyze reasoning traces

**🔗 NASA GCN Connection:**
- Implement agent that:
  1. Receives question about alerts
  2. Decides which tools to use (query, plot, calculate)
  3. Executes actions
  4. Returns evidence-based response

**📝 Deliverable:** Functional ReAct agent for GCN

---

### 📅 Day 14 - Saturday, February 14, 2026 (1h30)
**Week 1-2 Review + Mock Exam**

**Review (30 min):**
- 📝 Review key concepts:
  - RAG architecture
  - Vector Search
  - Compound AI Systems
  - Multi-stage Reasoning
  - Agents (ReAct)

**Mock Exam (30 min):**
- 🎯 Practice questions on Weeks 1-2:
  - RAG end-to-end architecture
  - Compound AI Systems design patterns
  - Chain-of-Thought prompting
  - ReAct agent components
  - Tool use and function calling
  - Multi-stage reasoning vs single-stage

**Integrated mini-project (30 min):**
- 🧪 Create RAG agent for GCN that:
  - Queries vector search
  - Uses multi-stage reasoning
  - Generates visualizations

**📝 Deliverable:** Complete RAG agent for NASA GCN + Mock exam score

---

## 🗓️ WEEK 3: Deployment & Monitoring (Course 3)
**Goal:** Master model deployment and production monitoring

### 📅 Day 15 - Sunday, February 15, 2026 (1h30)
**Setup + Module 01: Batch Deployment (Part 1)**

**Theory (50 min):**
- 📖 Lecture: MLOps Primer
  - Model lifecycle in production
  - CI/CD for ML
  - Model Registry
- 📖 Lecture: Deployment Methods
  - Batch vs Real-time
  - Edge deployment
  - Hybrid approaches
- 📖 Lecture: Introduction to Batch Deployment
  - When to use batch?
  - Batch inference architecture
  - Databricks Jobs for batch

**Practice (40 min):**
- 💻 Notebook: `00-Build-Model.py`
  - Train example model
  - Register in Model Registry

**🔗 NASA GCN Connection:**
- Plan batch inference for historical alert classification

**📝 Deliverable:** Model registered in Model Registry

---

### 📅 Day 16 - Monday, February 16, 2026 (1h30)
**Module 01: Batch Deployment (Part 2)**

**Practice (1h30):**
- 💻 Demo: `1.0 - Batch Inference using SLM.py`
  - Implement batch inference
  - Use Spark UDFs for parallelization
  - Save results to Delta Table
- 🧪 Lab: `1.LAB - Batch Inference using SLM.py`
  - Process large dataset
  - Optimize performance
  - Monitor job execution

**🔗 NASA GCN Connection:**
- Implement batch inference for:
  - Classify 100k+ historical alerts
  - Extract embeddings from Circulars
  - Process in parallel with Spark

**📝 Deliverable:** Batch inference job for GCN

---

### 📅 Day 17 - Tuesday, February 17, 2026 (1h30)
**Module 02: Real-time Deployment (Part 1)**

**Theory (40 min):**
- 📖 Lecture: Introduction to Real-time Deployment
  - Use cases: APIs, streaming
  - SLAs and latency
  - Scaling strategies
- 📖 Lecture: Databricks Model Serving
  - Serverless architecture
  - Endpoints and routing
  - Auto-scaling

**Practice (50 min):**
- 💻 Demo: `2.1 - Serving External Models with Model Serving.py`
  - Create endpoint for external model (OpenAI, HuggingFace)
  - Configure rate limiting
  - Test calls

**🔗 NASA GCN Connection:**
- Plan real-time endpoint for:
  - Receive alert → classify → return priority

**📝 Deliverable:** Real-time classification endpoint

---

### 📅 Day 18 - Wednesday, February 18, 2026 (1h30)
**Module 02: Real-time Deployment (Part 2)**

**Practice (1h30):**
- 💻 Demo: `2.2 - Deploying an LLM Chain to Databricks Model Serving.py`
  - Deploy complete RAG chain
  - Configure caching
  - Test latency
- 🧪 Lab: `2.LAB - Custom Model Deployment and A/B Testing.py`
  - Deploy custom model
  - Configure A/B test (model v1 vs v2)
  - Analyze traffic split

**🔗 NASA GCN Connection:**
- Deploy RAG agent created in Week 2
- A/B test: embedding model A vs B

**📝 Deliverable:** RAG endpoint with A/B testing

---

### 📅 Day 19 - Thursday, February 19, 2026 (1h30)
**Module 03: Monitoring (Part 1)**

**Theory (45 min):**
- 📖 Lecture: AI Application Monitoring
  - ML metrics: drift, accuracy, latency
  - Observability: logs, traces, metrics
  - Lakehouse Monitoring
  - Alerting strategies

**Practice (45 min):**
- 💻 Demo: `3.1 - Online Monitoring an LLM RAG Chain.py`
  - Configure Lakehouse Monitoring
  - Create dashboards
  - Define SLAs

**🔗 NASA GCN Connection:**
- Plan monitoring for:
  - Endpoint latency
  - Class distribution (drift)
  - Cost per request

**📝 Deliverable:** Monitoring dashboard for GCN endpoint

---

### 📅 Day 20 - Friday, February 20, 2026 (1h30)
**Module 03: Monitoring (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `3.LAB - Online Monitoring.py`
  - Implement complete monitoring
  - Configure alerts
  - Simulate drift and test detection

**🔗 NASA GCN Connection:**
- Implement monitoring for:
  - Detect drift in alert types
  - Alert if latency > 2s
  - Cost tracking

**📝 Deliverable:** Monitoring system with alerts

---

### 📅 Day 21 - Saturday, February 21, 2026 (1h30)
**Deployment & Monitoring Review + Mock Exam**

**Review (20 min):**
- 📝 Review concepts:
  - Batch vs Real-time deployment
  - Model Serving architecture
  - A/B Testing strategies
  - Lakehouse Monitoring metrics

**Mock Exam (30 min):**
- 🎯 Practice questions on Week 3:
  - MLOps lifecycle and Model Registry
  - Batch inference with Spark UDFs
  - Model Serving endpoints and auto-scaling
  - A/B testing configuration
  - Monitoring metrics (drift, latency, cost)
  - SLA definition and alerting

**Integration (40 min):**
- 🧪 Complete GCN solution deployment:
  - Batch job: process historical data
  - Real-time endpoint: new alerts
  - Monitoring: dashboards + alerts

**📝 Deliverable:** Complete deployed pipeline + Mock exam score

---

## 🗓️ WEEK 4: Evaluation & Governance (Course 4)
**Goal:** Master model evaluation and AI governance

### 📅 Day 22 - Sunday, February 22, 2026 (1h30)
**Setup + Module 01: Data Legality & Guardrails (Part 1)**

**Theory (45 min):**
- 📖 Lecture: Why Evaluating GenAI Applications
  - LLM evaluation challenges
  - Qualitative vs quantitative metrics
  - Human evaluation vs automated

**Practice (45 min):**
- 💻 Notebook: `00-Build-Model.py`
  - Model setup for evaluation
- 💻 Demo: `1.1 - Explore Licensing of Datasets.py`
  - Verify dataset licenses
  - Compliance checks
  - Copyright considerations

**🔗 NASA GCN Connection:**
- Verify NASA GCN data license (public domain)
- Document data provenance

**📝 Deliverable:** Compliance document for GCN

---

### 📅 Day 23 - Monday, February 23, 2026 (1h30)
**Module 01: Data Legality & Guardrails (Part 2)**

**Practice (1h30):**
- 💻 Demo: `1.2 - Prompts and Guardrails Basics.py`
  - Implement input validation
  - Content filtering
  - PII detection
- 🧪 Lab: `1.LAB - Implement and Test Guardrails for LLMs.py`
  - Create custom guardrails
  - Test with adversarial inputs
  - Evaluate false positives

**🔗 NASA GCN Connection:**
- Implement guardrails for:
  - Avoid responses about non-astronomical data
  - Validate astronomical coordinates
  - Filter malicious queries

**📝 Deliverable:** Guardrails system for GCN agent

---

### 📅 Day 24 - Tuesday, February 24, 2026 (1h30)
**Module 02: Security & Governance (Part 1)**

**Theory (40 min):**
- 📖 Lecture: AI System Security
  - Prompt injection attacks
  - Data poisoning
  - Model extraction
  - Privacy concerns (PII leakage)
  - OWASP Top 10 for LLMs

**Practice (50 min):**
- 💻 Demo: `2.1 - Implementing AI Guardrails.py`
  - Implement security guardrails
  - Test against prompt injection
  - Rate limiting

**🔗 NASA GCN Connection:**
- Analyze attack vectors on GCN agent
- Implement protections

**📝 Deliverable:** Security assessment of GCN agent

---

### 📅 Day 25 - Wednesday, February 25, 2026 (1h30)
**Module 02: Security & Governance (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `2.LAB - Implementing AI Guardrails.py`
  - Implement complete governance
  - Audit logs
  - Access control
  - Prompt versioning

**🔗 NASA GCN Connection:**
- Implement audit trail for GCN agent:
  - Log all queries
  - User tracking
  - Response versioning

**📝 Deliverable:** Implemented governance system

---

### 📅 Day 26 - Thursday, February 26, 2026 (1h30)
**Module 03: Evaluation Techniques (Part 1)**

**Theory (30 min):**
- 📖 Lecture: Evaluation Techniques
  - Benchmark datasets
  - Human evaluation
  - LLM-as-a-Judge
  - Domain-specific metrics

**Practice (1h):**
- 💻 Demo: `3.1 - Benchmark Evaluation.py`
  - Use standard benchmarks (MMLU, etc.)
  - Compare models
- 💻 Demo: `3.2 - LLM-as-a-Judge.py`
  - Use GPT-4 as evaluator
  - Create rubrics
  - Evaluate responses

**🔗 NASA GCN Connection:**
- Create benchmark for GCN agent:
  - 50 astronomical queries
  - Ground truth answers
  - Evaluation criteria

**📝 Deliverable:** Benchmark dataset for GCN

---

### 📅 Day 27 - Friday, February 27, 2026 (1h30)
**Module 03: Evaluation Techniques (Part 2)**

**Practice (1h30):**
- 🧪 Lab: `3.LAB - Domain-Specific Evaluation.py`
  - Create custom metrics
  - Implement automated evaluator
  - Calculate accuracy, relevance, hallucination rate

**🔗 NASA GCN Connection:**
- Evaluate GCN agent:
  - Accuracy: correct answers about events
  - Relevance: useful information for astronomers
  - Hallucination: data fabrication

**📝 Deliverable:** GCN agent evaluation report

---

### 📅 Day 28 - Saturday, February 28, 2026 (1h30)
**Module 04: End-to-end Evaluation + Final Mock Exam**

**Theory (15 min):**
- 📖 Lecture: End-to-end Application Evaluation
  - Holistic evaluation
  - Cost-performance tradeoffs
  - User satisfaction metrics

**Practice (30 min):**
- 💻 Demo: `4.1 - Evaluation with Mosaic AI Agent Evaluation.py`
  - Use Mosaic AI Agent Evaluation
  - Evaluate complete agent
  - Generate report

**Final Mock Exam (45 min):**
- 🎯 **COMPLETE CERTIFICATION MOCK EXAM**
  - 40-50 questions covering all topics:
    - Week 1: RAG, Vector Search, Data Preparation
    - Week 2: Compound AI, Multi-stage Reasoning, Agents
    - Week 3: Deployment, Model Serving, Monitoring
    - Week 4: Evaluation, Guardrails, Governance
  - Time limit: 45 min (simulate real exam pressure)
  - Evaluate score and identify gaps

**📝 Deliverable:** Final mock exam score (target: >80%)

---

## 🎯 Day 29 - Sunday, March 1, 2026
**EXAM: Databricks Generative AI Engineer Associate**

### Final Preparation (Morning - before exam)
- ☕ Review key concepts (30 min)
- 📝 Review favorite hands-on labs (30 min)
- 🧘 Relax and be confident

### Key Topics to Review:
1. ✅ RAG Architecture (retrieval, generation, evaluation)
2. ✅ Vector Search (embeddings, similarity search)
3. ✅ Compound AI Systems (design patterns)
4. ✅ Multi-stage Reasoning (CoT, ReAct)
5. ✅ Agents (tool use, autonomy)
6. ✅ Model Deployment (batch, real-time)
7. ✅ Model Serving (endpoints, scaling)
8. ✅ Monitoring (drift, latency, costs)
9. ✅ Evaluation (benchmarks, LLM-as-Judge)
10. ✅ Governance (security, guardrails, compliance)

---

## 📚 Additional Resources

### Official Documentation
- [Databricks GenAI Documentation](https://docs.databricks.com/generative-ai/index.html)
- [Mosaic AI Documentation](https://docs.databricks.com/machine-learning/mosaic-ai/index.html)
- [Model Serving Guide](https://docs.databricks.com/machine-learning/model-serving/index.html)
- [Lakehouse Monitoring](https://docs.databricks.com/lakehouse-monitoring/index.html)

### Tools & Frameworks
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

### Important Papers
- [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)
- [ReAct: Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)

---

## 🏆 Progress Checklist

### Week 1: RAG Foundations ✅
- [ ] Day 1: Prompt Engineering basics
- [ ] Day 2: AI Playground lab
- [ ] Day 3: Data preparation theory
- [ ] Day 4: Data preparation lab
- [ ] Day 5: Vector Search theory
- [ ] Day 6: Vector Search lab
- [ ] Day 7: RAG assembly

### Week 2: Application Development ✅
- [ ] Day 8: Compound AI Systems theory
- [ ] Day 9: Compound AI Systems lab
- [ ] Day 10: Multi-stage reasoning theory
- [ ] Day 11: Multi-stage reasoning lab
- [ ] Day 12: Agents theory
- [ ] Day 13: Agents lab (ReAct)
- [ ] Day 14: Integrative review

### Week 3: Deployment & Monitoring ✅
- [ ] Day 15: MLOps + Batch deployment theory
- [ ] Day 16: Batch deployment lab
- [ ] Day 17: Real-time deployment theory
- [ ] Day 18: Real-time deployment lab + A/B test
- [ ] Day 19: Monitoring theory
- [ ] Day 20: Monitoring lab
- [ ] Day 21: Complete deployment review

### Week 4: Evaluation & Governance ✅
- [ ] Day 22: Data legality + licensing
- [ ] Day 23: Guardrails implementation
- [ ] Day 24: Security theory
- [ ] Day 25: Security lab + governance
- [ ] Day 26: Evaluation techniques (benchmark + LLM-as-Judge)
- [ ] Day 27: Domain-specific evaluation
- [ ] Day 28: End-to-end evaluation + final review

### Exam 🎯
- [ ] Day 29 (Mar 1): Databricks GenAI Engineer Associate Exam

---

## 💡 Study Tips

### Daily Organization
1. **Preparation (5 min):** Review day's objective
2. **Theory (30-50 min):** Read lectures, take notes
3. **Practice (40-60 min):** Run notebooks, experiment
4. **Review (5 min):** Note key learnings
5. **GCN Connection (ongoing):** Think about practical applications

### Best Practices
- ✅ Run ALL notebooks (don't just read)
- ✅ Make modifications and experiment
- ✅ Document code in NASA GCN project
- ✅ Take notes in Markdown
- ✅ Take screenshots of dashboards/results
- ✅ Record weekly YouTube videos
- ✅ Review on weekends (Days 7, 14, 21)

### YouTube Content Planning
- **Week 1:** "Building RAG for Astronomical Alerts - Part 1"
- **Week 2:** "AI Agents for Cosmic Event Analysis"
- **Week 3:** "Deploying LLMs to Production with Databricks"
- **Week 4:** "Evaluation and Governance of AI Systems"

---

## 🔗 NASA GCN Project Connection

### Practical Implementations Throughout Roadmap

**After Week 1:**
- ✅ Functional RAG over GCN Circulars
- ✅ Vector Search index for alerts
- ✅ Semantic query of astronomical events

**After Week 2:**
- ✅ Compound AI System for multi-stage classification
- ✅ Autonomous agent for alert analysis
- ✅ Multi-stage reasoning for multi-messenger events

**After Week 3:**
- ✅ Batch processing of historical alerts
- ✅ Real-time endpoint for classification
- ✅ Monitoring dashboard

**After Week 4:**
- ✅ Complete governance system
- ✅ Query guardrails
- ✅ Quantitative system evaluation
- ✅ Compliance documentation

### Final NASA GCN + GenAI Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    NASA GCN Pipeline                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Kafka] → [Bronze] → [Silver] → [Gold] → [GenAI Layer] │
│                                              ↓           │
│                                         ┌────────────┐   │
│                                         │ Vector DB  │   │
│                                         │ (Circulars)│   │
│                                         └────────────┘   │
│                                              ↓           │
│                                         ┌────────────┐   │
│                                         │ RAG Agent  │   │
│                                         │ (ReAct)    │   │
│                                         └────────────┘   │
│                                              ↓           │
│                                         ┌────────────┐   │
│                                         │ Serving    │   │
│                                         │ Endpoint   │   │
│                                         └────────────┘   │
│                                              ↓           │
│                                         ┌────────────┐   │
│                                         │ Monitoring │   │
│                                         │ Dashboard  │   │
│                                         └────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Success Metrics

### Measurable Objectives
- ✅ Complete 100% of labs (31 labs total)
- ✅ Implement 7+ GenAI features in GCN project
- ✅ Record 4 YouTube videos (1 per week)
- ✅ Pass exam with score >70%

### NASA GCN Project KPIs
- **RAG Quality:** Accuracy >80% on astronomical benchmark
- **Latency:** Response <2s for simple queries
- **Uptime:** 99%+ for production endpoint
- **Cost:** <$50/month in inference costs

---

**🎓 Good luck with your studies and certification!**

**Last updated:** February 1, 2026
**Next review:** After exam approval (March 1, 2026)
