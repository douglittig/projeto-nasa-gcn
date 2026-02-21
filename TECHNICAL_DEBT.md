# Technical Debt & Improvements

## Prioritization Matrix (Criticality vs. Complexity)

| ID | Item | Criticality | Complexity | Impact | Sprint |
|:--:|:-----|:-----------:|:----------:|:-------|:------:|
| **1** | **Binary Parser Duplication** | 🔴 High | 🟠 Medium | Maintenance burden, consistency risk | 3 |
| **2** | **Failing Test** | 🔴 High | 🟢 Low | CI broken, test reliability | 1 |
| **3** | **Test Coverage** | 🟠 Medium | 🔴 High | Regression risk, no SDP/config tests | 2 |
| **4** | **Generic Error Handling** | 🟠 Medium | 🟡 Medium | Silent failures, debugging difficulty | 2 |
| **5** | **CI/CD Implementation** | 🟠 Medium | 🟡 Medium | Manual process, human error | 3 |
| **6** | **Vector Store Integration** | 🟠 Medium | 🔴 High | RAG scalability bottleneck | Backlog |
| **7** | **Streaming Configuration** | 🟠 Medium | 🟡 Medium | Data loss risk, no checkpoints | 3 |
| **8** | **Hardcoded Values** | 🟡 Low | 🟢 Low | Testing/staging difficulty | 2 |
| **9** | **Performance - Count Queries** | 🟡 Low | 🟢 Low | Slow on large tables (3M+ rows) | 1 |
| **10** | **Dependency Version Bounds** | 🟡 Low | 🟢 Low | Breaking changes risk | 1 |
| **11** | **SDP Auto-Optimize** | 🟡 Low | 🟢 Low | Small files in Bronze | 1 |
| **12** | **Data Quality Expectations** | 🟠 Medium | 🟡 Medium | Silent bad data in Silver | 2 |
| **13** | **Documentation Auto-gen** | 🟡 Low | 🟡 Medium | Manual maintenance overhead | Backlog |

---

## Sprint Planning

### 🏃 Sprint 1: Quick Wins (1 week)
Focus: Low-hanging fruit, immediate impact

- **#2** - Fix failing test (test_get_logger)
- **#9** - Optimize count queries
- **#10** - Add dependency upper bounds
- **#11** - Add Auto-Optimize table properties to Bronze

### 🏃 Sprint 2: Quality & Reliability (2 weeks)
Focus: Testing and error handling

- **#3** - Increase test coverage (SDP pipelines, config)
- **#4** - Improve error handling
- **#8** - Make hardcoded values configurable
- **#12** - Add Data Quality Expectations to Silver tables

### 🏃 Sprint 3: Architecture & DevOps (3 weeks)
Focus: Structural improvements

- **#1** - Resolve binary parser duplication
- **#5** - Implement CI/CD
- **#7** - Configure secure streaming

### 📦 Backlog: Future Improvements
- **#6** - Vector Store production migration
- **#13** - Documentation auto-generation
- Change Data Feed for downstream CDC (when needed)
- CLUSTER BY AUTO for Gold layer (evaluate query patterns first)

---

## Pending Items (Details)

### 1. Binary Parser Duplication 🔴
- **Issue**: Binary parser logic duplicated in `binary_parser.py` and `silver_pipeline.py`
  - `binary_parser.py:203-374` (original, source of truth)
  - `silver_pipeline.py:61-196` (copy for UDF compatibility)
  - `PACKET_TYPE_NAMES` dict (196 entries) duplicated
- **Root Cause**: Databricks SDP serverless environment cannot import sibling modules in UDF executors
- **Impact**:
  - Bug fixes must be applied in two places
  - Risk of inconsistency
  - ~300 lines of duplicated code
- **Solution Options**:
  - **Option A (Current)**: Keep duplication, accept maintenance burden
  - **Option B**: Build-time code injection script
  - **Option C**: Spark UDF with `.addPyFile()` (may not work in serverless)
- **Recommendation**: Implement build-time injection (Option B)
  - Create `scripts/build_pipeline.py` that injects parser code
  - Run before deploy: `python scripts/build_pipeline.py && databricks bundle deploy`
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
  - Zero tests for SDP pipelines (`bronze_pipeline.py`, `silver_pipeline.py`, `gold_pipeline.py`)
  - Zero tests for `config.py` (credential logic)
  - Only utility functions tested in `main.py`
- **Impact**: High regression risk, especially in pipeline transformations
- **Solution**:
  - Add SDP pipeline tests with Spark mocks
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
- **Issue**: `failOnDataLoss: "false"` in Kafka config
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
- **Solution**: Use `DESCRIBE EXTENDED` for metadata or SDP event log
  ```python
  # Instead of:
  count = spark.table(full_name).count()

  # Use:
  stats = spark.sql(f"DESCRIBE EXTENDED {full_name}").collect()
  # Or use SDP event log for row counts
  ```
- **Effort**: 30 minutes

### 10. Dependency Version Bounds 🟡
- **Issue**: Dependencies without upper bounds
  - `python-dotenv>=1.0.0` (no upper bound)
  - `mypy`, `ruff` unpinned
- **Impact**: Breaking changes in future versions
- **Solution**: Use `~=` operator
  ```toml
  python-dotenv = "~=1.0"  # >=1.0, <2.0
  ```
- **Effort**: 15 minutes

