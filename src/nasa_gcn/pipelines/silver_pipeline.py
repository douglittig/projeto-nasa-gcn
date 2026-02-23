"""
NASA GCN Silver Pipeline - Cleaned & Typed Data

Reads from Bronze raw table and creates topic-specific Silver tables
with proper schemas, parsing, and data quality.

Source: nasa_gcn.bronze.raw
Target: nasa_gcn.silver.*

Migrated from DLT to Spark Declarative Pipelines (SDP) - February 2026
"""

import struct
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

# Bootstrap: configure sys.path for Free Edition (see _bootstrap.py for details)
import _bootstrap

from pyspark import pipelines as dp
from pyspark.sql.functions import (
    coalesce,
    col,
    concat_ws,
    current_timestamp,
    expr,
    from_json,
    get_json_object,
    lit,
    regexp_extract,
    udf,
)

# Complete setup with spark session (spark is global in SDP context)
_bootstrap.setup_environment(spark)  # noqa: F821

try:
    from nasa_gcn.schemas import CIRCULAR_SCHEMA
    from nasa_gcn.utils import clean_json_id, decode_utf8
except ImportError:
    from schemas import CIRCULAR_SCHEMA
    from utils import clean_json_id, decode_utf8


# ==============================================================================
# BINARY PARSER (Embedded for UDF compatibility)
# ==============================================================================
PACKET_TYPE_NAMES: Dict[int, str] = {
    1: "BATSE_ORIGINAL",
    2: "TEST",
    3: "IMALIVE",
    4: "KILL",
    11: "BATSE_MAXBC",
    21: "BRADFORD_TEST",
    22: "BATSE_FINAL",
    24: "BATSE_LOCBURST",
    25: "ALEXIS",
    26: "RXTE_PCA_ALERT",
    27: "RXTE_PCA",
    28: "RXTE_ASM_ALERT",
    29: "RXTE_ASM",
    30: "COMPTEL",
    31: "IPN_RAW",
    32: "IPN_SEGMENT",
    33: "SAX_WFC_ALERT",
    34: "SAX_WFC",
    35: "SAX_NFI_ALERT",
    36: "SAX_NFI",
    37: "RXTE_ASM_XTRANS",
    38: "SPARE_TESTING",
    39: "IPN_POSITION",
    40: "HETE_S/C_ALERT",
    41: "HETE_S/C_UPDATE",
    42: "HETE_S/C_LAST",
    43: "HETE_GNDANA",
    44: "HETE_TEST",
    45: "GRB_COUNTERPART",
    46: "SWIFT_TOO_FOM_OBSERVE",
    47: "SWIFT_TOO_SC_SLEW",
    48: "DOW_TOD_TEST",
    51: "INTEGRAL_POINTDIR",
    52: "INTEGRAL_SPIACS",
    53: "INTEGRAL_WAKEUP",
    54: "INTEGRAL_REFINED",
    55: "INTEGRAL_OFFLINE",
    56: "INTEGRAL_WEAK",
    57: "AAVSO",
    58: "MILAGRO",
    59: "KONUS_LIGHTCURVE",
    60: "SWIFT_BAT_GRB_ALERT",
    61: "SWIFT_BAT_GRB_POSITION",
    62: "SWIFT_BAT_GRB_NACK",
    63: "SWIFT_BAT_GRB_LC",
    64: "SWIFT_BAT_SCALED_MAP",
    65: "SWIFT_FOM_OBSERVE",
    66: "SWIFT_SC_SLEW",
    67: "SWIFT_XRT_POSITION",
    68: "SWIFT_XRT_SPECTRUM",
    69: "SWIFT_XRT_IMAGE",
    70: "SWIFT_XRT_LIGHTCURVE",
    71: "SWIFT_XRT_NACK_POSITION",
    72: "SWIFT_UVOT_IMAGE",
    73: "SWIFT_UVOT_SRC_LIST",
    76: "SWIFT_BAT_GRB_PROC_LC",
    77: "SWIFT_XRT_PROC_SPECTRUM",
    78: "SWIFT_XRT_PROC_IMAGE",
    79: "SWIFT_UVOT_PROC_IMAGE",
    80: "SWIFT_UVOT_PROC_SRC_LIST",
    81: "SWIFT_UVOT_POSITION",
    82: "SWIFT_BAT_GRB_POS_TEST",
    83: "SWIFT_POINTDIR",
    84: "SWIFT_BAT_TRANS",
    85: "SWIFT_XRT_THRESHPIX",
    86: "SWIFT_XRT_THRESHPIX_PROC",
    87: "SWIFT_XRT_SPER",
    88: "SWIFT_XRT_SPER_PROC",
    89: "SWIFT_UVOT_NACK_POSITION",
    97: "SWIFT_BAT_QUICKLOOK_POSITION",
    98: "SWIFT_BAT_SUBTHRESHOLD_POSITION",
    99: "SWIFT_BAT_SLEW_GRB_POSITION",
    103: "SWIFT_ACTUAL_POINTDIR",
    133: "SWIFT_BAT_MONITOR",
    140: "SWIFT_BAT_SUB_SUB_THRESH_POS",
    141: "SWIFT_BAT_KNOWN_SRC_POS",
    100: "SUPERAGILE_GRB_WAKEUP",
    101: "SUPERAGILE_GRB_GROUND",
    102: "SUPERAGILE_GRB_REFINED",
    105: "AGILE_MCAL_ALERT",
    107: "AGILE_POINTDIR",
    109: "SUPERAGILE_GRB_POS_TEST",
    110: "FERMI_GBM_ALERT",
    111: "FERMI_GBM_FLT_POS",
    112: "FERMI_GBM_GND_POS",
    114: "FERMI_GBM_GND_INTERNAL",
    115: "FERMI_GBM_FINAL_POS",
    116: "FERMI_GBM_ALERT_INTERNAL",
    117: "FERMI_GBM_FLT_INTERNAL",
    119: "FERMI_GBM_POS_TEST",
    131: "FERMI_GBM_SUBTHRESHOLD",
    120: "FERMI_LAT_GRB_POS_INI",
    121: "FERMI_LAT_GRB_POS_UPD",
    122: "FERMI_LAT_GRB_POS_DIAG",
    123: "FERMI_LAT_TRANS",
    124: "FERMI_LAT_GRB_POS_TEST",
    125: "FERMI_LAT_MONITOR",
    126: "FERMI_SC_SLEW",
    127: "FERMI_LAT_GND",
    128: "FERMI_LAT_OFFLINE",
    129: "FERMI_POINTDIR",
    144: "FERMI_SC_SLEW_INTERNAL",
    146: "FERMI_GBM_FIN_POS_INTERNAL",
    130: "SIMBAD_NED_SEARCH_RESULTS",
    134: "MAXI_UNKNOWN_SOURCE",
    135: "MAXI_KNOWN_SOURCE",
    136: "MAXI_TEST",
    137: "OGLE",
    139: "MOA",
    145: "COINCIDENCE",
    148: "SUZAKU_LIGHTCURVE",
    149: "SNEWS",
    150: "LVC_PRELIMINARY",
    151: "LVC_INITIAL",
    152: "LVC_UPDATE",
    153: "LVC_TEST",
    154: "LVC_COUNTERPART",
    163: "LVC_EARLY_WARNING",
    164: "LVC_RETRACTION",
    157: "AMON_ICECUBE_COINC",
    158: "AMON_ICECUBE_HESE",
    159: "AMON_ICECUBE_TEST",
    160: "CALET_GBM_FLT_LC",
    161: "CALET_GBM_GND_LC",
    166: "AMON_ICECUBE_CLUSTER",
    168: "GWHEN_COINC",
    169: "AMON_ICECUBE_EHE",
    170: "AMON_ANTARES_FERMILAT_COINC",
    171: "HAWC_BURST_MONITOR",
    172: "AMON_NU_EM_COINC",
    173: "ICECUBE_ASTROTRACK_GOLD",
    174: "ICECUBE_ASTROTRACK_BRONZE",
    175: "SK_SUPERNOVA",
    176: "AMON_ICECUBE_CASCADE",
    188: "GECAM_FLT",
    189: "GECAM_GND",
}

