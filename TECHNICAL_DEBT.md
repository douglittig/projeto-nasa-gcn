# Technical Debt & Improvements

## Prioritization Matrix (Criticality vs. Complexity)

| ID | Item | Criticality | Complexity | Impact | Sprint |
|:--:|:-----|:-----------:|:----------:|:-------|:------:|
| **1** | **Binary Parser Duplication** | 🔴 High | 🟠 Medium | Maintenance burden, consistency risk | 3 |
| **2** | **Failing Test** | 🔴 High | 🟢 Low | CI broken, test reliability | 1 |
| **3** | **Test Coverage** | 🟠 Medium | 🔴 High | Regression risk, no DLT/config tests | 2 |
| **4** | **Generic Error Handling** | 🟠 Medium | 🟡 Medium | Silent failures, debugging difficulty | 2 |
| **5** | **CI/CD Implementation** | 🟠 Medium | 🟡 Medium | Manual process, human error | 3 |
| **6** | **Vector Store Integration** | 🟠 Medium | 🔴 High | RAG scalability bottleneck | Backlog |
| **7** | **Streaming Configuration** | 🟠 Medium | 🟡 Medium | Data loss risk, no checkpoints | 3 |
| **8** | **Hardcoded Values** | 🟡 Low | 🟢 Low | Testing/staging difficulty | 2 |
| **9** | **Performance - Count Queries** | 🟡 Low | 🟢 Low | Slow on large tables (3M+ rows) | 1 |
| **10** | **Linting/MyPy Errors** | 🟡 Low | 🟢 Low | Code quality, type safety | 1 |
| **11** | **Dependency Version Bounds** | 🟡 Low | 🟢 Low | Breaking changes risk | 1 |
| **12** | **DLT Table Boilerplate** | 🟡 Low | 🟡 Medium | Code duplication, maintenance | Backlog |
| **13** | **Documentation Auto-gen** | 🟡 Low | 🟡 Medium | Manual maintenance overhead | Backlog |

---

## Sprint Planning

### 🏃 Sprint 1: Quick Wins (1 week)
Focus: Low-hanging fruit, immediate impact

- **#2** - Fix failing test (test_get_logger)
- **#10** - Fix linting/mypy errors
- **#9** - Optimize count queries
- **#11** - Add dependency upper bounds

### 🏃 Sprint 2: Quality & Reliability (2 weeks)
Focus: Testing and error handling

- **#3** - Increase test coverage (DLT pipeline, config)
- **#4** - Improve error handling
- **#8** - Make hardcoded values configurable

### 🏃 Sprint 3: Architecture & DevOps (3 weeks)
Focus: Structural improvements

- **#1** - Resolve binary parser duplication
- **#5** - Implement CI/CD
- **#7** - Configure secure streaming

### 📦 Backlog: Future Improvements
- **#6** - Vector Store production migration
- **#12** - Refactor DLT boilerplate
- **#13** - Documentation auto-generation

---

## Pending Items (Details)

### 1. Binary Parser Duplication 🔴
- **Issue**: Binary parser logic duplicated in `binary_parser.py` and `dlt_pipeline.py`
  - `binary_parser.py:203-374` (original)
  - `dlt_pipeline.py:102-167` (copy)
  - `PACKET_TYPE_NAMES` dict (196 entries) duplicated
- **Root Cause**: Databricks serverless environment has package distribution limitations
- **Impact**:
  - Bug fixes must be applied in two places
  - Risk of inconsistency
  - ~300 lines of duplicated code
- **Solution Options**:
  - **Option A (Current)**: Keep duplication, accept maintenance burden
  - **Option B**: Build-time code injection script
  - **Option C**: Spark UDF with `.addPyFile()` (may not work in serverless)
- **Recommendation**: Implement build-time injection (Option B)
  - Create `scripts/build_dlt.py` that injects parser code
  - Run before deploy: `python scripts/build_dlt.py && databricks bundle deploy`
  - Maintains single source of truth
- **Effort**: 4-6 hours

### 2. Failing Test 🔴
- **Issue**: `tests/main_test.py::test_get_logger` fails
- **Location**: `tests/main_test.py:test_get_logger`
- **Error**: `assert len(logger.handlers) >= 1` fails (len is 0)
- **Root Cause**: `get_logger()` sets level but doesn't add handler
- **Impact**: CI broken, undermines test confidence
- **Solution**: Either add StreamHandler in `get_logger()` or adjust test expectation
- **Effort**: 15 minutes

