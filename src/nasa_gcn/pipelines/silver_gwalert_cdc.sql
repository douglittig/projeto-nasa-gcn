-- ==============================================================================
-- SILVER: GCN GW Alert with AUTO CDC (SCD Type 2)
-- ==============================================================================
-- Gravitational wave alerts from LIGO/Virgo/KAGRA with full history tracking.
-- Uses AUTO CDC to deduplicate by event_id while preserving all alert versions.
--
-- SCD Type 2 adds columns:
--   - __START_AT: When this version became valid
--   - __END_AT: When this version was superseded (NULL = current)
--
-- To query only current records: WHERE __END_AT IS NULL
-- ==============================================================================

-- Intermediate streaming table with parsed JSON (required for AUTO CDC)
CREATE OR REPLACE STREAMING TABLE gcn_gwalert_parsed AS
SELECT
    message_key,
    CAST(value AS STRING) AS json,
    get_json_object(CAST(value AS STRING), '$.superevent_id') AS event_id,
    get_json_object(CAST(value AS STRING), '$.alert_type') AS alert_type,
    kafka_timestamp,
    current_timestamp() AS processed_at
FROM stream(`${bronze_catalog}`.`${bronze_schema}`.gcn_raw)
WHERE topic = 'igwn.gwalert'
  AND get_json_object(CAST(value AS STRING), '$.superevent_id') IS NOT NULL;

-- Target streaming table for AUTO CDC
CREATE OR REFRESH STREAMING TABLE gcn_gwalert
COMMENT 'IGWN Gravitational Wave Alerts with SCD Type 2 history tracking'
CLUSTER BY (event_id);

-- AUTO CDC flow: Deduplicates by event_id, orders by kafka_timestamp
CREATE FLOW gwalert_cdc_flow AS
AUTO CDC INTO gcn_gwalert
FROM stream(gcn_gwalert_parsed)
KEYS (event_id)
SEQUENCE BY kafka_timestamp
COLUMNS * EXCEPT (processed_at)
STORED AS SCD TYPE 2;
