# Model Deployment Fundamentals

## Part 1: Model Management

### Slide 1: Model Management

**Title:** Model Management
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture Model Management, we cover the Gen AI system lifecycle, GenAI deployment strategies, MLflow components and model flavors, integrating MLflow with the development lifecycle, Unity Catalog features, using MLflow's Unity Catalog Model Registry, and how MLflow facilitates GenAI deployment.

---

### Slide 2: The Gen AI System Lifecycle - Your AI System is ready, then what?

**Title:** The Gen AI System Lifecycle
**Subtitle:** Your AI System is ready, then what?

*(Visual: Lifecycle diagram showing: Business Problem → Define Success Criteria → Data Collection → Data Preprocessing → AI System (RAG/Chain) Building → AI System Evaluation → AI System Deployment → AI System Monitoring)*

**Two Phases:**
- **System Development** (use static data)
- **Deployment & Production** (deal with continuously changing new data)

**Speaker Notes:**
Managing a machine learning or generative AI project involves several key steps. First, start with a well-defined business problem and set clear success criteria using existing processes or baseline models as a comparison. Next, gather or prepare quality data for training or evaluation, which might involve technical writers or pre-processing the data to make it usable for machine learning or LLM systems.

After preparing the data, build the system—this could involve fine-tuning, pre-training, or assembling components like RAG chains. Begin with offline evaluation to test system performance, refining data preparation if results aren't satisfactory. Once the model passes offline checks, deploy it and monitor its behavior in production, always maintaining a feedback loop so new data can continually improve the model over time.

---

### Slide 3: GenAI Deployment - Packaging models/pipelines

**Title:** GenAI Deployment
**Subtitle:** Packaging models/pipelines

With LLMs, **ML logic is packaged in new forms** which could include:
*   An engineered prompt (possibly stored as a template)
*   A "chain" from LangChain, LlamaIndex etc.
*   A lightweight call to an LLM API service such as:
    *   (Internally/Self) hosted foundation models (e.g. DBRX)
    *   External proprietary models providers (e.g. OpenAI)
*   A lightweight call to a bespoke (self) hosted LLM API:
    *   Fine-tuned model
    *   Pretrained model
*   Locally invoking an LLM or an LLM+tokenizer pipeline (e.g. Hugging Face pipeline) running on GPU(s)

**Note:** All of these still constitute models and pipelines!

**Speaker Notes:**
When packaging generative AI or language models, the logic can take several forms. It might be an engineering prompt—precise instructions given to the model to guide output. The system could also use a chain-based approach, like LangChain or LlamaIndex, or something custom-coded in Python to combine different components.

Often, models are accessed using API calls, which could point to internal or self-hosted foundation models, open source models, or external providers like OpenAI. These APIs can also serve bespoke, fine-tuned, or custom-trained models. Alternatively, models can run locally on GPUs or CPUs, especially for batch processing, where the model and pipeline are fully loaded onto the hardware. All of these approaches—prompts, chains, APIs, and local pipelines—define how a generative AI model or chain is packaged and deployed.

---

### Slide 4: MLflow Components - Model management with MLflow

**Title:** MLflow Components
**Subtitle:** Model management with MLflow

*   Manage end-to-end ML and GenAI workflows, from development to production.
*   Unified platform for both traditional ML and GenAI applications.
*   Generative AI specific model flavors and evaluation metrics.

*(Visual: MLflow component diagram showing: Experiment tracking, Model Registry, Evaluation, Serving, Generative AI, Visualization - with note "We recommend using Model Registry in Unity Catalog")*

**Speaker Notes:**
To package generative AI models efficiently, MLflow plays an important role. MLflow is an open-source tool, not limited to Databricks, that helps manage the entire machine learning and generative AI workflow—from development through to production. When paired with Unity Catalog, it offers a comprehensive experience for tracking all data and AI assets in one place. MLflow also supports generative AI-specific model types and evaluation metrics, making it easier to monitor and assess these advanced models throughout their lifecycle. To package generative AI systems cleanly, MLflow is a key solution. MLflow is an open-source tool that is not exclusive to Databricks—it manages the entire machine learning and generative AI workflow from development to production. Combined with Unity Catalog, it lets you organize and track all your data and AI assets in one place. MLflow now supports generative AI models and includes evaluation metrics tailored for them, which will be discussed in more detail later in the lesson.

---

### Slide 5: MLflow - Model ("Flavor") - A standard format for packaging machine learning models

**Title:** MLflow - Model ("Flavor")
**Subtitle:** A standard format for packaging machine learning models

*   Each **MLflow Model** is a directory containing arbitrary files, together with an MLModel file.
*   `MLModel` file can define **multiple flavors** that the model can be viewed in.
*   With MLflow Models deployment tools can understand the model.
*   Model file can contain **additional metadata** such as `signature`, `input example` etc.

