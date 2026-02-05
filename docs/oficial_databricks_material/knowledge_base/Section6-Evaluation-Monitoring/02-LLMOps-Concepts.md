# LLMOps Concepts

## Part 1: MLOps Primer

### Slide 1: MLOps Primer

**Title:** MLOps Primer
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture MLOps Primer, we begin with conventional ML, explore the importance of MLOps, multi-environment semantics, environment separation, deployment patterns, recommended deploy-code architectures for MLOps, and modern LLMOps architecture on a unified platform.

---

### Slide 2: Let us start from conventional ML - What is MLOps

**Title:** Let us start from conventional ML
**Subtitle:** What is MLOps

MLOps is the set of **processes and automation**
for **managing data, code and models**
to **improve performance, stability and long-term efficiency** of ML systems

**MLOps = DataOps + DevOps + ModelOps**

*(Visual: Three icons representing Data (database), Code (brackets), and Models (gear/brain))*

**Speaker Notes:**
Before diving into large language model operations, it's helpful to quickly revisit what machine learning operations, or MLOps, actually involve. MLOps is a set of processes and automated tools designed to manage data, code, and models, ensuring that the model continues to perform as intended over time. A typical machine learning system consists of three main components: the data or features, the models used for training and prediction, and the code that orchestrates interactions between the two.

For each pillar, there are rigorous best practices to ensure quality. The concept of MLOps brings these practices together into one unified workflow, with the goal that everything operates smoothly and in sync. This idea builds on established software development methods like DevOps, combined with specialized tools for experiment tracking, model management, and data operations to create a thorough machine learning lifecycle.

---

### Slide 3: Why does MLOps matter?

**Title:** Why does MLOps matter?
**Subtitle:** Success depends on quality data and operations practices

*   Defining an effective strategy
    *   ML systems built on **quality data**
    *   **Streamlining** process of taking solutions to **production**
    *   Operationalizing **cost & performance monitoring**
*   So what?
    *   Accelerated time to realizing business value
    *   Reduction in manual oversight

**Real-world Example:**
Databricks customer CareSource accelerated their model's development and deployment, resulting in a **self-service MLOps solution for data scientists** that reduced ML project time from 8 weeks to 3-4 weeks.

The CareSource team can extend this approach to other machine learning projects, realizing this benefit broadly.

**Speaker Notes:**
Why is this important? Well, the success of machine learning systems really hinges on following best practices in their operations. That means ensuring data quality, streamlining every stage of the process, and getting models into production as efficiently as possible. It's also crucial to monitor costs and performance so you can speed up time to market and achieve business value quickly.

If things aren't working as expected, having strong operational practices helps you catch problems early, reducing the need for intensive manual oversight or extra engineering work to resolve infrastructure issues.

---

### Slide 4: Multi-environment Semantics

**Title:** Multi-environment Semantics
**Subtitle:** Defining Development, Staging, and Production environments

| Development | Staging | Production |
|-------------|---------|------------|
| An environment where data scientists can **explore, experiment, and develop** | An environment where machine learning practitioners can **test** their solutions | An environment where machine learning engineers can **deploy and monitor** their solutions |

*(Visual: Flow diagram showing progression from Development → Staging → Production with Code, Data, Models icons)*

**Speaker Notes:**
In traditional software development, you're always working across multiple environments. You start with a development environment, which is used for exploring ideas, experimenting, and building out your code. Sometimes there's also a staging environment, where you run functional tests and perform continuous integration or regression testing.

Ultimately, though, whatever you build is meant to end up in the production environment. That's where the system is fully deployed and monitored, powering your most important business applications.

---

### Slide 5: Environment Separation

**Title:** Environment Separation
**Subtitle:** How many Databricks workspaces do we need?

| Direct Separation | Indirect Separation |
|-------------------|---------------------|
| Completed separate Databricks workspaces for each environment | One Databricks workspace with enforced separation |
| Simpler environments | Simpler overall infrastructure requiring less permission required |
| Scales well to multiple projects | Complex individual environment |
| | Doesn't scale well to multiple projects |

