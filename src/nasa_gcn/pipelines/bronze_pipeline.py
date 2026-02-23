"""
NASA GCN Bronze Pipeline - Raw Data Ingestion

Ingests raw messages from NASA GCN Kafka stream into a single Bronze table.
All messages are stored as-is for downstream processing.

Target: nasa_gcn.bronze.raw

Migrated from DLT to Spark Declarative Pipelines (SDP) - February 2026
"""

# Bootstrap: configure sys.path for Free Edition (see _bootstrap.py for details)
import _bootstrap

from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp

# Complete setup with spark session (spark is global in SDP context)
_bootstrap.setup_environment(spark)  # noqa: F821

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
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
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
