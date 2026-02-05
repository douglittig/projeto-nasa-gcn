# Slide Content Extraction

This file contains the extracted content from the slide images.

## Slide 1
**Title:** Introduction to Vector Stores  
**Subtitle:** Lecture

**Content:**
*(Visual: Databricks logo, Title text, Abstract graphic with charts)*

**Speaker Notes:**
In this lecture Introduction to Vector Stores, we discuss what vector databases are, why they are popular, common and sample use cases, vector similarity, search strategies, HNSW, product quantization, and the role of reranking.

---

## Slide 2
**Title:** What are Vector Databases?

**Content:**
*   A vector database is a database that is optimized to store and retrieve **high-dimensional vectors such as embeddings**.
*   In RAG architecture **contextual information** is stored in vectors.
*   Vector databases are designed for **efficient storage of vectors** utilized in generative AI applications, which rely on identifying documents or images with similarities.
*   Vector databases provide a query interface that retrieves vectors most similar to a specified query vector.

**Speaker Notes:**
A vector store—or vector database—is a specialized system designed for storing and rapidly retrieving high-dimensional vectors, such as text or image embeddings. In RAG architectures, all contextual information is converted into dense vectors, allowing for semantic similarity search instead of just exact keyword matching. These databases differ from traditional ones by optimizing their storage and indexing structures for efficient similarity search on vectors, and they provide interfaces for querying which results are most similar to a given query vector. Vector databases are commonly used in applications like search engines, recommendation systems, and RAG workflows—enabling large language models to find and use relevant contextual information stored as embeddings. Their flexibility and efficiency with complex, unstructured data types are essential for powering modern AI systems and enabling precise semantic retrieval across vast amounts of data.

---

## Slide 3
**Title:** Why are Vector Databases So Hot?  
**Subtitle:** Query time and scalability

**Content:**
*   Specialized, full-fledged databases for **unstructured data**
    *   Inherit database properties, i.e. Create-Read-Update-Delete (CRUD)
*   Speed up query search for the closest vectors
    *   Uses vector search algorithms such as Approximate Nearest Neighbor (ANN)
    *   Organize embeddings into indices

*(Visual: Comparison between "Traditional search engine" failing to find "Wine for seafood" and "Vector search engine" finding "Covey Run 2005 Chardonnay")*

**Speaker Notes:**
Vector databases are gaining popularity due to their crucial role in generative AI and RAG applications, as they were specifically designed for storing and searching unstructured data in high-dimensional vector form. Unlike traditional databases focused on keyword search, vector databases support rapid similarity queries using specialized algorithms, enabling semantic search, document recommendation, and anomaly detection for large language models and intelligent agents.

These databases offer full CRUD support and advanced indexing mechanisms for organizing embeddings, allowing users to efficiently find contextually relevant vectors out of billions, which is essential for scalable, accurate search and retrieval in modern AI workflows.

---

## Slide 4
**Title:** Common Use Cases for Vector Databases

**Content:**

**RAG**
*   Delivering relevant unstructured documents to help a RAG application answer user's questions.

**Recommendation Engines**
*   Personalized, context aware recommendations to users.
*   More efficient similarity search than traditional approaches. Example; recommending movies with similar genres, actors, or directors to those a user has previously enjoyed.

**Similarity Search**
*   Semantic match, rather than keyword match!
*   Enabling plain language search queries that deliver relevant results.
*   Text, images, audio.
*   Understand similarities and differences between data.

**Speaker Notes:**
Vector databases are used well beyond RAG: core production use cases include recommendation engines (e.g., product or music suggestions) and semantic similarity search that goes past keywords to match meaning. They also enable multimodal retrieval by projecting different data types—text, images and audio—into a shared embedding space so a text description can reliably retrieve the most similar images, clips, or documents.

Once content from each modality is embedded with compatible models, the system can run fast nearest-neighbor queries across those vectors to find the closest matches irrespective of the original format. This lets applications unify search experiences, such as querying with text and getting back relevant images or matching user tastes across songs and products, all powered by the same similarity search primitives.

---

## Slide 5
**Title:** A Sample Use Case  
**Subtitle:** Spotify uses natural language search for their recommendation engine

**Content:**
**Problem:** Fuzzy matching, normalization, and manual aliases cannot capture all variations of user queries.

**Solution:**
*   Match user queries with content that is semantically correlated instead of exact word matching.
*   Used vector search techniques like Approximate Nearest Neighbor (ANN).

*(Visual: Diagram showing mapping of user queries to semantic concepts, e.g., "Are electric cars better for the environment?" -> "electric cars climate impact")*

**Speaker Notes:**
If you really want to get a sense of how recommendation engines work in practice, there’s a great example from a blog post by Spotify. In their write-up, they explain how they go beyond simple keyword matching and instead match a user’s query with content that is semantically related. So rather than only relying on exact word matches, they’re able to understand the deeper meaning behind what someone is looking for. When we think about Spotify, we might usually think in terms of music genres or maybe artist names, but sometimes the things a user is searching for don’t actually appear in a song title, the metadata, or even the artist information. To solve this, Spotify goes into detail about how they build out their recommendation engine, showing how they use vector search techniques—specifically methods like approximate nearest neighbor search—to find and recommend content based on similarity rather than surface-level keyword matches.