*(Visual: Diagrams showing Model Code and Model Artifact flowing through dev → staging → prod for both approaches)*

**Speaker Notes:**
In Databricks, environments can be separated using workspaces—for example, having one for development, one for staging, and one for production. This makes it easier to manage projects, reduce risk, and control access to sensitive or production data, with each workspace serving a specific purpose. Development environments offer flexibility for experimentation, staging is for automated workflow and code verification, and production handles critical applications and monitoring.

Alternatively, you can use a single workspace with strict access controls through Unity Catalog ACLs. This approach is simpler for quick setup and central management, but it requires careful stewardship to maintain permissions, data labeling, and resource limits. While indirect separation simplifies some aspects, it can become harder to scale with many models and projects due to API and hardware constraints. Ultimately, the best setup depends on specific requirements and organizational practices.

---

### Slide 6: Deployment Patterns

**Title:** Deployment Patterns
**Subtitle:** Moving from Deploy Model to Deploy Code

| Deploy Model | Deploy Code (recommended) |
|--------------|---------------------------|
| Model is trained in development environment | Code is developed in the development environment |
| Model artifact is moved from staging through production | Code is tested in the staging environment |
| Separate process needed for other code (inference, monitoring, operational pipelines) | Code is deployed in the production environment |
| | Training pipeline is run in each environment, model is deployed in production |

*(Visual: Diagrams showing Model Code and Model Artifact flows for both approaches through dev → staging → prod)*

**Speaker Notes:**
In the machine learning and generative AI world, deployment can follow two main approaches: deploying code or deploying models. The traditional software route focuses on promoting code through different environments, where code changes determine what happens. In contrast, the deploy model approach allows you to train models in a development environment and then push those models to staging or production, often using automated jobs to handle validation and versioning.

With deploy model, the training happens in development, but the inference, monitoring, and production-side adjustments are addressed separately at the production level. Meanwhile, the deploy code strategy promotes and tests the entire pipeline across all stages—development, staging, and production—ensuring that both code and models are handled together throughout the workflow.

---

### Slide 7: Recommended "deploy-code" architecture (MLOps)

**Title:** Recommended "deploy-code" architecture (MLOps)

*(Visual: Comprehensive MLOps architecture diagram showing Development, Staging, and Production environments with CI/CD pipelines, feature tables, model training, MLflow registry, and monitoring components)*

**Speaker Notes:**
To illustrate how the workflow comes together, imagine starting in the development environment, where data scientists carry out exploratory analysis, build features, write inference and serving code, and train models using available data. Once changes are made, code gets committed to the dev branch, which triggers a pull request and launches unit and integration tests through CI/CD tools like Git Actions or Azure DevOps.

After tests pass, the code is merged into the staging branch to prepare a release, which becomes the reference for deploying in production. In the production environment, models go through feature updates, retraining, promotion, and testing before being deployed for API or batch jobs. Throughout this cycle, monitoring metrics are written back to the lakehouse, with all environments sharing a single source of truth—reinforcing a data-centric approach.

---

### Slide 8: A Single Platform for Modern MLOps

**Title:** A Single Platform for Modern MLOps
**Subtitle:** Combining DataOps, DevOps, and ModelOps solutions

*(Visual: Platform architecture diagram showing layers)*

**Platform Components:**
*   **Model Registry, Model Serving, and Lakehouse Monitoring** (EDA, Data Preparation, Model Development, Model Validation, Model Serving, Data and Model Monitoring)
*   **Data Intelligence Engine** - Use generative AI to understand the semantics of your data
*   **Unity Catalog** - Unified security, governance, and cataloging
*   **Delta Lake** - Unified data storage for reliability, quality, and sharing

**Additional Components:**
*   **Repos** - Code management, version control, and automatic testing
*   **MLOps stack** - Automate the creation of infrastructure for an ML project
*   **Workflows** - DAG-based orchestration, job scheduling
*   **Databricks Asset Bundles** - Provide CI/CD capabilities with a concise and declarative YAML syntax