### 3. Test Coverage 🟠
- **Issue**: Insufficient test coverage (~7.3%)
  - Zero tests for `dlt_pipeline.py` (13 KB, complex logic)
  - Zero tests for `config.py` (3.6 KB, credential logic)
  - Only utility functions tested in `main.py`
- **Impact**: High regression risk, especially in DLT pipeline
- **Solution**:
  - Add DLT pipeline tests with Spark mocks
  - Add config tests with environment variable mocking
  - Test main functions (get_pipeline_stats, get_dlt_metrics)
- **Target Coverage**: >60%
- **Effort**: 2-3 days

### 4. Generic Error Handling 🟠
- **Issue**: Multiple instances of overly broad exception handling
  - `config.py:45-46`: `except Exception: pass` (swallows all errors)
  - `main.py:136-137`: Generic exception stored as string
  - `binary_parser.py:369-372`: Catches all exceptions
- **Impact**: Silent failures, difficult debugging
- **Solution**:
  - Use specific exception types
  - Add proper logging at minimum
  - Consider Result/Option patterns for parser
- **Examples**:
  ```python
  # Bad
  try:
      result = risky_operation()
  except Exception:
      pass

  # Good
  try:
      result = risky_operation()
  except ConnectionError as e:
      logger.error(f"Connection failed: {e}")
      raise
  except ValueError as e:
      logger.warning(f"Invalid value: {e}")
      return default_value
  ```
- **Effort**: 4-6 hours

### 5. CI/CD Implementation 🟠
- **Issue**: Deployment is manual via `deploy.sh`
- **Impact**: Human error risk, no automated testing on PR
- **Solution**: GitHub Actions workflow
  ```yaml
  # .github/workflows/ci.yml
  - Run tests (pytest)
  - Run linting (ruff)
  - Run type checking (mypy)
  - Deploy to dev on PR merge
  - Deploy to prod on main merge
  ```
- **Effort**: 1 day

### 6. Production Vector Store Integration 🟠
- **Issue**: RAG uses basic Delta Table (`gcn_embeddings`)
- **Impact**: Scalability bottleneck, manual index management
- **Solution**: Migrate to Databricks Vector Search
  - Managed indexing
  - Low-latency retrieval
  - Auto-scaling
- **Effort**: 1-2 weeks
- **Note**: Requires paid Databricks workspace

### 7. Streaming Configuration 🟠
- **Issue**: `failOnDataLoss: "false"` in `dlt_pipeline.py:108`
- **Impact**: Accepts data loss silently
- **Solution**:
  - Enable checkpoints for exactly-once semantics
  - Set `failOnDataLoss: "true"`
  - Use `startingOffsets: "latest"` for new runs
- **Effort**: 2-3 hours

### 8. Hardcoded Values 🟡
- **Issue**: Configuration values hardcoded in `config.py`
  - Kafka broker: `kafka.gcn.nasa.gov:9092`
  - OAuth endpoint: `https://auth.gcn.nasa.gov/oauth2/token`
  - Topic patterns: Lines 71-78
- **Impact**: Difficult to test, can't use staging/mock servers
- **Solution**: Move to configuration variables
  ```python
  KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER", "kafka.gcn.nasa.gov:9092")
  ```
- **Effort**: 1-2 hours

### 9. Performance - Count Queries 🟡
- **Issue**: `main.py:134` uses `.count()` which scans entire table
- **Impact**: Slow for large tables (3M+ rows in gcn_raw)
- **Solution**: Use `DESCRIBE EXTENDED` for metadata or query history
  ```python
  # Instead of:
  count = spark.table(full_name).count()

  # Use:
  stats = spark.sql(f"DESCRIBE EXTENDED {full_name}").collect()
  # Or use DLT event log for row counts
  ```
- **Effort**: 30 minutes

### 10. Linting/MyPy Errors 🟡
- **Issue**: Outstanding linting errors
  - `dlt_pipeline.py:195`: `spark` undefined (mypy F821)
  - `dlt_pipeline.py:69`: Line length > 100 chars
  - `utils.py:6`: Unused `sys` import
- **Solution**: Fix all errors, configure pre-commit hooks
- **Effort**: 30 minutes

### 11. Dependency Version Bounds 🟡
- **Issue**: Dependencies without upper bounds
  - `python-dotenv>=1.0.0` (no upper bound)
  - `mypy`, `ruff` unpinned
- **Impact**: Breaking changes in future versions
- **Solution**: Use `~=` operator
  ```toml
  python-dotenv = "~=1.0"  # >=1.0, <2.0
  ```
- **Effort**: 15 minutes