---

## Slide 6
**Title:** Vector Search Process and Performance

**Speaker Notes:**
Now let’s try to understand vector search process and performance

---

## Slide 7
**Title:** Vector Similarity  
**Subtitle:** How to measure if 2 vectors are similar?

**Content:**
**Distance Metrics**
*   The **higher** the metric, the **less similar**
*   L2 (Euclidean) is the most popular
*   *(Visual: Euclidean vs Manhattan distance graphs)*

**Similarity Metrics**
*   The **higher** the metric, the **more similar**
*   Cosine similarity is the most popular
*   *(Visual: Cosine similarity angle graph)*

**Speaker Notes:**
Let’s talk about a key metric for finding the closest vectors. In similarity search, we usually measure the distance between vectors, with Euclidean distance (L2) being the most common. A higher distance means vectors are less similar, while a smaller distance means they’re closer. Another approach is cosine similarity, which looks at the angle between vectors through their dot product. A smaller angle means higher similarity. Interestingly, cosine similarity and L2 distance are related—if embeddings are normalized, cosine similarity is just another way of expressing the L2 distance, which in that case never exceeds one.

---

## Slide 8
**Title:** Vector Search Strategies

**Content:**
*   K-nearest neighbors (KNN)
*   Approximate nearest neighbors (ANN)
    *   Trade accuracy for speed gains
    *   Examples of indexing algorithms:
        *   Tree-based: **ANNOY** by Spotify
        *   Proximity graphs: **HNSW**
        *   Clustering: **FAISS** by Facebook
        *   Hashing: **LSH**
        *   Vector compression: **ScaNN** by Google, **Product Quantization (PQ)**

*(Visual: Tree-based ANN search diagram)*

**Speaker Notes:**
So that’s the metric we calculate, but the real challenge is how to do it at scale—when you’re comparing a single query vector against millions or even billions of vectors. Computing distances for all of them directly would be extremely intensive. The question becomes: do we really need to calculate against every single vector, or can we be smarter and narrow the search space? That’s where nearest neighbor algorithms come in. Methods like k-nearest neighbor, or approximate approaches, intentionally trade a bit of accuracy for a big gain in speed by focusing only on the most relevant regions. There’s a wide range of algorithms designed for this, many developed by companies like Spotify, Facebook, and Google. Examples include ANNOY, FAISS, and other libraries built for large-scale similarity search. Among the most widely used are proximity graph–based approaches, which are also adopted in systems like Mosaic AI vector search, as well as many other open-source and proprietary vector databases.

Refer to: Vector Indexing | Weaviate Documentation

---

## Slide 9
**Title:** HNSW: Hierarchical Navigable Small Worlds  
**Subtitle:** Builds proximity graphs based on Euclidean (L2) distance

**Content:**
*   Uses linked list to find the element x: "11"
*   Traverses from query vector node to find the nearest neighbor
*   What happens if too many nodes? Use hierarchy!

*(Visual: Skip list diagram and 3D HNSW layer structure)*

**Speaker Notes:**
In a nutshell, this isn’t meant to be a deep dive into linear algebra or proximity graphs, but the idea behind HNSW, which stands for Hierarchical Navigable Small World graphs, is to construct a proximity graph using measures like the L2 distance. The point is that you don’t calculate the pairwise distance of a query vector against millions of existing vectors in a database. Instead, you start from an entry point in the vector space and navigate step by step. Based on how close that entry point is to the query, you move toward the next closest neighbor and then continue this process. Graph-based techniques help here: essentially, you create linked structures where nearby vectors are connected, embedding distance information in those links. From there, a breadth-first search approach is used to find a short path or the minimal number of hops from the starting point to the query vector. At a high level, that’s what the algorithm is trying to achieve. And if you’re seriously working with retrieval problems, it’s definitely worth digging deeper into the specifics of how HNSW is designed and applied.

Refer to:
*   Hierarchical Navigable Small Worlds (HNSW) | Pinecone
*   IVFPQ + HNSW for Billion-scale Similarity Search | Towards Data Science
*   Understanding Hierarchical Navigable Small Worlds (HNSW) - Zilliz Learn

---

## Slide 10
**Title:** Product Quantization (PQ)  
**Subtitle:** Definition

**Content:**
*   Product Quantization (PQ) is a technique used to **compress high-dimensional vectors** and perform efficient approximate nearest neighbor (ANN) searches.
*   Useful in systems where memory usage and search speed are critical.

*(Visual: Diagram showing Original Vector -> Sub Vectors -> Clustering -> Quantized Vectors -> Compressed PQ Codes)*

**Speaker Notes:**
Product Quantization (PQ) is a technique used to compress high-dimensional vectors and perform efficient approximate nearest neighbor (ANN) searches. It is particularly useful in systems where memory usage and search speed are critical.