**Speaker Notes:**
This unified platform approach is central to Databricks Intelligence Platform, allowing DataOps, DevOps, and ModelOps to operate together seamlessly—without the need for separate tools or stacks. In this course, the focus has mainly been on ModelOps, such as creating experiments, tracking progress, promoting models through the registry, serving them, and monitoring their performance. Unity Catalog plays a big part in DataOps too, by letting you track lineage and see how indexes and tables connect to your models and chains.

DevOps, although covered in other modules, completes the picture by handling integration with Git, version control, workflow scheduling, and infrastructure management for machine learning projects. Databricks provides MLOps tools and asset bundles that use a simple, declarative setup for CI/CD and orchestration. Overall, this cohesive platform means you can manage data, code, and models all in one place for efficient and scalable operations.

---

### Slide 9: Recommended LLMOps Architecture

**Title:** Recommended LLMOps Architecture
**Subtitle:** A high-level view of code, data, and GenAI environments

*(Visual: Architecture diagram showing Code Management, Development, Staging, Production environments with Data/System Component Management)*

**Components:**
*   **Code Management** - A single project code repository to be used throughout all environments
*   **Development** - A Databricks workspace (or environment) for exploratory data analysis, **AI system iterated development, establishing of required infrastructure, prototyping, serving**, and monitoring.
*   **Staging** - A Databricks workspace (or environment) for testing the efficacy of the system, including unit tests, integration tests, **risk mitigation tests**, and performance regression tests.
*   **Production** - A Databricks workspace (or environment) for production **AI systems, human data collection**, and system monitoring.
*   **Data/System Component Management** - A single data/system component management solution with access to environment-specific catalogs

**Speaker Notes:**
When it comes to LLM operations, start by developing iteratively in the development environment. This is where you prototype the model, get a sense of infrastructure needs, and learn how to best structure and parse messages for monitoring. In staging, extra risk mitigation steps are crucial—you'll add tests to check model quality and avoid harmful completions before moving forward.

In production, gathering and prioritizing human feedback becomes key, since evaluating unstructured text output is complex and hard to automate. Human insights help guide and improve future model iterations. Throughout, a data-centric approach ensures all environments leverage the same data management and code promotion systems for efficient and reliable operations.

---

## Part 2: LLMOps vs MLOps

### Slide 10: LLMOps vs MLOps

**Title:** LLMOps vs MLOps
**Type:** Lecture

*(Visual: Databricks logo, Title text, Abstract graphic)*

**Speaker Notes:**
In this lecture LLMOps vs MLOps, we explore LLMOps concepts, development and deployment patterns, packaging and governance, cost and performance considerations, human feedback, adapting MLOps for LLMs, and the use of Databricks Asset Bundles.

---

### Slide 11: What About LLMOps?

**Title:** What About LLMOps?
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps by area

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|
| The workflows and patterns that practitioners follow when developing machine learning and generative AI solutions | The composition of entire machine learning and generative AI applications in order to effectively deliver and scale solutions | The deployment of machine learning and generative AI applications for output storage or delivery to the end user. | The access control and management of APIs used as a part of the machine learning or generative AI application. | The constant measurement and evaluation of the cost of developing and maintaining the application and its value and performance in production. | The inclusion of data generated by humans into the evaluation or iteration of machine learning and generative AI applications. |

**Note:** We'll walk through each of these areas and map to the LLMOps reference architecture.

**Speaker Notes:**
To compare MLOps with LLMOps, it's helpful to focus on a few important areas as you begin your LLM development journey. First, there are development patterns—these are the workflows and best practices used when building either traditional machine learning or generative AI solutions. Packaging models is another aspect, and although we've touched on it before, it's worth emphasizing how model packaging differs for ML and LLM systems as part of a bigger picture.

