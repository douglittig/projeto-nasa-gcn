"""
NASA GCN Data Pipeline (Delta Live Tables)
"""

import dlt
from pyspark.sql.functions import (
    coalesce,
    col,
    collect_list,
    concat_ws,
    count,
    current_timestamp,
    expr,
    from_json,
    get_json_object,
    lit,
    max,
    regexp_extract,
    udf,
)

# Import modularized logic
from nasa_gcn.binary_parser import PARSED_BINARY_SCHEMA, parse_gcn_binary_packet
from nasa_gcn.config import get_kafka_options
from nasa_gcn.schemas import CIRCULAR_SCHEMA
from nasa_gcn.utils import clean_json_id, decode_utf8

# Register binary parser UDF
parse_binary_udf = udf(parse_gcn_binary_packet, PARSED_BINARY_SCHEMA)


@dlt.table(name="gcn_raw")
def gcn_raw():
    return (
        spark.readStream.format("kafka")
        .options(**get_kafka_options())
        .load()
        .select(  # type: ignore
            col("key").cast("string").alias("message_key"),
            "value",
            "topic",
            "partition",
            "offset",
            col("timestamp").alias("kafka_timestamp"),
            current_timestamp().alias("ingestion_timestamp"),
        )
    )


@dlt.table(name="gcn_classic_text")
def gcn_classic_text():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic").startswith("gcn.classic.text."))
        .withColumn("text", decode_utf8())
        .select(
            "message_key",
            col("text").alias("message_text"),
            "topic",
            regexp_extract(col("text"), r"TITLE:\s+(.*?)(?=\\n)", 1).alias("title"),
            col("text").alias("document_text"),
            "kafka_timestamp",
            current_timestamp().alias("silver_ts"),
        )
    )


@dlt.table(name="gcn_classic_voevent")
def gcn_classic_voevent():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic").startswith("gcn.classic.voevent."))
        .withColumn("xml", decode_utf8())
        .select(
            "message_key",
            "xml",
            "topic",
            expr("xpath_string(xml, '/*[local-name()=\"VOEvent\"]/@ivorn')").alias("ivorn"),
            concat_ws(
                " | ", lit("ID"), expr("xpath_string(xml, '/*[local-name()=\"VOEvent\"]/@ivorn')")
            ).alias("document_text"),
            "kafka_timestamp",
            current_timestamp().alias("silver_ts"),
        )
    )


@dlt.table(name="gcn_classic_binary")
def gcn_classic_binary():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic").startswith("gcn.classic.binary."))
        .withColumn("p", parse_binary_udf("value"))
        .select(
            "message_key", "p.*", "topic", "kafka_timestamp", current_timestamp().alias("silver_ts")
        )
    )


@dlt.table(name="gcn_notices")
def gcn_notices():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic").startswith("gcn.notices."))
        .withColumn("json", decode_utf8())
        .select(
            "message_key",
            "json",
            "topic",
            clean_json_id(
                coalesce(get_json_object("json", "$.id"), get_json_object("json", "$.event_name"))
            ).alias("notice_id"),
            "kafka_timestamp",
            current_timestamp().alias("silver_ts"),
        )
    )


@dlt.table(name="gcn_circulars")
def gcn_circulars():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic") == "gcn.circulars")
        .withColumn("json", decode_utf8())
        .withColumn("p", from_json("json", CIRCULAR_SCHEMA))
        .select(
            "message_key",
            "json",
            col("p.circularId").alias("circular_id"),
            col("p.eventId").alias("event_id"),
            "p.subject",
            "p.body",
            (col("p.createdOn") / 1000).cast("timestamp").alias("created_on"),
            concat_ws("\n", lit("SUBJECT: "), col("p.subject"), lit("---"), col("p.body")).alias(
                "document_text"
            ),
            "kafka_timestamp",
            current_timestamp().alias("silver_ts"),
        )
    )


@dlt.table(name="igwn_gwalert")
def igwn_gwalert():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic") == "igwn.gwalert")
        .withColumn("json", decode_utf8())
        .select(
            "message_key",
            "json",
            get_json_object("json", "$.superevent_id").alias("event_id"),
            get_json_object("json", "$.alert_type").alias("alert_type"),
            "kafka_timestamp",
            current_timestamp().alias("silver_ts"),
        )
    )


@dlt.table(name="gcn_heartbeat")
def gcn_heartbeat():
    return (
        dlt.read_stream("gcn_raw")
        .filter(col("topic") == "gcn.heartbeat")
        .select("message_key", decode_utf8().alias("heartbeat_json"), "topic", "kafka_timestamp")
    )


@dlt.table(name="gcn_events_summarized")
def gcn_events_summarized():
    circs = dlt.read("gcn_circulars")
    gws = dlt.read("igwn_gwalert")
    agg_circs = (
        circs.groupBy("event_id")
        .agg(
            count("circular_id").alias("circular_count"),
            concat_ws("\n\n---\n\n", collect_list("document_text")).alias("scientific_narrative"),
            max("created_on").alias("last_date"),
        )
        .filter(col("event_id").isNotNull())
    )
    return agg_circs.join(gws, "event_id", "left").select(
        "event_id",
        "circular_count",
        "last_date",
        "alert_type",
        "scientific_narrative",
        current_timestamp().alias("gold_ts"),
    )
