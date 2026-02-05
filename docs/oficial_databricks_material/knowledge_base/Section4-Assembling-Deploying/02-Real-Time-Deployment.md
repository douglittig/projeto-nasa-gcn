# Real-time Deployment

## Part 1: Introduction to Real-time Deployment

### Slide 1: Introduction to Real-time Deployment

**Title:** Introduction to Real-time Deployment
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture Introduction to Real-time Deployment, we discuss real-time deployment, challenges of building real-time AI systems, and Databricks Model Serving.

---

### Slide 2: Real-time Deployment - Overview

**Title:** Real-time Deployment

**Key Points:**
*   The process of serving machine learning models in a production environment where **predictions are generated instantly** in response to incoming data or requests.
*   Crucial for applications that require **low-latency responses**, such as chatbots, message intent detection, autonomous systems, and other time-sensitive tasks.

*With the emergence of new Gen AI applications, this deployment method is becoming increasingly common, especially as large language models need to be served in real-time.*

**Speaker Notes:**
First, let's go over the basics of real-time deployment. This refers to serving a machine learning or language model in a production environment where predictions are generated instantly. The goal is to provide quick access to completions, which is crucial for low-latency use cases like chatbots or message intent detection. For example, if a user posts a message on a social media platform, you might want to immediately check that it doesn't contain violent content. As mentioned earlier, with the rise of new generative AI applications and the complexity of running batch jobs on your own infrastructure, real-time deployment is becoming more and more common—especially since large language models are often expected to deliver results instantly.

---

### Slide 3: Real-time Deployment - Use Case

**Title:** Real-time Deployment
**Subtitle:** A typical real-time deployment use case

*   **Description:** Real-time Intent Detection for social media platform
*   **Scenario:**
    *   A fine-tuned large language model for classifying social media post, is deployed in the real-time environment.
    *   The model provides immediate classification of posts over a REST API.
    *   If post content is classified as toxic/violent/harmful it is taken down/removed.
*   **Requirements:** Low latency, immediate action, 24/7 uptime, continuous monitoring

**Speaker Notes:**
To give an example, a typical real-time deployment scenario would be intent detection on a social media platform. In this case, you might deploy a fine-tuned large language model or use a proprietary model with few-shot classification capabilities. The goal is for the model to immediately classify user posts as they're submitted to the platform. Through a REST API, if a post is flagged as harmful, toxic, or violent, it should be taken down right away. This kind of setup demands low latency, instant action, and round-the-clock uptime with ongoing monitoring.

---

### Slide 4: Real-time Deployment - Workflow for LMs

**Title:** Real-time Deployment
**Subtitle:** A typical real-time model deployment workflow for LMs

*(Visual: Workflow diagram showing the complete real-time deployment pipeline)*

**Components:**
*   Delta Lake / UC Volume - Training Data
*   Build Model (Create model/pipeline/chain)
*   MLflow UC Model Registry
*   Vector Search (e.g. Databricks Vector Search)
*   Serving Endpoint - Databricks Model Serving
*   Monitoring
*   Downstream App (Web app, mobile app)

**Sources:** DIY, Hugging Face Hub, Databricks Marketplace

**Speaker Notes:**
Going back to how this affects development and deployment in Databricks, the approach to developing the model itself doesn't really change. Whether you're using a model from the marketplace, fine-tuning a model from the model hub or Databricks' supported foundation models with the fine-tuning API, or even building your own model from scratch, the development process remains consistent. Once the model is registered, deploying it to a model serving endpoint is straightforward and efficient. As queries come in from downstream applications—like chatbots or web applications—the serving endpoint delivers responses in real time. If you're building a retrieval-augmented generation (RAG) application, vector search can be utilized as well. Throughout this process, everything happening at the endpoint, from hardware utilization to each request and response, is automatically logged and monitored.

---

### Slide 5: Challenges with building Real-time AI Systems (1/3)

**Title:** Challenges with building Real-time AI Systems
**Subtitle:** Most AI systems don't get into production

**Challenge 1: Infrastructure is hard**

Real-time AI systems require fast and scalable serving infrastructure, which is costly to build and maintain

**Speaker Notes:**
So, what are the challenges in building these kinds of systems? Even though it may sound straightforward, infrastructure can be quite complicated. It's not easy to access GPUs and serve either multiple models or a single model to many users across different regions while also making sure hardware is used efficiently. The main issue is that this hardware is expensive, so getting the most out of what's provisioned is crucial. This is where REST or real-time APIs come in—using them can help ease some of the burden, at least from the consumer's perspective.

---

### Slide 6: Challenges with building Real-time AI Systems (2/3)

**Title:** Challenges with building Real-time AI Systems
**Subtitle:** Most AI systems don't get into production

