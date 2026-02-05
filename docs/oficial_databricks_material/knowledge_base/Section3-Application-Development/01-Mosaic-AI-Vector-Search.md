# Slide Content Extraction

This file contains the extracted content from the slide images in mosaic_ai_vector_search.

## Slide 1
**Title:** Introduction to Mosaic AI Vector Search  
**Subtitle:** Lecture

**Content:**
*(Visual: Databricks logo, Title text, Abstract graphic with charts)*

**Speaker Notes:**
In this lecture Introduction to Mosaic AI Vector Search, we cover what Mosaic AI Vector Search is, how vector search works, and how to set it up.

---

## Slide 2
**Title:** Mosaic AI Vector Search

**Content:**
*   Stores vector representation of your data, plus metadata
*   Tightly integrated with your Lakehouse
*   Scalable, low latency production service with zero operational overhead
*   Supports ACLs using Unity Catalog integration
*   API for real-time similarity search
    *   Query can include filters on metadata
    *   REST API and Python client

**Speaker Notes:**
Mosaic AI Vector Search allows us to store vector representations alongside metadata. For example, as shown earlier in the embeddings table demo, you can have an embedding plus additional fields, columns, or tags that can be used for pre- or post-filtering. It’s fully integrated with the lakehouse, so you’re not spinning up a separate stack to manage or sync with your existing data. It’s designed to be scalable, low latency, and production grade, with SLAs in mind. It also leverages the same access control model you might know from Unity Catalog, where the same principles that apply to data and models now also apply to indexes. On top of that, it provides an API that supports real-time search, accessible through both a REST API and a Python client.

---

## Slide 3
**Title:** How does Vector Search Work?  
**Subtitle:** Method 1: Delta Sync API with managed embeddings

**Content:**
**Features:** automatic sync, fully managed embeddings

*(Visual: Diagram showing Source Delta Table -> Auto Sync -> Indexer (Embedding Generation) -> Vector DB -> Query Engine -> REST API/Python SDK)*
*   **Source Delta Table:** id, text, col1, col2
*   **Mosaic AI Vector Search Engine:** Indexer, Vector DB, Query Engine
*   **Mosaic AI Model Serving:** Embedding Model (Custom Models, External Models, Foundational Models)

**Speaker Notes:**
So once you have a source Delta table, there are a couple of options to enable vector search. The first option is what’s called a fully managed embedding. In this setup, you don’t need to pre-calculate the embeddings yourself. Instead, your Delta table might contain several columns, and one of them will hold the text of interest. When you enable or create a vector index from that table in managed mode, you simply specify the table, the column to embed, and which model to use from the model serving stack—whether that’s a foundation model provided for you or one you’ve deployed yourself. From there, the system automatically generates embeddings with that model and stores them in the index. When you later issue a query, either through REST API or a Python client, you just provide the text. The system uses the same model to embed the query, ensuring that both the source data and the queries are encoded consistently. This way, you avoid problems like offline–online skew, since the same embedding model is always used end to end without you having to manage that process manually.

---

## Slide 4
**Title:** How does Vector Search Work?  
**Subtitle:** Method 2: Delta Sync API with self-managed embeddings

**Content:**
**Features:**
*   automatic sync
*   self-managed embeddings

*(Visual: Diagram showing Source Delta Table (with vector column) -> Auto Sync -> Indexer -> Vector DB -> Query Engine -> REST API/Python SDK)*
*   **Source Delta Table:** id, vector, col1, col2
*   **Mosaic AI Vector Search Engine:** Indexer, Vector DB, Query Engine
*   **Note:** Store any data, Query as vector

