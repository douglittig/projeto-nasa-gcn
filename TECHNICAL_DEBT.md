# Technical Debt & Improvements

## Code Quality & Maintainability

### 1. Refactor `pipeline.ipynb` into Modules
- **Issue**: The notebook contains complex logic, schema definitions, and lookup tables (e.g., `PACKET_TYPE_NAMES` dict is very large).
- **Solution**: Move `PACKET_TYPE_NAMES`, helper functions (`clean_json_id`, `parse_gcn_binary_packet`), and schemas to a separate Python module (e.g., `src/utils.py` or `src/schema.py`) and import them. This improves readability and testability.

### 2. Redundant Logic
- **Issue**: `decode(col("value"), "UTF-8")` is repeated in every table definition.
- **Solution**: Create a shared Bronze-to-Silver transformer or a UDF that handles consistent decoding and basic metadata extraction.

### 3. Hardcoded Schemas
- **Issue**: `CIRCULAR_SCHEMA` and `PARSED_BINARY_SCHEMA` are defined as strings within the notebook cells.
- **Solution**: Centralize schema definitions in a config file or a dedicated schemas module.

## RAG Optimization

### 4. Vector Store Integration
- **Issue**: We are currently only preparing the text (`document_text`).
- **Solution**: Implement the Gold layer steps to generate embeddings (e.g., using Databricks Vector Search or OpenAI embeddings) and store them in a vector database.

### 5. Advanced Enrichment
- **Issue**: Tables are currently independent.
- **Solution**: Implement the "Gold Layer" strategy to join Notices (facts) with Circulars (narrative) based on Event ID or spatial/temporal matching, as researched.

## Documentation

### 6. Documentation Auto-generation
- **Issue**: Docs are manually written in `docs/*.md`.
- **Solution**: Explore tools to auto-generate schema documentation from the Delta Live Tables metadata.