| Infrastructure is hard | Deploying real time models needs disparate tools |
|------------------------|--------------------------------------------------|
| Real-time AI systems require fast and scalable serving infrastructure, which is costly to build and maintain | Data teams use diverse tools to develop models |
| | Customers use separate platforms for data, LLMs and Serving, adding complexity and cost |

**Speaker Notes:**
If you've ever attempted to set this up on your own, you've probably noticed that it involves working with several different stacks and tools at once, and managing to keep everything stable, connected, and in sync can be pretty challenging.

---

### Slide 7: Challenges with building Real-time AI Systems (3/3)

**Title:** Challenges with building Real-time AI Systems
**Subtitle:** Most AI systems don't get into production

| Infrastructure is hard | Deploying real time models needs disparate tools | Operating production AI requires expert resources |
|------------------------|--------------------------------------------------|---------------------------------------------------|
| Real-time AI systems require fast and scalable serving infrastructure, which is costly to build and maintain | Data teams use diverse tools to develop models | Steep learning curve of deployment tools. |
| | Customers use separate platforms for data, LLMs and Serving, adding complexity and cost | Model deployment is bottlenecked by limited engineering resources, limiting the ability to scale AI |

**Speaker Notes:**
On top of that, there's the ongoing operational effort and engineering hours needed to keep everything running smoothly. Someone has to be ready to step in if anything breaks, plus it's important to always use the latest and best technology in the serving stack. All of these resources and expertise aren't readily available to most individuals who might want to harness the power of generative AI.

---

### Slide 8: Databricks Model Serving - Overview

**Title:** Databricks Model Serving
**Subtitle:** Integrate your model into your websites and applications as an API

| Production-Grade Serving | Accelerate deployments with Lakehouse-Unified Serving | Simplified Deployment |
|--------------------------|-------------------------------------------------------|----------------------|
| **Highly available**, low latency, scalable serving that works for small and large workloads | Automatic feature lookups, monitoring and unified governance that **automates deployment** and reduce errors | Simple and flexible deployment through **UI** or **API** |

**Speaker Notes:**
Finally, Databricks Model Serving streamlines deployment with its user-friendly and flexible UI or API. Creating model endpoints is made easy with just a few clicks, allowing you to swiftly deploy your models.

---

## Part 2: Databricks Model Serving

### Slide 9: Databricks Model Serving

**Title:** Databricks Model Serving
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture Databricks Model Serving, we explore the MLflow development lifecycle and the features of Databricks Model Serving.

---

### Slide 10: MLflow and Development Lifecycle

**Title:** MLflow and Development Lifecycle
**Subtitle:** MLflow integration to seamlessly deploy models

*(Visual: Workflow diagram showing: RAG/Chain Building (Flavor 1, Flavor 2) → Tracking and Evaluation (Parameters, Metrics, Artifacts, Metadata, Models) → MLflow Registry with Unity Catalog (versions v1, v2, v3 with @challenger/@champion aliases) → Databricks Model Serving → REST Endpoint → Dashboards, Applications)*

**Speaker Notes:**
What does this integration with MLflow look like?

Here's a high level picture of a typical lifecycle of an ML model.

In a typical ML model lifecycle, Model Serving is tightly integrated with the Model Registry. The Model Registry allows efficient management and staging of models, while Model Serving facilitates deployment of any version of the model through REST endpoints, providing flexibility and ease of use for real-time applications.

---

### Slide 11: Databricks Model Serving - Unified Platform

**Title:** Databricks Model Serving
**Subtitle:** Unified UI, API & SDK for managing all types of AI Models

*(Visual: Model Serving hierarchy showing three branches)*

**Model Types:**
*   **Custom Models** - Deploy any model as a REST API with Serverless compute, managed via MLflow. CPU and GPU. Integration with Feature Store and Vector Search.
*   **Foundation Models APIs** - Databricks curates top Foundation Models and provides them behind simple APIs. You can start experimentation immediately, without setting up serving yourself. (Meta, DBRX logos)
*   **External Models** - Govern external models and APIs. Previously announced as "AI Gateway" at Data+AI Summit 2023. (OpenAI, Anthropic, AI21 logos)

**Speaker Notes:**
Given that there are so many options available—whether you want to build your own models, use pre-existing open source foundation models, or even tap into proprietary models—all of these can be accessed on the Databricks platform through a unified API or SDK. This setup makes it really simple to switch between models behind the scenes without needing to rewrite either the backend or even the frontend of your system. Essentially, the way you interact with the system remains the same. On top of that, this unified API provides a lot of built-in functionality for monitoring your system right out of the box.

---

### Slide 12: Databricks Model Serving - Production-grade APIs

