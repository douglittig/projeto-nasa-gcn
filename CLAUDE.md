# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NASA GCN (Gamma-ray Coordinates Network) Data Pipeline using Databricks Asset Bundles and Delta Live Tables. The project ingests real-time astronomical alerts from NASA's Kafka stream and processes them through a medallion architecture (Bronze → Silver → Gold).

**Key Technologies:**
- Databricks Asset Bundles (DAB) for infrastructure-as-code
- Delta Live Tables (DLT) for declarative data pipelines
- PySpark for distributed data processing
- NASA GCN Kafka for streaming astronomical alerts
- `uv` for Python package management

## Common Commands

### Development Setup
```bash
# Install dependencies
uv sync --dev

# Encode NASA GCN credentials (recommended)
python scripts/encode_credentials.py
# Then add output to .env file

# Validate bundle configuration
databricks bundle validate
```

### Testing & Quality
```bash
# Run tests
pytest

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Deployment
```bash
# Deploy only
./deploy.sh

# Deploy + run job
./deploy.sh run

# Run job without deploying
./deploy.sh run-only

# Deploy to production
TARGET=prod ./deploy.sh run
```

### Manual Deployment (Alternative)
```bash
# Load credentials and deploy manually
source .env
export BUNDLE_VAR_gcn_client_id=$(echo $GCN_CLIENT_ID_B64 | base64 -d)
export BUNDLE_VAR_gcn_client_secret=$(echo $GCN_CLIENT_SECRET_B64 | base64 -d)
databricks bundle deploy -t dev
databricks bundle run nasa_gcn_job
```

## Architecture

### Medallion Data Flow
```
NASA GCN Kafka Stream
        ↓
┌─────────────────┐
│  Bronze Layer   │  gcn_raw (all raw messages)
└────────┬────────┘
         ↓
┌─────────────────┐
│  Silver Layer   │  7 topic-specific tables:
│                 │  - gcn_classic_text
│                 │  - gcn_classic_voevent
│                 │  - gcn_classic_binary
│                 │  - gcn_notices
│                 │  - gcn_circulars
│                 │  - igwn_gwalert
│                 │  - gcn_heartbeat
└────────┬────────┘
         ↓
┌─────────────────┐
│   Gold Layer    │  gcn_events_summarized (enriched events)
└─────────────────┘
```

### Code Organization
```
src/nasa_gcn/
├── config.py          # Kafka configuration & credentials (supports Base64 decoding)
├── schemas.py         # PySpark schemas for all data types
├── utils.py           # Shared utilities (decode_utf8, clean_json_id, logging)
├── binary_parser.py   # Binary GCN packet parser (original)
├── dlt_pipeline.py    # Delta Live Tables pipeline definition
└── main.py            # Job orchestration & metrics reporting

resources/
├── nasa_gcn.job.yml      # Databricks Job definition
└── nasa_gcn.pipeline.yml # DLT Pipeline configuration