Serving models efficiently is crucial, along with ensuring enough storage for prediction outputs. API governance is increasingly important: as more systems rely on APIs for model access, strong controls are needed to prevent misuse and manage infrastructure and hardware responsibly. Costs and performance take on new dimensions, where thinking in terms of tokens—especially with API usage—is essential. Finally, incorporating human feedback remains vital for improving quality and guiding future iterations.

---

### Slide 12: Development Patterns in LLMOps

**Title:** Development Patterns in LLMOps
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|

*   **Incremental** development patterns
    *   Developers typically **start with off-the-shelf external models and move toward more custom models** through RAG, fine-tuning, or pre-training
*   Inclusion of **text templates**
    *   Many interfaces to GenAI solutions **include text templates** to facilitate LLM behavior within the application – these must be developed, iterated on, and managed as part of an LLM pipeline

**Speaker Notes:**
Development in LLMOps is still iterative and incremental, but unlike ML, you're not usually starting by training a model from scratch. Instead, most workflows begin by consuming off-the-shelf proprietary models offered through APIs—for example, from providers like OpenAI or Anthropic. As you gain experience and see which models address your use case, you may move toward customizing models, fine-tuning, or creating solutions tailored to your specific data and tasks.

A key difference with language models is the importance of prompt engineering. Using text templates or prompt templates becomes a critical new aspect; these help track and structure the different styles and methods of prompting each model. Since every model responds best to unique prompts based on its own training, maintaining prompt templates brings rigor and flexibility, ensuring they're a core component in your LLM pipeline.

---

### Slide 13: Packaging Artifacts in LLMOps

**Title:** Packaging Artifacts in LLMOps
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|

*   **Package entire applications**
    *   Rather than deploying a single model, large applications need to be packaged and deployed together
    *   This can include calls to other LLMs or GenAI applications as a part of a deployed pipeline
*   **Environment configurations**
    *   Additional configurations need to be made to the package environment to manage things like other endpoints and embeddings, including testing external systems are working

**Speaker Notes:**
When it comes to packaging, the approach is quite different from traditional ML. Instead of creating a single, atomic artifact that simply takes an input and instantly provides an output, you're often constructing a more complex pipeline or chain. This system may need to interact with various other services and components.

Because of this, each connected service or model in the chain will likely require separate environment configurations, such as unique tokens or access credentials. The packaging process, therefore, needs to account for these dependencies to ensure everything operates smoothly together.

---

### Slide 14: Recommended "deploy-code" architecture (LLMOps) - Development

**Title:** Recommended "deploy-code" architecture (LLMOps)

*(Visual: Architecture diagram highlighting the model training section)*

**Callouts:**
*   "Model" may be a model (LLM) or a pipeline (e.g., LangChain chain). It may also call other services like vector databases.
*   "Model training" may be replaced by 1 or more of: Model fine-tuning, Pipeline tuning, Prompt engineering

**Speaker Notes:**
Mapping these topics back to the architecture, dev patterns and packaging mainly sit at the model training stage. Instead of training straight away, you'll usually begin with prompt engineering. As you progress or have enough data, you may fine-tune models, whether simple or complex—sometimes running locally or interacting with external services. Tying this to the architecture, dev patterns and packaging are part of the model training process. You often start with prompt engineering, then move to fine-tuning as you gain data or experience. Models can range from complex pipelines with external interactions to simple solutions running on local GPUs.

---

### Slide 15: Serving Applications in LLMOps

**Title:** Serving Applications in LLMOps
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|

*   **Additional components like vector databases**
    *   When augmenting LLM applications with contextual data, new systems like vector databases need to be set up and used for scale
*   **GPU infrastructure**
    *   Due to the size of language models used in many applications, GPUs are required for the serving and deployment of AI systems
*   **User interface components**
    *   While some might choose to manage this separately, developers might need to include end user interface components as a part of their serving deployment