**Title:** Databricks Model Serving
**Subtitle:** Deploy registered models behind real-time, production-grade APIs

*(Visual: Diagram showing Models in UC → Real-time Endpoint Serving → API Calls)*

**Key Points:**
*   Production-ready, serverless solution to simplify real-time ML model deployment.
*   Deploy models as an API to integrate model predictions with applications or websites.
*   Built-in payload logging and infrastructure/system observability.

**Speaker Notes:**
We offer built-in payload logging, so every time a request comes into the endpoint, it's automatically recorded in a Delta table for ad hoc analysis. In addition to that, infrastructure metrics are also available and can be accessed through the API.

---

### Slide 13: Databricks Model Serving - Benefits

**Title:** Databricks Model Serving
**Subtitle:** Deploy registered models behind real-time, production-grade APIs

*(Visual: Diagram showing Models in UC → Real-time Endpoint Serving → API Calls)*

**Benefits:**
*   Reduces operational costs
*   Streamlines the ML lifecycle
*   Enables Data Science teams to focus on the core task of integrating production-grade real-time ML into their solutions
*   Autoscaling and serverless compute
*   Works with custom, foundational, and external models
*   Built-in A/B testing

**Speaker Notes:**
To summarize the value of Databricks Model Serving, we look at the core benefits it provides when deploying production-grade, real-time APIs.

First, it significantly reduces operational costs and streamlines the ML lifecycle. By handling the complex infrastructure and scaling automatically, it enables Data Science teams to concentrate on their core task: integrating production-grade real-time ML into their solutions.

The platform offers autoscaling and serverless compute, which helps manage the expense and performance challenges we discussed earlier.

Importantly, it provides flexibility by working seamlessly with custom models, Databricks foundational models, and external models.

Finally, it includes built-in A/B testing, which is critical for continuously improving and validating your generative AI systems.

---

### Slide 14: Databricks Model Serving - Online Evaluation

**Title:** Databricks Model Serving
**Subtitle:** Online evaluation

*   Supports online evaluation strategies such as A/B testing or canary deployments through the ability to serve multiple models to a serving endpoint

*(Visual: Screenshot showing model serving endpoint configuration with fraud_classifier/v1 and fraud_classifier/v2 with traffic routing percentages)*

**Speaker Notes:**
The built-in A/B testing capability mentioned on the previous slide is a key feature for online evaluation.

Databricks Model Serving supports sophisticated online evaluation strategies. This includes techniques like A/B testing or canary deployments.

The way this is achieved is through the platform's ability to serve multiple models to a single serving endpoint. For instance, you could route 80% of live traffic to the currently established 'Champion' Model Version 1, and the remaining 20% to a new 'Challenger' Model Version 2 to test its performance in a real-time environment before a full rollout. This ensures that any model promotion is backed by real production metrics.

---

### Slide 15: Databricks Model Serving - Inference Tables (Overview)

**Title:** Databricks Model Serving
**Subtitle:** Inference tables

*(Visual: Unity Catalog diagram showing: UC Volume → Raw/Processed text table(s) (Delta Lake) → Embeddings/Index)*

**Speaker Notes:**
To give you an idea of how monitoring works for a deployed generative AI system within Databricks' serving infrastructure, there's a key feature called the inference table from model serving. This feature allows for effective online monitoring of the system in real time.

---

### Slide 16: Databricks Model Serving - Inference Tables (Details)

**Title:** Databricks Model Serving
**Subtitle:** Inference tables

*(Visual: Extended Unity Catalog diagram showing: UC Volume → Raw/Processed text table(s) → Embeddings/Index → Model/Chain → Model Serving → Inference table)*

**Inference tables** for monitoring and debugging models:
Each **[request-response] is appended to a delta table in Unity Catalog**
*   Use as retraining/fine-tuning dataset for next iteration of your model(s)
*   Perform diagnostics and debugging of suspicious inferences
*   Create a dataset of mislabels data to be re-labele

**Speaker Notes:**
As the name suggests, the inference table is simply a Databricks table created within a chosen catalog and schema, designed to log every request, response, and extra metadata related to a model deployed on a serving endpoint. To break it down: you have a model in your catalog, deploy it using the model serving infrastructure, and once payload logging is enabled, any incoming request to that endpoint is automatically captured in a Delta table called the inference table.

This not only lets you use real-world data to retrain or fine-tune your models in the future but also helps with online diagnosis, debugging, and system monitoring—measuring things like model drift or spikes in toxicity or perplexity. Moreover, it allows you to create sets of mislabeled or relabel-needed data. For example, if a model's response isn't accurate, those instances can be flagged in another table and later used to retrain the model, ensuring it better handles edge cases and remains well-aligned with intended outcomes.
