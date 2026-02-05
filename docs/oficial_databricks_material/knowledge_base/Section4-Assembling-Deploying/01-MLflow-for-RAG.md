# MLflow for RAG Applications

## Slide 1: MLflow for RAG Applications
In this lecture MLflow for RAG Applications, we explore the RAG application workflow, how to assemble a RAG application, and key MLflow features including model tracking, model flavors, and the model registry.

## Slide 2: RAG Application Workflow
Assembly comes into play in the RAG development workflow during the inner loop, where you prepare documents, pipelines, chunking, and embedding models. Once the chain is built and tested, it’s passed to expert or power users, evaluated with an offline harness, and then readied for production. In short, assembly is about putting all components together, validating them, and preparing the chain for deployment.

## Slide 3: Assembling a RAG Application
So far, we’ve ingested our PDFs, cleaned them, calculated embeddings, and stored everything in a vector search index. The next step is to assemble this into a chain. When a user submits a query, it will first be turned into an embedding, then passed to the Mosaic Vector Search for retrieval. The retrieved documents are injected into the chain’s prompt template, which then calls a large language model—in this case, Llama 2. The model generates a completion, and that response is sent back to the user. Essentially, the chain itself stays lightweight, acting only as an orchestrator: the vector search runs on the Mosaic Vector Search index, the completions run on Databricks model serving, and together they provide the final output to the end user.

## Slide 4: MLflow - Using MLflow for RAG solutions
MLflow supports these workflows by providing experiment tracking and evaluation capabilities. It’s an open-source tool, not exclusive to Databricks, even though many contributors are from Databricks. Within the data intelligence platform, MLflow comes with a few extra features and flavors not available in the open-source version, but most of the core features needed for tracking experiments and running evaluations—like those being used today—are accessible in both environments. This means important aspects like experiment management and model evaluation are supported whether you use MLflow on Databricks or as open source.

## Slide 5: MLflow Model Tracking - Make your GenAI workflow more manageable and transparent
As a refresher, the model tracking, or tracking server, lets you log details every time a new chain or model is created. You can record specific LLM parameters like temperature for completions, and many relevant metrics are automatically tracked as well. If you run evaluations or use an eval harness, any artifacts generated during testing can be attached to the run. Plus, it will link directly to the source code used for that run, helping keep everything organized and reproducible.

## Slide 6: MLflow - Model ("Flavor") - Make your GenAI workflow more manageable and transparent
The primary level of support for enabling RAG patterns is the introduction of the LangChain flavor within MLflow models on Databricks. MLflow supports multiple model flavors—from classic options like scikit-learn and XGBoost to PyTorch and more—and now includes LangChain as a flavor as well. This means you can package an entire chain, along with all relevant metadata and lineage information, into a single MLflow model. It’s a significant step forward, making it easy to track, manage, and deploy complete RAG pipelines within the platform.

## Slide 7: MLflow - Model ("Flavor") - Built-in model flavors
Another alternative for chain orchestration, aside from using libraries like Llama Index, is to manually define each step using custom Python code. In these cases, especially for simpler or more restricted chains, you can leverage the pyfunc flavor within MLflow. The pyfunc flavor acts as a flexible model interface, allowing you to package custom chain logic just like any other MLflow model, making deployment and management straightforward even when you build the orchestration yourself.

## Slide 8: MLflow Model Registry - A centralized model store
When a chain is created and relevant parameters are logged, its promotion cycle becomes simple to manage using the model registry. The registry lets you version chains, assign aliases for context based on development stage, and provides lineage tracking out of the box. With these features, you can easily view the full history of a chain—including its connections to specific indexes—through the lineage graph, making it straightforward to track and manage every chain in your workflow.