**Speaker Notes:**
The second option, which is the one being shown in the demo, is called ‘bring your own embedding’. In this approach, you calculate the embeddings yourself using any model you prefer—whether that’s through a foundation model API or one you’ve built and deployed. Once you’ve generated the vectors and stored them in the Delta table, you simply create the index and specify that you’re supplying your own embeddings. From there, the system ensures that the index stays in sync with the source table, just like with the fully managed option. That means if new data is appended, the index is quickly refreshed, and if there are larger updates or overrides—such as modified columns or recalculated embeddings—the index is rebuilt accordingly, which may take longer but remains fully automatic. The key point is this built-in automatic syncing through the Delta sync API, which guarantees that the rows, their associated text, and the corresponding vector indexes are always kept up to date without any manual intervention.

---

## Slide 5
**Title:** How does Vector Search Work?  
**Subtitle:** Method 3: Direct access CRUD API

**Content:**
**Features:** manual sync via API, with self-managed embeddings

*(Visual: Diagram showing Mosaic AI Vector Search Engine (Vector DB, Indexer, Query Engine, Direct Vector API) <-> REST API/Python SDK)*
*   Code snippet showing `vsc.similarity_search(...)` and `vsc.upsert(...)`

**Speaker Notes:**
In terms of access, there’s also support for a full CRUD API. This means that if you’ve already created your table but later want to insert, update, or upsert a specific record, you can do it directly. For example, you might perform an upsert on the row where the primary key ID equals five, updating either the vector values or any additional column tied to that entry. While this isn't something you'll need to do often, it becomes useful if you identify a few embeddings that are incorrect or outdated. Instead of rebuilding the whole index, you can target those specific records and update their indexes or related information directly through the CRUD API.

---

## Slide 6
**Title:** Set up Vector Search
**Subtitle:** Key concepts/components for Vector Search

**Content:**

**1. Create a Vector Search Endpoint**
*   This is the **compute resource** associated with vector search.
*   Endpoints scale automatically to support the size of the index or the number of concurrent requests.
*   Support for multiple compute types.

**2. Create a Model Serving Endpoint**
*   Create if you choose to have Databricks compute the embeddings.
*   Model Serving supports embeddings via **Foundation Models APIs** (e.g., BGE), **external models** (e.g., OpenAI's ada-002), and **custom models**.

**3. Create a Vector Search Index**
*   Created and **auto-synced** from a Delta table.
*   Optimized to provide real-time approximate nearest neighbor searches.
*   Indexes appear in and are **governed by Unity Catalog**.
*   Index level ACLs.

**Speaker Notes:**
Setting it up in the platform is essentially a three-step process. The first step is to create a vector search endpoint, which acts as the compute resource that powers the system. If you're using managed embeddings or want to rely on an embedding model deployed in Databricks model serving endpoints, this needs to be set up ahead of time. That way, when you create the index, you can either pre-calculate the embeddings using that endpoint or instruct the index to use the same model from that endpoint for generating embeddings on the source data. The same applies to any incoming query, which will also use that endpoint for consistency. So overall, the setup process will depend on whether you're using managed embeddings, bringing your own embeddings, or self-managing, but it always begins with creating and configuring a vector search endpoint as the foundation.

---

## Slide 7
**Title:** Set up Vector Search
**Subtitle:** UI Overview

**Content:**
*(Visual: Multiple screenshots showing the Databricks UI for setting up Vector Search)*

**Screenshots include:**
1.  **Catalog Explorer** - Browsing tables and selecting "Create vector search index" option
2.  **Compute section** - Showing Vector Search endpoints with status (Ready), name, type (Standard), indexes count, and creator
3.  **Create vector search index dialog** - Form with fields for:
    *   Name
    *   Primary key
    *   Endpoint selection
    *   Embedding source (Compute embeddings / Use existing embedding column)
    *   Embedding source column
    *   Embedding model selection
    *   Sync mode (Triggered / Continuous)
4.  **Serving endpoints** - Showing Foundation Model APIs including:
    *   DBRX Instruct (Preview)
    *   Meta Llama 3 70B Instruct (Preview)
    *   Query and URL options
    *   Endpoints list with state, served entities, tags, task, creator, and last modified info

**Speaker Notes:**
Here is an overview of setting up a vector search.

---