---

## Slide 11
**Title:** Product Quantization (PQ)  
**Subtitle:** What is its purpose?

**Content:**
*   **Vector compression:**
    *   Convert vectors to compact codes which reduces memory footprint.
    *   Instead of storing the full detail of every vector, centroid of the clusters are indexed.
*   **Efficient Similarity Search:**
    *   The compressed vectors (PQ codes) enable efficient similarity searches.
    *   Input query doesn't compared with all vectores. Instead, it is compared with centroids of each cluster (the compressed representations instead of the full high-dimensional vectors).
*   **Scalability:**
    *   Suitable for dynamic databases where new data is continuously added.

**Speaker Notes:**
Vector compression converts vectors to compact codes, which reduces memory footprint. Instead of storing the full detail of every vector, centroids of the clusters are indexed.
Efficient similarity search is achieved as the compressed vectors (PQ codes) enable comparisons with centroids of each cluster instead of the full high-dimensional vectors.
Scalability is supported, making it suitable for dynamic databases where new data is continuously added.

---

## Slide 12
**Title:** How to Filter Only Highly Relevant Documents?

**Speaker Notes:**
Now let’s figure out how to filter only highly relevant documents

---

## Slide 13
**Title:** Reranking  
**Subtitle:** A method of prioritizing documents most relevant to user’s query

**Content:**
*   **Initial retrieval**
    *   Not all documents are equally important.
    *   We should use only the relevant documents.
*   **Reranker**
    *   Reorder documents based on the relevance scores.
    *   The goal is to **place most relevant documents at the top** of the list.

*(Visual: Process flow: Query -> Vector Store -> [Docs 1-7] -> Reranker -> [Docs 4, 2, 5])*

**Speaker Notes:**
Now, moving into a more advanced topic, there’s this concept of re-ranking, which comes into play when you want to go beyond simply retrieving results. The typical process starts with running a similarity search, where you get back a list of potential vectors or documents that are close to your query. Usually, these results are ordered by the distance or similarity metric that was used. But in practice, not every document in that list is equally important. Some should be emphasized more, while others might not add as much value. Another issue is redundancy. For example, you might retrieve five different chunks of text that all talk about the same topic, but what you really want is a more diverse set of information covering different angles of your query. That’s where re-rankers come in. Their job is to push the most relevant and important documents to the top while reducing redundancy, so that the final ranking highlights diversity and ensures the most useful content is prioritized.

---

## Slide 14
**Title:** Reranking  
**Subtitle:** A method of prioritizing documents most relevant to user’s query

**Content:**
*   Reranking adjusts the initial ranking of retrieved documents to **enhance the precision and relevance** of search results.
*   Reranking supports **deeper semantic understanding** based on documents’ actual relevance to the query.
*   **Rerankers:**
    *   Private APIs: Cohere ReRank, Jina Rerank
    *   Open-source: Cross-encoders, bge-reranker-base, **FlashRank**

*(Visual: Comparison of Representation-based Comparison (Query <-> Doc via Cosine) vs Reranker (Query & Doc into Model))*

**Speaker Notes:**
At a high level, the way re-ranking works is that it takes the initial list of retrieved documents and adjusts their order to improve both precision and relevance. We’ll get deeper into what those terms mean, but essentially the idea is that while vector search operates in the embedding space, you also want to bring in semantic understanding from the text itself. This means the re-ranking step isn’t just about working with numerical similarity scores but also about interpreting and weighing the actual content of the text. In practice, this creates more of a hybrid approach—one that considers both embeddings and linguistic meaning. There are proprietary APIs provided by vector database vendors and private providers that offer re-ranking capabilities, but there are also plenty of open-source options available. One example is FlashRank, which we’ll be using in our demo and lab exercises. It’s not meant to be a definitive or only solution, but it’s a simple and practical tool to show how re-ranking can be applied to refine retrieved query results.

---

## Slide 15
**Title:** Using Reranking  
**Subtitle:** Benefits and challenges

**Content:**

**Benefits**
*   Select more **relevant documents**.
*   Improve the **accuracy** of the response.
*   Reduce hallucinations.

**Challenges**
*   The LLM must be called repeatedly, increasing the **cost and latency** of the RAG chain.
*   Implementing rerankers adds **complexity** to the RAG pipeline.

**Speaker Notes:**
The main benefit of re-ranking is that it helps ensure only the most relevant documents are kept, which in turn improves the accuracy of the response. A key motivation here is the broader goal of reducing hallucinations by filtering out noise and keeping the context tighter. However, the challenge with re-ranking is that it can come at a cost. Often, it requires calling the LLM multiple times, which increases both latency and expense in the workflow. You might get an initial retrieval, rerun processing based on the LLM’s output, and then perform another pass, which adds layers of complexity to the pipeline. That’s why it’s important to strike a balance—depending on your service-level requirements, you may choose a lighter, initial re-ranking just to cut down on noise, or you might allow for deeper, more iterative re-ranking if higher precision is critical.

