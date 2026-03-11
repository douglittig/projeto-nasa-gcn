-- ==============================================================================
-- GOLD PIPELINE: Enriched & Aggregated Data
-- ==============================================================================
-- Creates business-ready materialized views with aggregations and enrichments
-- from Silver layer tables.
--
-- Source: ${silver_catalog}.${silver_schema}.*
-- Target: Current pipeline catalog/schema (gold)
--
-- Converted from Python to SQL for CLUSTER BY AUTO support - February 2026
-- ==============================================================================

-- ==============================================================================
-- gcn_events_summary: Consolidated astronomical events with narratives
-- ==============================================================================
-- Aggregates all circulars per event_id and enriches with GW alert metadata.
-- This is the primary table for downstream analytics and reporting.
-- ==============================================================================

CREATE OR REPLACE MATERIALIZED VIEW gcn_events_summary
COMMENT 'Consolidated astronomical events with scientific narratives'
AS
WITH agg_circulars AS (
    SELECT
        event_id,
        COUNT(circular_id) AS circular_count,
        CONCAT_WS('\n\n---\n\n', COLLECT_LIST(document_text)) AS scientific_narrative,
        MAX(created_on) AS last_updated
    FROM `${silver_catalog}`.`${silver_schema}`.gcn_circulars
    WHERE event_id IS NOT NULL
    GROUP BY event_id
)
SELECT
    c.event_id,
    c.circular_count,
    c.last_updated,
    g.alert_type,
    c.scientific_narrative,
    current_timestamp() AS processed_at
FROM agg_circulars c
LEFT JOIN `${silver_catalog}`.`${silver_schema}`.gcn_gwalert g
    ON c.event_id = g.event_id;


-- ==============================================================================
-- gcn_daily_stats: Daily statistics of GCN activity
-- ==============================================================================
-- Provides counts of circulars, notices, and alerts per day.
-- Used for monitoring and reporting dashboards.
-- ==============================================================================

CREATE OR REPLACE MATERIALIZED VIEW gcn_daily_stats
COMMENT 'Daily statistics of GCN activity'
AS
WITH circulars_daily AS (
    SELECT
        DATE_TRUNC('day', created_on) AS date,
        COUNT(*) AS circular_count
    FROM `${silver_catalog}`.`${silver_schema}`.gcn_circulars
    GROUP BY DATE_TRUNC('day', created_on)
),
notices_daily AS (
    SELECT
        DATE_TRUNC('day', kafka_timestamp) AS date,
        COUNT(*) AS notice_count
    FROM `${silver_catalog}`.`${silver_schema}`.gcn_notices
    GROUP BY DATE_TRUNC('day', kafka_timestamp)
),
gwalerts_daily AS (
    SELECT
        DATE_TRUNC('day', kafka_timestamp) AS date,
        COUNT(*) AS gwalert_count
    FROM `${silver_catalog}`.`${silver_schema}`.gcn_gwalert
    GROUP BY DATE_TRUNC('day', kafka_timestamp)
)
SELECT
    COALESCE(c.date, n.date, g.date) AS date,
    COALESCE(c.circular_count, 0) AS circulars,
    COALESCE(n.notice_count, 0) AS notices,
    COALESCE(g.gwalert_count, 0) AS gwalerts,
    current_timestamp() AS processed_at
FROM circulars_daily c
FULL OUTER JOIN notices_daily n ON c.date = n.date
FULL OUTER JOIN gwalerts_daily g ON COALESCE(c.date, n.date) = g.date;
