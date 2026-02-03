# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NASA GCN (Gamma-ray Coordinates Network) Data Pipeline using Databricks Asset Bundles and Delta Live Tables. Ingests real-time astronomical alerts from NASA's Kafka stream through a medallion architecture (Bronze -> Silver -> Gold).

**Stack:** Databricks Asset Bundles, Delta Live Tables (DLT), PySpark, NASA GCN Kafka, `uv` package manager.

## Common Commands

```bash
# Install dependencies
uv sync --dev

# Run all tests
pytest

# Run single test
pytest tests/test_utils.py::test_decode_utf8 -v

# Run tests with coverage
pytest --cov=nasa_gcn --cov-report=term-missing

# Lint and fix
ruff check src/ tests/ --fix

# Format code
ruff format src/ tests/

# Type checking
mypy src/

# Validate bundle configuration
databricks bundle validate

# Deploy and run (loads credentials from .env automatically)
./deploy.sh run

# Deploy only
./deploy.sh

# Run job without deploying
./deploy.sh run-only

# Deploy to production
TARGET=prod ./deploy.sh run
```

## Architecture

```
NASA GCN Kafka Stream
        |
        v
+------------------+
|   Bronze Layer   |  gcn_raw (all raw messages)
+--------+---------+
         |
         v
+------------------+
|   Silver Layer   |  7 topic-specific tables:
|                  |  gcn_classic_text, gcn_classic_voevent,
|                  |  gcn_classic_binary, gcn_notices,
|                  |  gcn_circulars, igwn_gwalert, gcn_heartbeat
+--------+---------+
         |
         v
+------------------+
|    Gold Layer    |  gcn_events_summarized (enriched events)
+------------------+
```

## Critical Constraints

### Binary Parser Duplication (IMPORTANT)

`dlt_pipeline.py` contains **duplicated binary parser logic** (lines 56-167) that must stay in sync with `binary_parser.py`.

**Why:** Databricks serverless DLT cannot reliably import custom modules on Spark executors. The parser must be inlined.

**When modifying binary parser:**
1. Update `binary_parser.py` (source of truth)
2. Manually sync changes to `dlt_pipeline.py:56-167`
3. Keep `PACKET_TYPE_NAMES` dict in sync

### DLT-Specific Gotchas

- `spark` is a **global variable** in DLT context - it's not imported, but available at runtime
- UDFs in DLT cannot import from sibling modules on executors - all code must be inlined in the UDF file
- `dlt.read_stream()` reads from other DLT tables, `spark.readStream` reads external sources

### Credentials Management

Databricks Community Edition does **not** support Secrets API. Credentials are stored in `.env` (gitignored):

```bash
# Preferred: Base64-encoded
GCN_CLIENT_ID_B64=...
GCN_CLIENT_SECRET_B64=...

# Fallback: Plain-text
GCN_CLIENT_ID=...
GCN_CLIENT_SECRET=...
```

Use `python scripts/encode_credentials.py` to encode credentials. `deploy.sh` auto-detects and decodes Base64.

### Unity Catalog Schema

- Catalog: `sandbox`
- Schema: `nasa_gcn_${bundle.target}` (e.g., `nasa_gcn_dev`, `nasa_gcn_prod`)

## Development Workflow

### Adding New GCN Topic

1. Add schema in `src/nasa_gcn/schemas.py`
2. Add `@dlt.table` definition in `src/nasa_gcn/dlt_pipeline.py`
3. Update `TABLES_TO_CHECK` in `main.py` if needed

### Known Issues

- **Failing test:** `tests/main_test.py::test_get_logger` - logger handler assertion fails
- **Slow counts:** `main.py` uses `.count()` on large tables (3M+ rows) - consider DLT event log
- **Generic exceptions:** `config.py:45-46` and `binary_parser.py:369-372` swallow errors silently

See `TECHNICAL_DEBT.md` for full issue tracking and sprint planning.
