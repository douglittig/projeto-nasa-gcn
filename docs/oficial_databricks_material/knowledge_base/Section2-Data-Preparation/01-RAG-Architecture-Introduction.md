# Slide 18: Introduction to RAG

**Title:** Introduction to RAG
**Type:** Lecture

**Visuals:**
- Databricks logo.
- Abstract graphic showing a screen with analytics and a podium-like shape.

**Speaker Notes:**
In this lecture Introduction to RAG, we explore how language models learn knowledge, the role of context in factual recall, the concept of RAG, its use cases, main workflow concepts, benefits of its architecture, and how the RAG workflow maps to Databricks features.

---

# Slide 19: How do Language Models Learn Knowledge?

**Title:** How do Language Models Learn Knowledge?

**Three Approaches:**

1.  **Model Pre-Training**
    *   Training an LLM from scratch
    *   Requires large datasets (billions to trillions of tokens)
    *   *Icon:* Network diagram

2.  **Model Fine Tuning**
    *   Adapting a pre-trained LLM to specific data sets or domains
    *   Requires thousands of domain-specific or instruction examples
    *   *Icon:* Wrench and screwdriver

3.  **Passing Contextual Information** (Focus of this course)
    *   Combining an LLM with external knowledge retrieval
    *   Requires external knowledge base
    *   *Question:* How do we use vectors to search and provide **relevant context** to LLMs?
    *   *Icon:* Document and flow arrow

**Comparison:**
A large arrow indicates "LESS Complexity and Compute-intensiveness" moving from Pre-Training towards Passing Contextual Information.

**Speaker Notes:**
Retrieval augmented generation (RAG) offers a lightweight approach for working with language models, as it skips model training or fine-tuning and instead focuses on giving the model relevant context to improve responses. Rather than making complex changes to the model, RAG simply feeds the LLM the right information, resulting in more accurate answers specific to the data of interest. This course will focus on using RAG for effective interactions with language models.

---

# Slide 20: Passing Context to LMs Helps Factual Recall

**Title:** Passing Context to LMs Helps Factual Recall

**Key Points:**
*   **Passing context** as model inputs improves factual recall
    *   *Analogy:* Take an exam with **open notes**
*   LLMs are evolving to accept a larger/infinite input token window size

