# Technical Debt & Improvements

## Prioritization Matrix (Criticality vs. Complexity)

| ID | Item | Criticality | Complexity | Impact |
|:--:|:-----|:-----------:|:----------:|:-------|
| **2** | **Dynamic Configuration in `main.py`** | 🟠 **Medium** | 🟢 **Low** | Deployment risk. Hardcoded environment values. |
| **3** | **CI/CD Implementation** | 🟠 **Medium** | 🟡 **Medium** | Manual process prone to human error. |
| **4** | **Production Vector Store Integration** | 🟠 **Medium** | 🔴 **High** | Scalability bottleneck for RAG features. |
| **6** | **Documentation Auto-generation** | 🟡 **Low** | 🟡 **Medium** | Maintenance overhead. |
| **7** | **Type Hinting Coverage** | 🟡 **Low** | 🟢 **Low** | Reduced static analysis effectiveness. |

---

## Remaining Items

### 2. Dynamic Configuration in `main.py`
- **Issue**: `src/nasa_gcn/main.py` has hardcoded values for `CATALOG` ("sandbox") and `SCHEMA` ("nasa_gcn_dev").
- **Solution**: Update `main.py` to accept arguments or environment variables. Update `databricks.yml` to pass these dynamically.

### 3. CI/CD Implementation
- **Issue**: Deployment is manual via local scripts (`deploy.sh`).
- **Solution**: Create a GitHub Actions workflow (`.github/workflows/ci.yml`) to run tests (`pytest`), checks (`ruff`), and handle automated deployment to Databricks upon merge.

### 4. Production Vector Store Integration
- **Issue**: Current RAG uses a basic Delta Table (`gcn_embeddings`) and a prototype script.
- **Solution**: Migrate to **Databricks Vector Search** for managed indexing and low-latency retrieval.

### 6. Documentation Auto-generation
- **Issue**: Docs are manually written in `docs/*.md`.
- **Solution**: Explore tools to auto-generate schema documentation from the Delta Live Tables metadata.

### 7. Type Hinting Coverage
- **Issue**: Inconsistent type hints in `main.py` and `utils.py`.
- **Solution**: Complete type annotations to enable strict `mypy` validation.

---

## Resolved Items (✅ Completed)

### Observability & Logging
- **Action**: Implemented a central logging utility in `src/nasa_gcn/utils.py`. Replaced `print()` and `warnings.warn()` with structured logging (`logger.error`, `logger.warning`, `logger.info`) in `main.py` and `config.py`.
- **Status**: Implemented.

### DLT Pipeline Refactoring (DRY & Data Integrity)
- **Action**: Refactored `src/nasa_gcn/dlt_pipeline.py` to import and use modularized logic from `binary_parser.py`, `utils.py`, `schemas.py`, and `config.py`. Eliminated code duplication and ensured the production pipeline uses the full binary parser.
- **Status**: Implemented.

### Convert DLT Pipeline to Python File
- **Action**: Converted `src/pipeline.ipynb` to `src/nasa_gcn/dlt_pipeline.py`. Updated `resources/nasa_gcn.pipeline.yml` to point to the new Python file. Used `ruff` to ensure code quality.
- **Status**: Implemented.

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
