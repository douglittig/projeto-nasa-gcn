# NASA GCN Data Pipeline

## Project Overview

This project implements a data ingestion pipeline for the **NASA Gamma-ray Coordinates Network (GCN)**. It leverages **Databricks Asset Bundles (DABs)** for infrastructure-as-code and **Delta Live Tables (DLT)** for the ETL process.

The pipeline ingests raw GCN messages (Kafka), parses them into various formats (Text, VoEvent, Binary, Notices, Circulars), and summarizes them into a Gold layer. It follows the **Medallion Architecture** (Bronze -> Silver -> Gold).

## Key Technologies

*   **Language:** Python 3.10+
*   **Platform:** Databricks (Asset Bundles, Delta Live Tables, Unity Catalog)
*   **Package Manager:** `uv`
*   **Testing:** `pytest`
*   **Orchestration:** Databricks Workflows (Jobs & DLT Pipelines)

## Directory Structure

*   `src/nasa_gcn/`: Main Python source code (parsers, utilities, pipeline logic).
*   `resources/`: Databricks Job and Pipeline YAML definitions.
*   `docs/`: Documentation for RAG (Retrieval-Augmented Generation) use cases.
*   `tests/`: Unit and integration tests.
*   `databricks.yml`: Main configuration for the Databricks Asset Bundle.
*   `deploy.sh`: Helper script for deployment and execution.

## Development Workflow

### 1. Environment Setup

The project uses `uv` for dependency management.

```bash
# Install uv (if not already installed)
curl -Ls https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync --dev

# Activate virtual environment
source .venv/bin/activate
```

### 2. Configuration (`.env`)

Create a `.env` file based on `.env.example` with your NASA GCN credentials.

```bash
cp .env.example .env
# Edit .env and add GCN_CLIENT_ID and GCN_CLIENT_SECRET
```

### 3. Build & Deploy

The project uses a helper script `deploy.sh` for streamlined operations.

*   **Deploy (only):**
    ```bash
    ./deploy.sh
    ```
    *Builds the Python wheel and uploads the bundle configuration to the Databricks workspace (dev environment).*

*   **Deploy & Run:**
    ```bash
    ./deploy.sh run
    ```
    *Deploys changes and triggers the main job (`nasa_gcn_job`).*

*   **Run (only):**
    ```bash
    ./deploy.sh run-only
    ```
    *Triggers the job without rebuilding/deploying.*

*   **Manual Deployment (using Databricks CLI):**
    ```bash
    databricks bundle validate
    databricks bundle deploy -t dev
    databricks bundle run nasa_gcn_job
    ```

### 4. Testing & Quality

Run tests and linting checks before committing.

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format .

# Check for linting errors
uv run ruff check .
```

## Architecture & Data Flow

1.  **Ingestion (Bronze):** Raw Kafka messages are ingested into `gcn_raw`.
2.  **Processing (Silver):** Data is parsed and routed to specific tables based on format:
    *   `gcn_classic_text`
    *   `gcn_classic_voevent`
    *   `gcn_classic_binary`
    *   `gcn_notices`
    *   `gcn_circulars`
    *   `igwn_gwalert`
3.  **Aggregation (Gold):** `gcn_events_summarized` contains consolidated event narratives.

## Useful Commands

*   **Validate Bundle:** `databricks bundle validate`
*   **List DLT Pipelines:** `databricks bundle run nasa_gcn_pipeline --refresh-all` (triggers full refresh)
*   **Check Auth:** `databricks auth profiles`

## Documentation

Refer to the `docs/` directory for detailed specifications on how different GCN message types are handled and their RAG applications.