### 11. SDP Auto-Optimize (Bronze) 🟡 [NEW]
- **Issue**: Bronze pipeline lacks `delta.autoOptimize` table properties
- **Location**: `bronze_pipeline.py:48-52`
- **Impact**: Small files accumulation with high-frequency Kafka ingestion
- **Solution**: Add table properties
  ```python
  @dp.table(
      name="gcn_raw",
      cluster_by=["topic", "kafka_timestamp"],
      table_properties={
          "delta.autoOptimize.optimizeWrite": "true",
          "delta.autoOptimize.autoCompact": "true",
      },
  )
  ```
- **Benefit**: Reduces small files automatically, improves read performance
- **Effort**: 15 minutes

### 12. Data Quality Expectations (Silver) 🟠 [NEW]
- **Issue**: Silver tables have no data quality validation
- **Location**: `silver_pipeline.py` (all 7 tables)
- **Impact**: Bad data flows through pipeline silently
- **Solution**: Add `@dp.expect_or_drop` decorators
  ```python
  @dp.table(name="gcn_circulars", cluster_by=["event_id", "created_on"])
  @dp.expect_or_drop("valid_circular_id", "circular_id IS NOT NULL")
  @dp.expect_or_drop("valid_event_id", "event_id IS NOT NULL")
  def circulars():
      ...
  ```
- **Tables to add expectations**:
  - `gcn_circulars` - validate `circular_id`, `event_id`
  - `gcn_notices` - validate `notice_id`
  - `gcn_classic_binary` - validate `parse_error IS NULL`
  - `gcn_gwalert` - validate `event_id`
- **Effort**: 1-2 hours

### 13. Documentation Auto-generation 🟡
- **Issue**: Docs manually written in `docs/*.md`
- **Solution**: Auto-generate from SDP metadata
  - Schema documentation from table metadata
  - Data lineage from SDP DAG
- **Effort**: 1 week
- **Tools**: Consider custom scripts, SDP event log

---

## Resolved Items (✅ Completed)

### DLT to SDP Migration (2026-02-21)
- **Action**: Migrated all pipelines from Delta Live Tables (DLT) to Spark Declarative Pipelines (SDP)
- **Changes**:
  - Changed `import dlt` to `from pyspark import pipelines as dp`
  - Updated decorators from `@dlt.table` to `@dp.table` and `@dp.materialized_view`
  - Changed `dlt.read_stream()` to `spark.readStream.table()`
  - Added Liquid Clustering (`cluster_by`) to all tables
  - Added `per-file-ignores` in `pyproject.toml` for `spark` global variable
  - Removed legacy `dlt_pipeline.py` (341-line monolithic file)
- **Files Modified**:
  - `bronze_pipeline.py` - Kafka ingestion
  - `silver_pipeline.py` - Topic parsing (7 tables)
  - `gold_pipeline.py` - Aggregations (2 materialized views)
  - `pyproject.toml` - Ruff configuration
- **Status**: ✅ Implemented & Deployed

### Linting/MyPy Errors Fixed (2026-02-21)
- **Action**: Fixed F821 errors for `spark` undefined variable
- **Solution**: Added per-file-ignores in pyproject.toml for pipeline files
- **Status**: ✅ Implemented

### DLT Table Boilerplate Eliminated (2026-02-21)
- **Action**: Removed monolithic `dlt_pipeline.py` during SDP migration
- **Note**: Each layer now has its own focused pipeline file
- **Status**: ✅ Resolved by architecture change

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
- **Action**: Updated `databricks.yml` to define `catalog` and `schema` variables. Configured `nasa_gcn.job.yml` and pipeline configs to use these variables. Refactored `src/nasa_gcn/main.py` to accept `--catalog` and `--schema` via command line arguments using `argparse`.
- **Status**: ✅ Implemented

### Observability & Logging
- **Action**: Implemented a central logging utility in `src/nasa_gcn/utils.py`. Replaced `print()` and `warnings.warn()` with structured logging (`logger.error`, `logger.warning`, `logger.info`) in `main.py` and `config.py`.
- **Status**: ✅ Implemented

### SDP Pipeline Modularization (DRY & Data Integrity)
- **Action**: Refactored pipelines to use modularized logic from `binary_parser.py`, `utils.py`, `schemas.py`, and `config.py`. Eliminated code duplication where possible.
- **Note**: Binary parser still duplicated in `silver_pipeline.py` due to serverless UDF limitations (see #1 above)
- **Status**: ✅ Implemented (with known limitation)

### Convert DLT Pipeline to Python File
- **Action**: Converted `src/pipeline.ipynb` to Python files. Now structured as `bronze_pipeline.py`, `silver_pipeline.py`, `gold_pipeline.py`.
- **Status**: ✅ Implemented

### Code Quality & Linting
- **Action**: Added `ruff` to `dev` dependencies in `pyproject.toml` and configured line length (100) and target version (py310). Fixed existing linting errors in `src/nasa_gcn` and `tests`.
- **Status**: ✅ Implemented

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
- **Action**: Created `gcn_events_summary` and `gcn_daily_stats` materialized views joining Silver tables.
- **Status**: ✅ Implemented

---

## Metrics

**Current State:**
- Total Code: ~1,500 lines Python (3 pipeline files)
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
- Data Quality: Expectations on all Silver tables

---

**Last Updated**: 2026-02-21
**Next Review**: After Sprint 1 completion
