"""
NASA GCN Bronze Pipeline - Raw Data Ingestion

Ingests raw messages from NASA GCN Kafka stream into a single Bronze table.
All messages are stored as-is for downstream processing.

Target: nasa_gcn.bronze.raw

Migrated from DLT to Spark Declarative Pipelines (SDP) - February 2026
"""

import os
import sys

from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp

# ==============================================================================
# DRIVER SETUP: Allow importing sibling modules
# ==============================================================================
try:
    # Add bundle.sourcePath to sys.path for imports
    source_path = spark.conf.get("bundle.sourcePath", "")
    if source_path and source_path not in sys.path:
        sys.path.insert(0, source_path)

    # Also add parent directories for local development
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # nasa_gcn/
    grandparent_dir = os.path.dirname(parent_dir)  # src/
    for path in [parent_dir, grandparent_dir]:
        if path not in sys.path:
            sys.path.append(path)
except Exception:
    pass

try:
    from nasa_gcn.config import get_kafka_options
except ImportError:
    from config import get_kafka_options


# ==============================================================================
# BRONZE TABLE: Raw Kafka Messages
# ==============================================================================


@dp.table(
    name="gcn_raw",
    comment="Raw messages from NASA GCN Kafka stream - all topics combined",
    cluster_by=["topic", "kafka_timestamp"],
)
def raw():
    """
    Bronze layer: Raw ingestion from NASA GCN Kafka.

    Captures all messages from all topics without transformation.
    Adds metadata columns for tracking and debugging.
    """
    return (
        spark.readStream.format("kafka")
        .options(**get_kafka_options())
        .load()
        .select(
            col("key").cast("string").alias("message_key"),
            "value",
            "topic",
            "partition",
            "offset",
            col("timestamp").alias("kafka_timestamp"),
            current_timestamp().alias("ingested_at"),
        )
    )