**Speaker Notes:**
In the serving stack for LLM systems, you're not just deploying a simple CPU endpoint. If you're building a RAG or recommendation system, vector databases become an important new part of your infrastructure, supporting efficient retrieval and augmentation. It's also critical to manage GPU resources if serving your own models, weighing cost and utilization since idle GPUs are expensive and difficult to manage.

Another key point is the need for a user interface—especially when handling multi-turn conversations and collecting human feedback. If you lack a UI/UX team, tools like Gradio or Streamlit make it easier to build applications. Databricks also enables scaling these apps through Lakehouse apps, though deploying containers at scale can still be complex.

---

### Slide 16: Recommended "deploy-code" architecture (LLMOps) - Serving

**Title:** Recommended "deploy-code" architecture (LLMOps)

*(Visual: Architecture diagram highlighting the production serving section)*

**Callout:** Different production tooling: big models, vector databases, etc.

**Speaker Notes:**
In LLM systems, serving goes beyond just standard CPU endpoints. You might be running CPU serving, vector search serving, and even offering user interfaces. This means you're combining multiple types of production tooling—not just relying on traditional Kubernetes containers, but adding layers to support efficient search and real-time interactions. With LLMs, serving isn't limited to basic CPU endpoints—you're often supporting CPU serving, vector search serving, and potentially user interfaces too. As a result, your production environment involves diverse tooling, not just typical Kubernetes containers, to handle these multiple layers.

---

### Slide 17: API Governance in LLMOps

**Title:** API Governance in LLMOps
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|

*   **Managing access to endpoints**
    *   With the addition of new endpoints being created for various components of the project, access to those endpoints needs to be governed
*   **Governing use of application**
    *   Calls to endpoints should be logged and reviewed regularly to evaluate abuse
    *   Guardrails can be put in place to prohibit future abuse

**Speaker Notes:**
If you're like most users without the resources or expertise to deploy your own GPUs, you'll rely on APIs for serving models. Managing API access is critical—just like controlling access to data and endpoints—so your tokens and credentials don't get leaked or abused.

Mitigation involves setting rate limits for each token, a feature most API providers offer. In Databricks, when you set up an endpoint that calls an external model, you associate it with a token already configured with specific rate limits, all managed through a unified API system. For users who rely on APIs rather than running their own GPU servers, it's crucial to manage access to those APIs to prevent token leaks and credential overuse. Most providers allow you to create tokens and set rate limits for groups or business units. In Databricks, when spinning up a model endpoint that uses an external service, you assign a rate-limited token—all managed through a single, unified API.

---

### Slide 18: Cost and Performance in LLMOps

**Title:** Cost and Performance in LLMOps
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|

*   **Model size increases cost**
    *   LLMs are larger in size, and frequently result in more cost
*   **(API-based) Models have use-based cost**
    *   (External/FMAPI) Models offers per-token based pricing that needs to be considered
*   **Techniques for reducing model size/cost**
    *   Reduce model size
    *   Reduce number of queries to external models, if possible (use "caching")
    *   Reduce query input and/or constraint output size

**Speaker Notes:**
When it comes to cost and performance, larger models demand more infrastructure and result in higher expenses. If you're using APIs, you enter a "tokenomics" world—paying based on how many input and output tokens you use. Reducing model size and fine-tuning on your specific data can lower costs without sacrificing performance.

Other cost-saving measures include reducing the number of queries by caching repeat questions and trimming input length through summarization or prompt engineering. Fine-tuning generation parameters to set maximum output tokens also helps you control expenses and predict ongoing costs based on historical app usage.

---

### Slide 19: Recommended "deploy-code" architecture (LLMOps) - Cost

**Title:** Recommended "deploy-code" architecture (LLMOps)

*(Visual: Architecture diagram highlighting cost considerations)*

**Callouts:**
*   If model training or tuning are needed, managing cost and performance can be challenging.
*   Larger cost, latency, and performance tradeoffs for model & vector index serving, especially with 3rd-party APIs.

