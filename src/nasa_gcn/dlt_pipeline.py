"""
NASA GCN Data Pipeline (Delta Live Tables)
"""

import os
import struct
from typing import Any, Dict

import dlt
from pyspark.sql.functions import (
    Column,
    coalesce,
    col,
    collect_list,
    concat_ws,
    count,
    current_timestamp,
    decode,
    expr,
    from_json,
    get_json_object,
    lit,
    max,
    regexp_extract,
    regexp_replace,
    udf,
)


def decode_utf8(col_name: str = "value") -> Column:
    return decode(col(col_name), "UTF-8")


def clean_json_id(id_col: Column) -> Column:
    step1 = regexp_replace(id_col, r'^[\["]+', "")
    return regexp_replace(step1, r'[\]"]+$', "")


CIRCULAR_SCHEMA = (
    "circularId INT, eventId STRING, subject STRING, body STRING, submitter STRING, "
    "submittedHow STRING, createdOn LONG, format STRING"
)


def _get_credential(name: str) -> str:
    try:
        if spark:  # type: ignore
            val = spark.conf.get(name, "")
            if val:
                return val
    except:
        pass
    return os.getenv(name, "")


def get_kafka_options() -> dict:
    cid = _get_credential("GCN_CLIENT_ID")
    sec = _get_credential("GCN_CLIENT_SECRET")
    jaas = (
        f"kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required "
        f'clientId="{cid}" clientSecret="{sec}";'
    )
    return {
        "kafka.bootstrap.servers": "kafka.gcn.nasa.gov:9092",
        "kafka.security.protocol": "SASL_SSL",
        "kafka.sasl.mechanism": "OAUTHBEARER",
        "kafka.sasl.jaas.config": jaas,
        "kafka.sasl.login.callback.handler.class": "kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginCallbackHandler",
        "kafka.sasl.oauthbearer.token.endpoint.url": "https://auth.gcn.nasa.gov/oauth2/token",
        "failOnDataLoss": "false",
        "startingOffsets": "earliest",
        "subscribePattern": "gcn\\.heartbeat|gcn\\.classic\\.text\\..*|gcn\\.classic\\.voevent\\..*|gcn\\.classic\\.binary\\..*|gcn\\.notices\\..*|gcn\\.circulars|igwn\\.gwalert",
    }


def parse_gcn_binary_packet(data: bytes) -> Dict[str, Any]:
    if data is None or len(data) != 160:
        return {"parse_error": "size"}
    try:
        l = struct.unpack(">40i", data)
        return {
            "pkt_type": l[0],
            "trig_num": l[4] if l[4] > 0 else None,
            "ra": l[7] / 100.0,
            "dec": l[8] / 100.0,
        }
    except Exception as e:
        return {"parse_error": str(e)}


parse_binary_udf = udf(
    parse_gcn_binary_packet, "pkt_type INT, trig_num INT, ra DOUBLE, dec DOUBLE, parse_error STRING"
)


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
            regexp_extract(col("text"), r"TITLE:\s+(.*?)(?=\n)", 1).alias("title"),
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
    return agg_circs.join(gws.withColumnRenamed("event_id", "event_id"), "event_id", "left").select(
        "event_id",
        "circular_count",
        "last_date",
        "alert_type",
        "scientific_narrative",
        current_timestamp().alias("gold_ts"),
    )