TJD_EPOCH = datetime(1968, 5, 24, 0, 0, 0)


def get_packet_type_name(pkt_type: int) -> str:
    return PACKET_TYPE_NAMES.get(pkt_type, f"UNKNOWN_TYPE_{pkt_type}")


def tjd_sod_to_datetime(tjd: int, sod_centi: int) -> Optional[datetime]:
    if tjd <= 0 or sod_centi < 0:
        return None
    try:
        sod_seconds = sod_centi / 100.0
        return TJD_EPOCH + timedelta(days=tjd, seconds=sod_seconds)
    except (ValueError, OverflowError):
        return None


def centi_to_deg(value: int, scale: int = 100) -> float:
    return value / scale


def parse_gcn_binary_packet(binary_data: bytes) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "pkt_type": None,
        "pkt_type_name": None,
        "pkt_sernum": None,
        "trig_num": None,
        "burst_tjd": None,
        "burst_sod_centi": None,
        "burst_datetime": None,
        "burst_ra_deg": None,
        "burst_dec_deg": None,
        "burst_error_deg": None,
        "trigger_id": None,
        "misc": None,
        "parse_error": None,
    }
    if binary_data is None:
        result["parse_error"] = "binary_data is None"
        return result
    if len(binary_data) != 160:
        result["parse_error"] = f"Invalid packet size: {len(binary_data)} bytes (expected 160)"
        return result
    try:
        longs = struct.unpack(">40i", binary_data)
        pkt_type = longs[0]
        result["pkt_type"] = pkt_type
        result["pkt_type_name"] = get_packet_type_name(pkt_type)
        result["pkt_sernum"] = longs[1]
        trig_num = longs[4]
        result["trig_num"] = trig_num if trig_num > 0 else None
        burst_tjd = longs[5]
        burst_sod = longs[6]
        result["burst_tjd"] = burst_tjd
        result["burst_sod_centi"] = burst_sod
        if burst_tjd > 0 and burst_sod >= 0:
            burst_dt = tjd_sod_to_datetime(burst_tjd, burst_sod)
            if burst_dt:
                result["burst_datetime"] = burst_dt.isoformat()
        burst_ra = longs[7]
        burst_dec = longs[8]
        burst_error = longs[11]
        if burst_ra > 36000 or burst_ra < 0 or abs(burst_dec) > 9000:
            scale = 10000
        else:
            scale = 100
        ra_deg = centi_to_deg(burst_ra, scale)
        dec_deg = centi_to_deg(burst_dec, scale)
        err_deg = centi_to_deg(abs(burst_error), scale)
        if 0 <= ra_deg < 360:
            result["burst_ra_deg"] = ra_deg
        if -90 <= dec_deg <= 90:
            result["burst_dec_deg"] = dec_deg
        result["burst_error_deg"] = err_deg
        result["trigger_id"] = longs[18]
        result["misc"] = longs[19]
    except struct.error as e:
        result["parse_error"] = f"Struct unpack error: {e}"
    except Exception as e:
        result["parse_error"] = f"Unexpected error: {e}"
    return result