scripts/
└── encode_credentials.py # Helper to Base64-encode credentials
```

### Module Imports in DLT Pipeline

**Critical Architecture Detail:** `dlt_pipeline.py` contains **duplicated binary parser logic** embedded directly in the file (lines 56-167). This is a known architectural constraint documented in TECHNICAL_DEBT.md #1.

**Why:** Databricks serverless DLT pipelines cannot reliably import custom modules on Spark executors. The binary parser must be inlined in `dlt_pipeline.py` to work in UDFs.

**Implication:** When modifying binary parser logic:
1. Update `binary_parser.py` (source of truth)
2. Manually sync changes to `dlt_pipeline.py` lines 56-167
3. Keep `PACKET_TYPE_NAMES` dict (196 entries) in sync

## Critical Constraints

### 1. Binary Parser Duplication
- `binary_parser.py` (original, for testing/local use)
- `dlt_pipeline.py:56-167` (duplicated for DLT UDF compatibility)
- **Always update both files** when changing parser logic
- Future solution: Build-time code injection (see TECHNICAL_DEBT.md)

### 2. Credentials Management
- Databricks Community Edition **does not support** Databricks Secrets API
- Credentials stored in `.env` file (gitignored)
- **Preferred:** Base64-encoded (`GCN_CLIENT_ID_B64`, `GCN_CLIENT_SECRET_B64`)
- **Fallback:** Plain-text (`GCN_CLIENT_ID`, `GCN_CLIENT_SECRET`)
- `deploy.sh` auto-detects and decodes Base64 credentials
- `config.py:_decode_base64_credential()` handles decoding in pipeline

### 3. Test Coverage Limitation
- Current test coverage: ~7.3% (target: >60%)
- **No tests exist for:**
  - `dlt_pipeline.py` (main pipeline logic)
  - `config.py` (credential handling)
- **Known failing test:** `tests/main_test.py::test_get_logger`
- See TECHNICAL_DEBT.md Sprint 1-2 for testing roadmap

### 4. Unity Catalog Schema
- Default catalog: `sandbox`
- Schema naming: `nasa_gcn_${bundle.target}` (e.g., `nasa_gcn_dev`, `nasa_gcn_prod`)
- Configurable via `databricks.yml` variables

## Development Workflow

### Making Code Changes

1. **Local Changes:**
   - Edit code in `src/nasa_gcn/`
   - If modifying binary parser: update **both** `binary_parser.py` AND `dlt_pipeline.py`

2. **Testing:**
   ```bash
   pytest                    # Run tests
   ruff check src/ tests/   # Lint
   mypy src/                # Type check
   ```

3. **Deploy to Dev:**
   ```bash
   ./deploy.sh run          # Deploy + execute job
   ```

4. **Check Results:**
   - Job output shows Bronze/Silver/Gold table row counts
   - Check Databricks UI: Jobs → nasa_gcn_job → Runs

### Adding New GCN Topic

1. Add schema in `src/nasa_gcn/schemas.py`
2. Add table definition in `src/nasa_gcn/dlt_pipeline.py` (lines 192-319 for examples)
3. Update `main.py` TABLES_TO_CHECK if needed
4. Add documentation in `docs/`

## Known Issues & Workarounds

### Issue: Binary Parser Import Fails in DLT
**Symptom:** `ModuleNotFoundError: No module named 'nasa_gcn'` on Spark executors
**Workaround:** Binary parser logic is inlined in `dlt_pipeline.py`
**Permanent Fix:** Planned build-time code injection (TECHNICAL_DEBT.md #1)

### Issue: Count Queries Slow on Large Tables
**Symptom:** `main.py` takes minutes to count rows in `gcn_raw` (3M+ rows)
**Workaround:** Uses full table scan `.count()`
**Better Solution:** Query DLT event log for metrics (TECHNICAL_DEBT.md #9)

### Issue: Generic Error Handling
**Symptom:** Silent failures in `config.py:45-46`, `binary_parser.py:369-372`
**Impact:** Errors swallowed by `except Exception: pass`
**Mitigation:** Check logs carefully; planned refactor in Sprint 2 (TECHNICAL_DEBT.md #4)

## Important Files

- **TECHNICAL_DEBT.md** - Comprehensive list of known issues, prioritized by Sprint
- **README.md** - Setup instructions and deployment guide
- **deploy.sh** - Production deployment script (handles Base64 credentials)
- **.env.example** - Template for credentials file
- **databricks.yml** - Bundle configuration (dev/prod targets)
- **pyproject.toml** - Python dependencies and tool configuration

## NASA GCN Data Sources

The pipeline processes 7 topic families from NASA GCN Kafka:
1. **gcn.classic.text** - Plain text alerts (legacy format)
2. **gcn.classic.voevent** - XML VOEvent format
3. **gcn.classic.binary** - Binary packets (parsed using duplicated parser)
4. **gcn.notices** - JSON notices (new format)
5. **gcn.circulars** - Astronomical circulars (human-authored reports)
6. **igwn.gwalert** - Gravitational wave alerts (LIGO/Virgo)
7. **gcn.heartbeat** - System health checks

Each has dedicated documentation in `docs/<TOPIC>_RAG.md` with RAG query examples.

## Databricks Asset Bundle Structure

- **Bundle Name:** `nasa_gcn`
- **Targets:** `dev` (default), `prod`
- **Resources:**
  - Job: `nasa_gcn_job` (orchestration)
  - Pipeline: `nasa_gcn_pipeline` (DLT streaming)
- **Artifacts:** Python wheel built via `uv build --wheel`
- **Sync:** Auto-syncs `src/`, `dist/*.whl` to workspace

## Next Steps (from TECHNICAL_DEBT.md)

**Sprint 1 (Quick Wins):**
- Fix failing test in `main_test.py`
- Resolve mypy/ruff linting errors
- Optimize count queries
- Pin dependency versions

**Sprint 2 (Quality):**
- Increase test coverage to >60%
- Improve error handling (remove generic `except Exception`)
- Make hardcoded values configurable

**Sprint 3 (Architecture):**
- Resolve binary parser duplication
- Implement CI/CD (GitHub Actions)
- Configure streaming checkpoints