**Speaker Notes:**
Mapping this back to the architecture, if you're simply consuming models via prompt engineering or RAG, there are no training costs. Fine-tuning is relatively inexpensive and made easy with tools like Mosaic AI's fine-tune API. However, pre-training a model can be costly—the larger the model and the more tokens used for training, the higher the expense, especially with factors like number of epochs impacting costs.

Most of the expenses in generative AI systems come from the serving side—whether paying for tokens when using APIs or managing your own infrastructure. This includes keeping endpoints, vector databases, and structured databases like Databricks' online stores operational and highly available, as these components support prompt augmentation and increase overall system complexity and cost.

---

### Slide 20: Human Feedback in LLMOps

**Title:** Human Feedback in LLMOps
**Subtitle:** Comparing and contrasting LLMOps from traditional MLOps

| Dev Patterns | Packaging | Serving | API Governance | Cost and Performance | Human Feedback |
|--------------|-----------|---------|----------------|---------------------|----------------|

*   **Collection of data**
    *   Explicit satisfaction (i.e. with 👍 and 👎)
    *   User queries
    *   Human/Users corrections/suggestions
*   **Use of data (managed!)**
    *   Response examples
    *   Tests
    *   Architectural/strategic decisions

**Speaker Notes:**
A major new focus in LLMOps is collecting human feedback. Whether in chatbots or other applications, allowing users to rate their experience, provide thumbs up or down, and suggest better answers is extremely valuable. If users contribute this feedback, it offers rich data to improve models.

You can use this human feedback for reinforcement learning or to build higher-quality labeled datasets for fine-tuning, ultimately pushing model quality to the next level.

---

### Slide 21: Adapting MLOps for LLMs

**Title:** Adapting MLOps for LLMs

*(Visual: Architecture diagram highlighting human feedback and monitoring integration)*

**Callouts:**
*   Human/user feedback may be an important datasource from dev to prod.
*   Traditional monitoring may be augmented by a constant human feedback loop.

**Speaker Notes:**
Beyond standard monitoring, integrating user feedback into your UI or UX is crucial. By linking feedback directly to data sources, you strengthen the connection between model performance and user experience.

Collecting feedback in production, development, and staging is possible—for example, by inviting power users to test and review your application in staging. This crowdsourced approach helps catch risks and correct issues early, reducing the chance of negative outcomes in the live environment. In addition to traditional monitoring, integrating feedback features into your UI or UX lets users provide valuable input directly tied to specific data. Linking this feedback to your data sources strengthens model evaluation and iteration.

This approach isn't limited to production; it also works in development or staging. Crowdsourcing feedback from power users during testing helps identify and address issues before deployment, making your generative AI systems safer and more reliable.

---

### Slide 22: Databricks Asset Bundles (DABs)

**Title:** Databricks Asset Bundles (DABs)

*(Visual: Dark title slide with DABs highlighted in orange)*

**Speaker Notes:**
We have discussed the LLMOps architecture and the recommended 'deploy-code' approach across development, staging, and production environments. Now, we need the tool that makes this entire process repeatable, reliable, and production-ready. This is where Databricks Asset Bundles, or DABs, come in.

---

### Slide 23: Databricks Asset Bundles - Overview

**Title:** Databricks Asset Bundles
**Subtitle:** Where are bundles used?

| Write code once, deploy everywhere | What are Databricks Asset Bundles? | How do bundles work? |
|------------------------------------|-----------------------------------|---------------------|
| **YAML** files that specify the artifacts, resources, and configurations of a Databricks project. | The **new databricks CLI** has functions to **validate, deploy and run** Databricks Asset Bundles using bundle.yml files | Bundles are useful during **development and CI/CD** processes |

**Speaker Notes:**
Databricks Asset Bundles provide a solution for the ideal goal of writing code once and deploying it everywhere.

What are Databricks Asset Bundles? They are defined using YAML files that specify all the artifacts, resources, and configurations necessary for a Databricks project.

How do bundles work? The new Databricks CLI includes functions to validate, deploy, and run these bundles using the bundle.yml file. Bundles are particularly useful during development and CI/CD processes as they automate the transition between environments. They consolidate complex setup steps into a concise, declarative syntax.

