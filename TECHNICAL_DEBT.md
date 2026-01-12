# Technical Debt & Improvements

## Remaining Items

### 1. Documentation Auto-generation
- **Issue**: Docs are manually written in `docs/*.md`.
- **Solution**: Explore tools to auto-generate schema documentation from the Delta Live Tables metadata.

### 2. Production Vector Store Integration
- **Issue**: The current RAG implementation uses a Delta Table (`gcn_embeddings`) and a prototype script.
- **Solution**: Migrate to **Databricks Vector Search** for low-latency retrieval and managed indexing.

## Resolved Items (✅ Completed)

### Refactor `pipeline.ipynb` into Modules
- **Action**: Created `src/nasa_gcn` package with `utils.py`, `schemas.py`, and `binary_parser.py`.
- **Status**: Implemented.

### Redundant Logic
- **Action**: Created `decode_utf8` and `clean_json_id` utility functions logic.
- **Status**: Implemented.

### Hardcoded Schemas
- **Action**: Centralized schemas in `src/nasa_gcn/schemas.py`.
- **Status**: Implemented.

### Advanced Enrichment (Gold Layer)
- **Action**: Created `gcn_events_summarized` table joining Notices and Circulars.
- **Status**: Implemented.