PARSED_BINARY_SCHEMA = """
    pkt_type INT,
    pkt_type_name STRING,
    pkt_sernum INT,
    trig_num INT,
    burst_tjd INT,
    burst_sod_centi INT,
    burst_datetime STRING,
    burst_ra_deg DOUBLE,
    burst_dec_deg DOUBLE,
    burst_error_deg DOUBLE,
    trigger_id INT,
    misc INT,
    parse_error STRING
"""

parse_binary_udf = udf(parse_gcn_binary_packet, PARSED_BINARY_SCHEMA)


# ==============================================================================
# CONFIGURATION: Bronze source table
# ==============================================================================
# The Silver pipeline reads from the Bronze catalog
BRONZE_CATALOG = spark.conf.get("bronze_catalog", "nasa_gcn")
BRONZE_SCHEMA = spark.conf.get("bronze_schema", "bronze")
BRONZE_TABLE = f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.gcn_raw"


# ==============================================================================
# SILVER TABLES
# ==============================================================================


@dp.table(
    name="gcn_circulars",
    comment="GCN Circulars - Human-written astronomical reports",
    cluster_by=["event_id", "created_on"],
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
@dp.expect_or_drop("valid_circular_id", "circular_id IS NOT NULL")
@dp.expect_or_drop("valid_event_id", "event_id IS NOT NULL")
def circulars():
    """Scientific circulars from astronomers about transient events."""
    return (
        spark.readStream.table(BRONZE_TABLE)
        .filter(col("topic") == "gcn.circulars")
        .withColumn("json", decode_utf8())
        .withColumn("p", from_json("json", CIRCULAR_SCHEMA))
        .select(
            "message_key",
            col("p.circularId").alias("circular_id"),
            col("p.eventId").alias("event_id"),
            "p.subject",
            "p.body",
            (col("p.createdOn") / 1000).cast("timestamp").alias("created_on"),
            concat_ws("\n", lit("SUBJECT: "), col("p.subject"), lit("---"), col("p.body")).alias(
                "document_text"
            ),
            "kafka_timestamp",
            current_timestamp().alias("processed_at"),
        )
    )


@dp.table(
    name="gcn_notices",
    comment="GCN Notices - Machine-generated alerts in JSON format",
    cluster_by=["topic", "kafka_timestamp"],
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
@dp.expect_or_drop("valid_notice_id", "notice_id IS NOT NULL")
def notices():
    """Automated notices from various missions (Fermi, Swift, etc.)."""
    return (
        spark.readStream.table(BRONZE_TABLE)
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
            current_timestamp().alias("processed_at"),
        )
    )


@dp.table(
    name="gcn_classic_text",
    comment="GCN Classic Text - Legacy text-format alerts",
    cluster_by=["topic", "kafka_timestamp"],
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
def classic_text():
    """Legacy text-format alerts from classic GCN system."""
    return (
        spark.readStream.table(BRONZE_TABLE)
        .filter(col("topic").startswith("gcn.classic.text."))
        .withColumn("text", decode_utf8())
        .select(
            "message_key",
            col("text").alias("message_text"),
            "topic",
            regexp_extract(col("text"), r"TITLE:\s+(.*?)(?=\\n)", 1).alias("title"),
            col("text").alias("document_text"),
            "kafka_timestamp",
            current_timestamp().alias("processed_at"),
        )
    )


@dp.table(
    name="gcn_classic_voevent",
    comment="GCN Classic VOEvent - XML-format astronomical alerts",
    cluster_by=["topic", "kafka_timestamp"],
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
def classic_voevent():
    """VOEvent XML alerts following IVOA standard."""
    return (
        spark.readStream.table(BRONZE_TABLE)
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
            current_timestamp().alias("processed_at"),
        )
    )


@dp.table(
    name="gcn_classic_binary",
    comment="GCN Classic Binary - Parsed binary packet alerts",
    cluster_by=["pkt_type", "kafka_timestamp"],
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
@dp.expect_or_drop("valid_parse", "parse_error IS NULL")
def classic_binary():
    """Binary-format alerts with parsed coordinates and metadata."""
    return (
        spark.readStream.table(BRONZE_TABLE)
        .filter(col("topic").startswith("gcn.classic.binary."))
        .withColumn("p", parse_binary_udf("value"))
        .select(
            "message_key",
            "p.*",
            "topic",
            "kafka_timestamp",
            current_timestamp().alias("processed_at"),
        )
    )


# NOTE: gcn_gwalert table moved to silver_gwalert_cdc.sql
# Uses AUTO CDC with SCD Type 2 for deduplication and history tracking


@dp.table(
    name="gcn_heartbeat",
    comment="GCN Heartbeat - System health messages",
    cluster_by=["kafka_timestamp"],
    table_properties={
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
def heartbeat():
    """Heartbeat messages for monitoring Kafka connectivity."""
    return (
        spark.readStream.table(BRONZE_TABLE)
        .filter(col("topic") == "gcn.heartbeat")
        .select(
            "message_key",
            decode_utf8().alias("heartbeat_json"),
            "topic",
            "kafka_timestamp",
            current_timestamp().alias("processed_at"),
        )
    )
