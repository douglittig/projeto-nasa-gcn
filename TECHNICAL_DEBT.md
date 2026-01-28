# Technical Debt & Improvements

## Remaining Items

### 1. Documentation Auto-generation
- **Issue**: Docs are manually written in `docs/*.md`.
- **Solution**: Explore tools to auto-generate schema documentation from the Delta Live Tables metadata.

### 2. Production Vector Store Integration
- **Issue**: The current RAG implementation uses a Delta Table (`gcn_embeddings`) and a prototype script.
- **Solution**: Migrate to **Databricks Vector Search** for low-latency retrieval and managed indexing.

### 3. Convert DLT Pipeline to Python File
- **Issue**: The DLT pipeline is defined in `src/pipeline.ipynb`. While helper logic was moved to modules, the pipeline entry point remains a notebook.
- **Impact**: harder to unit test the pipeline definition, harder to review in PRs.
- **Solution**: Convert `src/pipeline.ipynb` to `src/nasa_gcn/dlt_pipeline.py` and update `resources/nasa_gcn.pipeline.yml` to point to the file instead of the notebook.

### 4. Dynamic Configuration in `main.py`
- **Issue**: `src/nasa_gcn/main.py` has hardcoded values for `CATALOG` ("sandbox") and `SCHEMA` ("nasa_gcn_dev").
- **Impact**: Deploying to production requires manual code changes or risks writing to the wrong environment.
- **Solution**: Update `main.py` to accept arguments (e.g., via `argparse`) or read environment variables for these values, and update `databricks.yml` to pass them dynamically based on the target (dev/prod).

### 5. CI/CD Implementation
- **Issue**: Deployment is manual via local scripts (`deploy.sh`).
- **Solution**: Create a GitHub Actions workflow (`.github/workflows/ci.yml`) to run tests (`pytest`), checks (`ruff`), and handle automated deployment to Databricks upon merge.

## Resolved Items (✅ Completed)

### Code Quality & Linting
- **Action**: Added `ruff` to `dev` dependencies in `pyproject.toml` and configured line length (100) and target version (py310). Fixed existing linting errors in `src/nasa_gcn` and `tests`.
- **Status**: Implemented.

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