*(Visual: Example of MLflow LangChain Flavor directory structure and MLModel file content)*

**Speaker Notes:**
Since language model applications can be complex, MLflow now offers new model flavors designed for generative AI. A "flavor" in MLflow adds extra details—like metadata, datasets, metrics, and other artifacts—on top of the original model to help track its lifecycle. For example, when using LangChain, MLflow can log the entire chain as a model flavor, recording all steps, dependencies, environment settings, and runtime versions. This makes it easy to package, reproduce, and manage even complex logic as a unified MLflow model. Because generative AI logic can be complex, MLflow has introduced new model flavors to handle these cases. A flavor in MLflow adds useful metadata, datasets, metrics, input examples, and other artifacts on top of your base model for easier lifecycle tracking. For example, if you log a chain built with LangChain, MLflow tracks all steps, dependencies, environment info, and even Databricks runtimes—packaging everything needed to reproduce and manage the complex logic as a single MLflow model.

---

### Slide 6: MLflow - Model ("Flavor") - Built-in model flavors

**Title:** MLflow - Model ("Flavor")
**Subtitle:** Built-in model flavors

**Python Function (`mlflow.pyfunc`):**
*   Serves as a **default model interface** for MLflow Python models.
*   Any MLflow Python model is expected to be loadable as a python function.
*   Allows you to deploy models as Python functions.
*   It includes all the information necessary to **load and use a model**.
*   Some functions: `log_model`, `save_model`, `load_model`, `predict`

*(Visual: List of MLflow Model Flavors including: LangChain, OpenAI, HuggingFace Transformers, PyTorch, TensorFlow, ONNX, Python function)*

**Speaker Notes:**
If your application logic isn't built using a pre-supported flavor—like LangChain, OpenAI, or Hugging Face transformers—you can use MLflow's pyfunc flavor. This provides a default model interface with a predict method, letting you wrap any custom Python code or API calls inside it. The pyfunc flavor is versatile for custom chains and production systems, allowing you to track and manage models even if they don't use standard frameworks.

---

### Slide 7: MLflow and Development Lifecycle - MLflow integration to seamlessly deploy models

**Title:** MLflow and Development Lifecycle
**Subtitle:** MLflow integration to seamlessly deploy models

*(Visual: Workflow diagram showing: Model/Chain Building (Flavor 1, Flavor 2) → MLflow Tracking and Evaluation (Parameters, Metrics, Artifacts, Metadata, Models) → MLflow Registry with Unity Catalog (versions v1, v2, v3 with @champion/@challenger aliases) → Model Deployment)*

**Speaker Notes:**
Integrating model flavors with MLflow streamlines the entire lifecycle of machine learning or language models. You start by creating different versions of your model or chain using a suitable flavor, then experiment and use MLflow to automatically track metadata, metrics, and parameters. Once a version performs well in offline evaluation, you push it to the MLflow registry, which manages DevOps or LLMOps tasks like versioning and deployment. Models can be tagged or given aliases in the registry, making it easier for deployment pipelines to select the right version for production. The Unity Catalog model registry further enhances this by offering robust organization and tracking of registered models.

---

### Slide 8: Unity Catalog (UC) - Single governance solution for data and AI assets on the Lakehouse

**Title:** Unity Catalog (UC)
**Subtitle:** Single governance solution for **data and AI assets** on the Lakehouse

*   Unified visibility into data and AI
*   Single permission model for data and AI
*   Open data sharing

*(Visual: Databricks Unity Catalog diagram showing: Discovery, Access Controls, Lineage, Monitoring, Auditing, Data Sharing capabilities across Tables, Files, Models, Notebooks, Dashboards)*

**Speaker Notes:**
Unity Catalog provides a single governance solution for both data and AI assets, enabling end-to-end lineage between them. It uses a unified permission model and an open data sharing protocol, making it easy to share models with third parties or outside organizations. Managing models in Unity Catalog means assets are organized, secure, and can be shared flexibly while maintaining traceability and control throughout their lifecycle.

---

### Slide 9: MLflow - Unity Catalog Model Registry - A centralized model store

**Title:** MLflow - Unity Catalog Model Registry
**Subtitle:** A centralized model store

*   **Model** lifecycle management with **versioning** & **@aliases**. (e.g. @champion/challenger)
*   Deploy and organize models
*   Collaboration and ACLs
*   Full model lineage
*   Tagging and annotations

*(Visual: Screenshot of Unity Catalog Model Registry UI showing model versions, aliases, and lineage information)*

**Speaker Notes:**
At a high level, Unity Catalog manages AI models through automatic versioning and tagging based on product names, business keywords, or project aliases. Aliases help track models across development stages and make it easy to select the correct model for production. You can control who can access, manage, create versions, and promote models—internally or externally—while also maintaining visibility into their lineage throughout the workflow.