**Downsides of "Long" context:**
*   Higher API costs (# input token)
*   Longer completion/inference times
*   Content/documents in the middle may be overlooked ([Lost in the middle](https://arxiv.org/abs/2307.03172) and [needle in haystack test](https://github.com/gkamradt/LLMTest_NeedleInAHaystack))

**Conclusion:**
=> Ongoing research to address "context limitation"

**Speaker Notes:**
Providing context to a language model helps maximize factual recall, especially since models are limited by their training cutoff dates and may not know recent or specific information. Feeding only relevant context keeps costs and processing time lower, as larger input windows are more expensive and can cause the model to overlook important details. Retrieval augmented generation remains essential as it efficiently supplies focused information to the model for better, more accurate responses. Context makes model responses more accurate since it helps overcome the limitations of training cutoffs or missing recent data. Including only relevant context reduces cost and speeds up inference, as large prompts can be pricey and distract the model. Retrieval augmented generation is an effective and evolving strategy for supplying models with precise, focused information.

---

# Slide 21: So what is RAG?

**Title:** So what is RAG?

**Visuals:**
Dark title slide.

**Speaker Notes:**
Now let's try to understand what is RAG?

---

# Slide 22: RAG is...

**Title:** RAG is...

**Definition:**
Retrieval Augmented Generation, or RAG;

*   Is a pattern ([Lewis et al. 2020](https://arxiv.org/abs/2005.11401)) that can improve the **efficacy** of large language model (LLM) applications by **leveraging custom data**.
*   Is done by **retrieving** data/documents relevant to a question or task and providing them as context to **augment** the prompts to an LLM to improve **generation**.

**Diagram:**
1.  **Retrieve domain specific context:** Query -> Find Similar docs
2.  **Prompt:** Combines Query + Similar doc1 + Similar doc2...
3.  **LLM:** Generates response based on Prompt.

**Speaker Notes:**
Retrieval augmented generation (RAG) is a technique first coined by Meta that improves language models by letting them use your own data. It works by retrieving relevant documents or information in response to a question and then feeding these directly into the model's prompt, helping the model provide more accurate and relevant answers.

---

# Slide 23: RAG is... (continued)

**Title:** RAG is...

**Key Point:**
*   The main problem that is solved with RAG architecture is the **knowledge gap**. This approach enhances the accuracy and relevance of responses.

**Diagram:**
Retrieval Augmented Generation flow:
1.  Query
2.  Retrieve domain specific context
3.  Prompt (Query + Similar doc1 + Similar doc2...)
4.  LLM generates response

**Speaker Notes:**
The main problem solved by RAG is the knowledge gap that arises from models being trained on outdated or limited data. By retrieving and adding recent or relevant information to the model's prompt, RAG helps produce more accurate responses for questions about content the model was not originally trained on.

---

# Slide 24: RAG Use Cases

**Title:** RAG Use Cases
**Subtitle:** Some practical use cases

**Three Use Cases:**

1.  **Q&A Chatbots**
    *   Incorporate LLMs with chatbots to automatically derive more accurate answers.
    *   Used to automate customer support and website lead follow-up to answer questions and resolve issues quickly.

2.  **Search Augmentation**
    *   Incorporating LLMs with search engines that augment search results with LLM-generated answers.
    *   Makes it easier for users to find the information they need.

3.  **Content Creation and Summarization**
    *   Facilitate the development of high-quality articles, reports, and summaries using additional context.
    *   Example: generation of news articles or summarization of lengthy reports.

**Speaker Notes:**
Retrieval augmented generation is commonly used in Q&A chatbots, which search relevant documentation and summarize answers for users rather than just returning a list of links. RAG also improves search augmentation by enabling broader and more accurate results, and it assists content creation by compiling information from existing resources to help generate targeted content.

---

# Slide 25: Main Concepts of RAG Workflow

**Title:** Main Concepts of RAG Workflow
**Subtitle:** Components and concepts in search and RAG workflow

**Four Components:**

1.  **Index & Embed:**
    *   An embedding model used for creating **vector representation** of the documents and user queries.

2.  **Vector Store:**
    *   Specialized to store unstructured data indexed by vectors. Vectors can be stored with a **vector DB, library, or plugin**.

3.  **Retrieval:**
    *   Search stored vectors using similarity search to efficiently **retrieve relevant information**.

4.  **Filtering & Reranking:**
    *   The process of selecting or ranking retrieved documents before passing as context.

**Speaker Notes:**
The main components behind RAG are indexing and embedding, where text is converted into vector representations for efficient searching and storage, often in specialized vector databases. When a question is asked, it's also turned into a vector and compared against stored vectors to retrieve the most relevant information, with optional filtering or re-ranking to improve the quality of the results.

---

# Slide 26: Main Concepts of RAG Workflow (continued)

**Title:** Main Concepts of RAG Workflow
**Subtitle:** Components and concepts in search and RAG workflow

**Two Additional Components:**

1.  **Prompt Augmentation:**
    *   Prompt engineering workflow to **enhance context via injection of data retrieved** from Vector store

2.  **Generation:**
    *   A large language model used for generating a response for the user's request.

**Speaker Notes:**
After retrieving and possibly filtering the relevant information, this content is injected into the prompt provided to the language model. The model then uses both the retrieved data and the question to generate an answer, producing a response that is informed by the added context.

---

# Slide 27: Retrieval Augmented Generation (RAG) - Architecture

**Title:** Retrieval Augmented Generation (RAG)
**Subtitle:** A sample architecture

**Architecture Diagram:**

1.  **Document Embedding** (top section)
    *   Source PDF documents
    *   Language Model converts chunks/docs to embeddings
    *   Stored in database

2.  **User Query** (bottom left)
    *   User asks a question
    *   LLM converts query to embeddings
    *   Similarity search performed

3.  **Generation Model** (bottom right)
    *   Similar chunks/documents are passed as context/memory
    *   LLM augments and generates completion
    *   User receives an answer

**Speaker Notes:**
To help visualize the architecture of a retrieval augmented generation (RAG) system, think of it as combining two main components: dense vector retrieval and in-context learning. Dense vector retrieval refers to the process of searching using vector representations of your text data, while in-context learning means the language model uses retrieved information as context for generating answers. Before you start retrieving with vectors, there's a key preparation step: you create vector representations of all your source textual data. This way, the retrieval can efficiently find relevant information to provide meaningful context for generation.

---

# Slide 28: Retrieval Augmented Generation (RAG) - Document Embedding

**Title:** Retrieval Augmented Generation (RAG)
**Subtitle:** A sample architecture

**Databricks features highlighted for Document Embedding:**
*   Delta Live Tables (batch/stream ingestion)
*   Mosaic AI Model Serving (Embeddings):
    *   Foundation Models
    *   External Models

**Speaker Notes:**
Here's an example using PDFs, which is what will be covered in the demos and lab. The first step involves ingesting documents—a process that can be done once or scheduled periodically depending on how often the knowledge base changes. After ingestion, the documents may be chunked into smaller pieces instead of embedding them as single blocks. Each chunk or document is then converted into its own vector embedding. In Databricks, tools like Delta Live Tables can help with ingesting both structured and unstructured data, though that's not covered in this module. Once the text data has been ingested and prepared, Databricks' foundation models from the model serving stack can be used to generate embeddings. These out-of-the-box models or third-party providers—such as OpenAI—are supported by the Mosaic model serving stack, and you can even configure endpoints to use external embedding models. The workflow uses either Delta Live Tables or a notebook to slice and dice data, followed by the model serving stack to transform the textual documents into their embedding vectors.

---

# Slide 29: Retrieval Augmented Generation (RAG) - User Query

**Title:** Retrieval Augmented Generation (RAG)
**Subtitle:** A sample architecture

**Databricks features highlighted for User Query:**
*   Mosaic AI Model Serving (Embeddings)
*   Mosaic AI Vector Search

**Speaker Notes:**
Now, focusing on the dense vector retrieval part, here's what happens: when a user asks a question, that question gets converted into its own vector embedding. With this embedding, the system searches through the existing collection of vector representations of documents using similarity search. This process identifies which documents or document chunks are most relevant to the user's query. To perform this similarity search, the same embedding model used for the original documents is also applied to the question, typically using the Mosaic AI serving stack. The Mosaic AI Vector Search then finds the vectors that are closest to the query's embedding and returns the matching sources and chunks of text that best answer the question.

---

# Slide 30: Retrieval Augmented Generation (RAG) - Generation Model

**Title:** Retrieval Augmented Generation (RAG)
**Subtitle:** A sample architecture

**Databricks features highlighted for Generation Model:**
*   Unity Catalog's Model registry
*   Mosaic AI Model Serving:
    *   Foundation Models
    *   Custom Models

**Speaker Notes:**
Once the relevant chunks of text are retrieved, the process moves to in-context learning. Here, those chunks are injected into a prompt, which is then sent to a large language model (LLM) so it can generate a complete response. To streamline and package this workflow—combining dense vector retrieval and in-context learning—it's built as a chain and logged as a model within Unity Catalog's model registry. This model records all steps: converting the question to an embedding, running a similarity search, injecting the results into the prompt, and sending it to the LLM for output. You can use LLMs provided by foundation model APIs or serve your own custom models via the Mosaic AI model serving stack. The entire chain is deployed as a custom model, and key platform components—model serving, vector search, registry, and MLflow—are covered in demonstrations throughout the module.

---

# Slide 31: Benefits of RAG Architecture

**Title:** Benefits of RAG Architecture
**Subtitle:** Key benefits

**Two Key Benefits:**

1.  **Up-to-date and accurate responses**
    *   LLM responses are not based solely on static training data.
    *   The model uses **up-to-date external data** sources to provide responses.

2.  **Reducing inaccurate responses, or hallucinations**
    *   RAG attempts to mitigate the risk of producing "**hallucinations**" or incorrect information.
    *   Outputs can include citations of **original sources**, allowing human verification.

**Speaker Notes:**
RAG is important because it helps ensure responses from language models are up-to-date and relevant to specific data, which can reduce hallucinations when the retrieved documents are accurate. It also allows the answer to be linked to its sources, making it easier to fact-check and verify the model's completions.

---

# Slide 32: Benefits of RAG Architecture (continued)

**Title:** Benefits of RAG Architecture
**Subtitle:** Key benefits

**Two Additional Benefits:**

1.  **Domain-specific contextualization**
    *   Can be tailored to interface with **proprietary or domain-specific** data.
    *   Improves the accuracy of the response by using contextually relevant information.

2.  **Efficiency and cost-effectiveness**
    *   Offers an alternative to fine-tuning LLMs by enabling in-context learning **without the up-front overhead of fine-tuning**.
    *   Beneficial where models need to be frequently updated with new data.

**Speaker Notes:**
Other benefits of RAG include its ability to handle highly domain-specific questions by passing only relevant context to the model. It also lowers costs and improves efficiency, since you can avoid training new models and simply update your index with new data as needed.

---

# Slide 33: Mapping the RAG Workflow to Databricks Features

**Title:** Mapping the RAG Workflow to Databricks Features

**Mapping Summary:**

1.  **Find Relevant Context -> Mosaic AI Vector Search**
    *   Built into the Databricks Intelligence Platform.
    *   Integrated with governance and productivity tools.
    *   Create and automatically sync with the underlying Delta table.

2.  **Generate Response -> Mosaic AI Model Serving**
    *   State-of-the-art **foundation models** (e.g. Llama-3) and **external models** (e.g. GPT-4) made available by **Foundation Model APIs**.
    *   **Mosaic AI Playground:** Interact with supported models.

3.  **Serve RAG Chain -> Mosaic AI Model Serving**
    *   Unified interface for deploying and querying models.
    *   Low-latency, high-availability model deployment service.
    *   Scales up or down to meet demand changes.

**Speaker Notes:**
The RAG workflow in Databricks is enabled through Mosaic AI's integrated features. Vector Search retrieves context directly from Delta Tables, which are automatically updated and synced with enterprise data. Model Serving then generates and delivers responses in real time, supporting both cutting-edge foundation models like Llama-3 and external APIs such as GPT-4. With the Mosaic AI Playground, users can easily experiment and validate models before deployment. The platform's governance and productivity tools ensure security, compliance, and collaboration, while its low-latency, scalable serving infrastructure adapts to changing demand. This makes Databricks a unified, enterprise-ready solution for building and managing RAG-based applications.