### 12. DLT Table Boilerplate 🟡
- **Issue**: 7 nearly identical table definitions (`dlt_pipeline.py:192-319`)
- **Pattern**: read → filter → decode → select
- **Solution**: Factory function or parametrization
  ```python
  def create_topic_table(topic_name: str, filter_pattern: str):
      @dlt.table(name=f"gcn_{topic_name}")
      def table():
          return (
              dlt.read_stream("gcn_raw")
              .filter(F.col("topic").rlike(filter_pattern))
              .select(...)
          )
      return table
  ```
- **Effort**: 2-3 hours

### 13. Documentation Auto-generation 🟡
- **Issue**: Docs manually written in `docs/*.md`
- **Solution**: Auto-generate from DLT metadata
  - Schema documentation from table metadata
  - Data lineage from DLT DAG
- **Effort**: 1 week
- **Tools**: Consider `dbt docs`, custom scripts

---

## Resolved Items (✅ Completed)

### Base64 Credentials Encoding (2026-01-30)
- **Action**: Implemented Base64 encoding for NASA GCN credentials to provide basic obfuscation in Databricks Community Edition.
- **Changes**:
  - Added `_decode_base64_credential()` function in `config.py`
  - Updated `deploy.sh` to auto-detect and decode Base64 credentials
  - Created helper script `scripts/encode_credentials.py`
  - Added test suite `scripts/test_base64_credentials.py`
  - Comprehensive security documentation in README
- **Status**: ✅ Implemented & Tested

### Type Hinting Coverage
- **Action**: Completed type annotations in `main.py` and `utils.py`. Added `mypy` to dev dependencies and configured it in `pyproject.toml` to ensure strict type checking.
- **Status**: ✅ Implemented

### Dynamic Configuration in `main.py`
- **Action**: Updated `databricks.yml` to define `catalog` and `schema` variables. Configured `nasa_gcn.job.yml` and `nasa_gcn.pipeline.yml` to use these variables. Refactored `src/nasa_gcn/main.py` to accept `--catalog` and `--schema` via command line arguments using `argparse`.
- **Status**: ✅ Implemented

### Observability & Logging
- **Action**: Implemented a central logging utility in `src/nasa_gcn/utils.py`. Replaced `print()` and `warnings.warn()` with structured logging (`logger.error`, `logger.warning`, `logger.info`) in `main.py` and `config.py`.
- **Status**: ✅ Implemented

### DLT Pipeline Refactoring (DRY & Data Integrity)
- **Action**: Refactored `src/nasa_gcn/dlt_pipeline.py` to import and use modularized logic from `binary_parser.py`, `utils.py`, `schemas.py`, and `config.py`. Eliminated code duplication and ensured the production pipeline uses the full binary parser.
- **Note**: Binary parser still duplicated due to serverless limitations (see #1 above)
- **Status**: ✅ Implemented (with known limitation)

### Convert DLT Pipeline to Python File
- **Action**: Converted `src/pipeline.ipynb` to `src/nasa_gcn/dlt_pipeline.py`. Updated `resources/nasa_gcn.pipeline.yml` to point to the new Python file. Used `ruff` to ensure code quality.
- **Status**: ✅ Implemented

### Code Quality & Linting
- **Action**: Added `ruff` to `dev` dependencies in `pyproject.toml` and configured line length (100) and target version (py310). Fixed existing linting errors in `src/nasa_gcn` and `tests`.
- **Note**: Some errors remain (see #10 above)
- **Status**: ✅ Mostly Implemented

### Refactor `pipeline.ipynb` into Modules
- **Action**: Created `src/nasa_gcn` package with `utils.py`, `schemas.py`, and `binary_parser.py`.
- **Status**: ✅ Implemented

### Redundant Logic
- **Action**: Created `decode_utf8` and `clean_json_id` utility functions logic.
- **Status**: ✅ Implemented

### Hardcoded Schemas
- **Action**: Centralized schemas in `src/nasa_gcn/schemas.py`.
- **Status**: ✅ Implemented

### Advanced Enrichment (Gold Layer)
- **Action**: Created `gcn_events_summarized` table joining Notices and Circulars.
- **Status**: ✅ Implemented

---

## Metrics

**Current State:**
- Total Code: ~1,378 lines Python
- Test Coverage: ~7.3%
- Tests: 19 total (18 passing, 1 failing)
- Pending Items: 13
- Critical Items: 2
- Sprint 1 Items: 4 (estimated 1 week)

**Target State (Post Sprint 3):**
- Test Coverage: >60%
- All Tests: Passing
- Critical Items: 0
- CI/CD: Automated
- Code Quality: All linting passing

---

**Last Updated**: 2026-01-30
**Next Review**: After Sprint 1 completion
