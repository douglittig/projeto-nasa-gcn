"""
NASA GCN Pipeline - Environment Bootstrap

This module centralizes the sys.path manipulation required for running
Spark Declarative Pipelines in Databricks Free/Community Edition.

==============================================================================
PEDAGOGICAL NOTE: FREE EDITION vs PRODUCTION
==============================================================================

This is a WORKAROUND for Free/Community Edition limitations.

IN FREE EDITION (current approach):
    - We use runtime path resolution to import sibling modules
    - The `bundle.sourcePath` Spark config tells us where our code lives
    - We manually add directories to sys.path so Python can find our modules
    - This "hack" is necessary because Free Edition doesn't support:
        * Managed Git repos with automatic PYTHONPATH
        * Workspace libraries installed as wheels
        * Unity Catalog-managed Python packages

IN PRODUCTION (recommended approach):
    - Build a Python Wheel (.whl) package from the `nasa_gcn` module
    - Declare it in the `libraries` section of your pipeline YAML:

        libraries:
          - whl: /Volumes/catalog/schema/wheels/nasa_gcn-1.0.0-py3-none-any.whl

    - Or use PyPI/private repo:

        libraries:
          - pypi:
              package: nasa-gcn==1.0.0

    - The wheel is installed on cluster startup, making all imports "just work"
    - No sys.path manipulation needed - clean, production-grade code

This bootstrap module exists to:
    1. Isolate infrastructure concerns from business logic
    2. Provide a single import for pipelines: `import _bootstrap`
    3. Document the architectural compromise for educational purposes

==============================================================================
"""

import os
import sys


def setup_environment(spark_session=None) -> None:
    """
    Configure Python path for Databricks SDP runtime.

    Args:
        spark_session: The Spark session (global `spark` variable in SDP context).
                      Pass it explicitly since globals aren't shared across modules.

    This function must be called at module import time (not inside functions)
    because Python resolves imports at parse time.
    """
    try:
        # Databricks Asset Bundles set this config with the deployed source path
        if spark_session is not None:
            source_path = spark_session.conf.get("bundle.sourcePath", "")
            if source_path and source_path not in sys.path:
                sys.path.insert(0, source_path)

        # Local development fallback: add parent directories
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)  # nasa_gcn/
        grandparent_dir = os.path.dirname(parent_dir)  # src/

        for path in [parent_dir, grandparent_dir]:
            if path not in sys.path:
                sys.path.append(path)

    except Exception:
        # Silently fail - we're either in a test environment or
        # the paths are already configured correctly
        pass


# Execute local path setup on import (doesn't need spark)
# The spark-dependent setup will be called explicitly from pipelines
setup_environment()