---

### Slide 10: MLflow and GenAI Deployment - Benefits of MLflow

**Title:** MLflow and GenAI Deployment
**Subtitle:** Benefits of MLflow

| Dependency & Environment Management | Packaging Models and Code | Multiple Deployment Options |
|-------------------------------------|---------------------------|----------------------------|
| Ensures that the deployment environments matches the training environment. | Any code and configuration are packaged. | Built-in local Flask Server with MLServer |
| Ensures that models are run consistently, regardless of where they are deployed. | Ensures model can be deployed seamlessly without any missing components | Deploy to major cloud providers. |
| | | **Deploy with Databricks Model Serving** |

**Speaker Notes:**
MLflow helps manage machine learning models by automatically tracking which package versions and dependencies were used to train your model. This means you don't have to manually set up environments when moving models between testing and production—they'll run with the right software automatically. With model flavors, MLflow lets you bundle your code, configuration files, and artifacts into a single package. This makes it easy to deploy your model for local testing and seamlessly scale up to production, especially with Databricks' one-click deployment options. This way, model transitions between environments are reliable, fast, and simple.

---

## Part 2: Deployment Methods

### Slide 11: Deployment Methods

**Title:** Deployment Methods
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture Deployment Methods, we discuss Gen AI model deployment and examine various deployment paradigms.

---

### Slide 12: Gen AI Model Deployment - Deploying a GenAI/LLM model in a few words

**Title:** Gen AI Model Deployment
**Subtitle:** Deploying a GenAI/LLM model in a few words

The process of integrating a AI model into a **production environment**, making it accessible for end-users or other systems to **generate predictions** or **completions**.

(Deployment Strategies: **batch**, **streaming**, **real-time**, or **embedded/edge**)

**Speaker Notes:**
Machine learning model deployment means integrating an AI model into a production environment so it can be used by end users or critical business applications. This allows the model to provide predictions, or for generative AI, produce text completions—usually in the form of textual outputs that support real-world systems and tasks. Deploying a machine learning model means putting the AI model into a production environment so it's accessible for end users or business systems. This way, applications can use the model's predictions or, for generative AI, its text completions to support business needs and workflows.

---

### Slide 13: Deployment Paradigms - Similar to traditional machine learning extended to GenAI

**Title:** Deployment Paradigms
**Subtitle:** Similar to traditional machine learning extended to GenAI

*(Visual: Gradient bar showing Latency Decreases and Throughput Decreases from Batch to Real-time)*

| Batch | Streaming | Real-time |
|-------|-----------|-----------|
| Generate (and store) completions on a table of (text) inputs/prompts | Generate (and store) completions on micro-batches of (text) inputs/prompts as they're processed | Generate completions asynchronously in real-time on individual input/prompt |

**Note:** Edge (on-device) deployment is challenging with large language models due to space requirements.

**Speaker Notes:**
There are several ways to deploy machine learning models, based on how fast predictions are needed and how much data must be processed:
- Batch deployment computes predictions ahead of time for large amounts of data. It runs at scheduled intervals (like hourly or daily), so latency is low and predictions aren't needed instantly. An example is summarizing long documents.
- Streaming deployment processes data in micro-batches, with latency of seconds to minutes and moderate throughput. This fits tasks like translating product reviews as they come in.
- Real-time deployment demands instant responses and high concurrency, typical for chatbots or RAG (Retrieval Augmented Generation) applications.
- Edge deployment runs small models locally on devices, like cars, for simple tasks (not covered in detail here).
Each approach suits different business and technical needs, balancing speed, scale, and hardware requirements.

---

### Slide 14: Deployment Paradigms - Comparing methods

**Title:** Deployment Paradigms
**Subtitle:** Comparing methods

| Deployment Method | Throughput | Latency | Example Application |
|-------------------|------------|---------|---------------------|
| **Batch** | High | High (hours to days) | Summarizing financial reports and generating insights. |
| **Streaming** | Moderate | Moderate (seconds to minutes) | Personalizing marketing messages. |
| **Real-time** | Low-High | Low (milliseconds) | Chatbots (e.g. customer service, doc assistant) |
| **Edge/Embedded** | Low | Low (Dependent on device processing power) | Modify air conditioning temperature in a car using voice command |

**Speaker Notes:**
To recap, model deployment methods include batch, streaming, real-time, and edge device deployments. For today's focus, you'll mainly work with batch and real-time approaches. To recap, the main deployment methods are batch, streaming, real-time, and edge device deployments. The focus here will mainly be on batch and real-time deployments. To recap, the different model deployment methods are batch, streaming, real-time, and edge device deployments. The main focus here will be on batch and real-time approaches. To recap, model deployment can be done via batch, streaming, real-time, or edge methods.