---

### Slide 24: A Closer Look

**Title:** A Closer Look

*(Visual: Screenshot of bundle.yml file with annotations)*

**Components:**
*   **Name and default Workspace** - Establishes the context for the project
*   **Resource configurations** - Jobs, DLT pipelines, MLflow, etc. Follows REST API schema for configuration.
*   **Environment-based specs** - Control project behavior in different environments

**Speaker Notes:**
A closer look at the bundle.yml file reveals its structured nature. It starts by defining the name and default Workspace, establishing the context for the project.

Next, it specifies the Resource configurations. These define resources such as Jobs, DLT pipelines, or MLflow components. This resource section follows the REST API schema for configuration.

Finally, and most critically for LLMOps, it contains Environment-based specs. These specifications allow you to control project behavior—such as cluster size, schedule, or access permissions—differently across environments like staging and production.

---

### Slide 25: Where Can We Use Bundles? - Development

**Title:** Where Can We Use Bundles?
**Subtitle:** As part of active development

*(Visual: Developer "Alice" using CLI commands with Dev environment diagram)*

**Commands:**
```
$ databricks bundle deploy -t "development"
$ databricks bundle run pipeline --refresh-all -t "development"
```

**Key Points:**
*   Deploy and run your project, tweak configs, deploy and test changes
*   Deploy to multiple workspaces for testing differences
*   Deploy and run from IDEs, terminals, or Databricks

**Speaker Notes:**
1. Bundles are integral to the active development phase.
2. As a developer, you can use simple CLI commands, such as databricks bundle deploy -t "development", to deploy your project, tweak configurations, and immediately test changes.
3. You can deploy and run your project from various interfaces like IDEs, terminals, or Databricks notebooks. This functionality allows for deploying to multiple workspaces for testing specific differences or isolation.

---

### Slide 26: Where can we use bundles? - CI/CD

**Title:** Where can we use bundles?

*(Visual: Source control flow diagram showing Dev → Staging → Prod with CI/CD integration)*

**Commands for Staging:**
```
$ databricks bundle deploy -t "staging"
$ databricks bundle run pipeline --refresh-all -t "staging"
```

**Commands for Production:**
```
$ databricks bundle deploy -t "production"
$ databricks bundle run pipeline refresh-all -t "production"
```

**Key Points:**
*   Executed on CI/CD server (e.g. GitHub Actions)
*   Triggered by CI or release pipelines
*   Ideally run as service principal

**Speaker Notes:**
When moving beyond development, bundles become the core of your automation pipeline.

Bundles are executed on a CI/CD server, such as one running GitHub Actions. They are triggered automatically by CI or release pipelines whenever code is merged or promoted.

The commands, like databricks bundle deploy -t "staging" or databricks bundle deploy -t "production", target the specific configurations for those environments, as defined in the bundle.yml file.

It is highly recommended that these automated runs be executed as a service principal rather than an individual user to ensure secure, reliable, and traceable deployments.

---

### Slide 27: Benefits of Using DABs

**Title:** Benefits of Using DABs
**Subtitle:** Write code once, deploy anywhere

*   **Democratizing best practices for CI/CD and project management**
    *   Co-version configs with code and resources
    *   Automation friendly (CLI vs. 1000 REST calls)
    *   Collaborate and deploy with confidence (isolation, automated testing, etc)
*   **Unified, single way to define and deploy your projects**

**Speaker Notes:**
The overarching benefit of using Databricks Asset Bundles is the unified approach to project deployment.

DABs are essential for democratizing best practices for CI/CD and project management. They achieve this by enabling you to co-version configurations alongside code and resources.

This approach is highly automation friendly, translating potentially thousands of individual REST API calls into simple CLI commands.

Ultimately, DABs provide a unified, single way to define and deploy your projects, allowing teams to collaborate and deploy with confidence through isolation and automated testing.
