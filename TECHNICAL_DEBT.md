# Technical Debt & Improvements

## Prioritization Matrix (Criticality vs. Complexity)

| ID | Item | Criticality | Complexity | Impact |
|:--:|:-----|:-----------:|:----------:|:-------|
| **1** | **DLT Pipeline Refactoring (DRY & Data Integrity)** | 🔴 **High** | 🟡 **Medium** | **Critical Data Loss**. Pipeline uses inferior, duplicated code instead of tested modules. |
| **2** | **Dynamic Configuration in `main.py`** | 🟠 **Medium** | 🟢 **Low** | Deployment risk. Hardcoded environment values. |
| **3** | **CI/CD Implementation** | 🟠 **Medium** | 🟡 **Medium** | Manual process prone to human error. |
| **4** | **Production Vector Store Integration** | 🟠 **Medium** | 🔴 **High** | Scalability bottleneck for RAG features. |
| **5** | **Observability & Logging** | 🟠 **Medium** | 🟢 **Low** | Blind spots in production monitoring. |
| **6** | **Documentation Auto-generation** | 🟡 **Low** | 🟡 **Medium** | Maintenance overhead. |
| **7** | **Type Hinting Coverage** | 🟡 **Low** | 🟢 **Low** | Reduced static analysis effectiveness. |

---

## Remaining Items

### 1. DLT Pipeline Refactoring (DRY & Data Integrity)
- **Issue**: `src/nasa_gcn/dlt_pipeline.py` violates DRY by duplicating logic from `utils.py`, `schemas.py`, and `config.py`. Worse, it re-implements a simplified version of the binary parser, ignoring `binary_parser.py`.
- **Impact**:
    - **Data Loss**: Production pipeline extracts significantly fewer fields from binary packets than the available parser.
    - **False Security**: Tests pass for `binary_parser.py`, but that code isn't running in the pipeline.
    - **Maintenance Nightmare**: Fixes in utility modules don't propagate to the pipeline.
- **Solution**: Refactor `dlt_pipeline.py` to import and use the established modules (`binary_parser`, `utils`, `schemas`, `config`) instead of redefining them.

### 2. Dynamic Configuration in `main.py`
- **Issue**: `src/nasa_gcn/main.py` has hardcoded values for `CATALOG` ("sandbox") and `SCHEMA` ("nasa_gcn_dev").
- **Solution**: Update `main.py` to accept arguments or environment variables. Update `databricks.yml` to pass these dynamically.

### 3. CI/CD Implementation
- **Issue**: Deployment is manual via local scripts (`deploy.sh`).
- **Solution**: Create a GitHub Actions workflow (`.github/workflows/ci.yml`) to run tests (`pytest`), checks (`ruff`), and handle automated deployment to Databricks upon merge.

### 4. Production Vector Store Integration
- **Issue**: Current RAG uses a basic Delta Table (`gcn_embeddings`) and a prototype script.
- **Solution**: Migrate to **Databricks Vector Search** for managed indexing and low-latency retrieval.

### 5. Observability & Logging
- **Issue**: Code relies on `print()` and `warnings.warn()`.
- **Solution**: Implement the standard Python `logging` library with structured formatting to integrate with Databricks monitoring.

### 6. Documentation Auto-generation
- **Issue**: Docs are manually written in `docs/*.md`.
- **Solution**: Explore tools to auto-generate schema documentation from the Delta Live Tables metadata.

### 7. Type Hinting Coverage
- **Issue**: Inconsistent type hints in `main.py` and `utils.py`.
- **Solution**: Complete type annotations to enable strict `mypy` validation.

---

## Resolved Items (✅ Completed)

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