"""
NASA GCN Gold Pipeline - Enriched & Aggregated Data

Creates business-ready tables with aggregations and enrichments
from Silver layer tables.

Source: nasa_gcn.silver.*
Target: nasa_gcn.gold.*

Migrated from DLT to Spark Declarative Pipelines (SDP) - February 2026
"""

from pyspark import pipelines as dp
from pyspark.sql.functions import (
    col,
    collect_list,
    concat_ws,
    count,
    current_timestamp,
    date_trunc,
    max,
)

# ==============================================================================
# CONFIGURATION: Silver source tables
# ==============================================================================
SILVER_CATALOG = spark.conf.get("silver_catalog", "nasa_gcn")
SILVER_SCHEMA = spark.conf.get("silver_schema", "silver")


# ==============================================================================
# GOLD TABLES
# ==============================================================================


@dp.materialized_view(
    name="gcn_events_summary",
    comment="Consolidated astronomical events with scientific narratives",
)
def events_summary():
    """
    Gold layer: Event summaries combining circulars and gravitational wave alerts.

    Aggregates all circulars per event_id and enriches with GW alert metadata.
    This is the primary table for downstream analytics and reporting.
    """
    circulars_table = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.gcn_circulars"
    gwalert_table = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.gcn_gwalert"

    circs = spark.read.table(circulars_table)
    gws = spark.read.table(gwalert_table)

    agg_circs = (
        circs.groupBy("event_id")
        .agg(
            count("circular_id").alias("circular_count"),
            concat_ws("\n\n---\n\n", collect_list("document_text")).alias("scientific_narrative"),
            max("created_on").alias("last_updated"),
        )
        .filter(col("event_id").isNotNull())
    )

    return agg_circs.join(gws, "event_id", "left").select(
        "event_id",
        "circular_count",
        "last_updated",
        "alert_type",
        "scientific_narrative",
        current_timestamp().alias("processed_at"),
    )


@dp.materialized_view(
    name="gcn_daily_stats",
    comment="Daily statistics of GCN activity",
)
def daily_stats():
    """
    Gold layer: Daily aggregated statistics for monitoring and reporting.

    Provides counts of circulars, notices, and alerts per day.
    """
    circulars_table = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.gcn_circulars"
    notices_table = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.gcn_notices"
    gwalert_table = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.gcn_gwalert"

    circs = (
        spark.read.table(circulars_table)
        .withColumn("date", date_trunc("day", col("created_on")))
        .groupBy("date")
        .agg(count("*").alias("circular_count"))
    )

    notices = (
        spark.read.table(notices_table)
        .withColumn("date", date_trunc("day", col("kafka_timestamp")))
        .groupBy("date")
        .agg(count("*").alias("notice_count"))
    )

    gws = (
        spark.read.table(gwalert_table)
        .withColumn("date", date_trunc("day", col("kafka_timestamp")))
        .groupBy("date")
        .agg(count("*").alias("gwalert_count"))
    )

    return (
        circs.join(notices, "date", "full")
        .join(gws, "date", "full")
        .select(
            col("date"),
            col("circular_count").alias("circulars"),
            col("notice_count").alias("notices"),
            col("gwalert_count").alias("gwalerts"),
            current_timestamp().alias("processed_at"),
        )
        .fillna(0)
    )
