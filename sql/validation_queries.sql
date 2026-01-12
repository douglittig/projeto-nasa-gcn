-- ==============================================================================
-- NASA GCN Pipeline - Queries de Validação
-- ==============================================================================
-- Use estas queries para validar os dados após execução do pipeline DLT.
-- Todas as tabelas estão no schema: sandbox.nasa_gcn_dev
-- ==============================================================================

-- ============================================================================
-- BRONZE LAYER
-- ============================================================================

-- Contagem total de mensagens na camada Bronze
SELECT 
    topic,
    COUNT(*) as total_messages,
    MIN(kafka_timestamp) as first_message,
    MAX(kafka_timestamp) as last_message
FROM sandbox.nasa_gcn_dev.gcn_raw
GROUP BY topic
ORDER BY total_messages DESC;

-- ============================================================================
-- SILVER LAYER - gcn_classic_binary
-- ============================================================================

-- Distribuição de tipos de pacotes binários
SELECT 
    pkt_type_name, 
    pkt_type,
    COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_classic_binary
GROUP BY pkt_type_name, pkt_type
ORDER BY total DESC;

-- Verificar tipos UNKNOWN (devem ser mínimos)
SELECT 
    pkt_type_name, 
    COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_classic_binary
WHERE pkt_type_name LIKE 'UNKNOWN%'
GROUP BY pkt_type_name;

-- Erros de parsing
SELECT 
    parse_error,
    COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_classic_binary
WHERE parse_error IS NOT NULL
GROUP BY parse_error;

-- ============================================================================
-- SILVER LAYER - gcn_circulars (RAG)
-- ============================================================================

-- Validar campos extraídos
SELECT 
    circular_id, 
    event_id, 
    event_type, 
    subject, 
    word_count, 
    char_count, 
    submitter_name,
    created_on
FROM sandbox.nasa_gcn_dev.gcn_circulars
LIMIT 10;

-- Distribuição por tipo de evento
SELECT 
    event_type, 
    COUNT(*) as total,
    AVG(word_count) as avg_words,
    AVG(char_count) as avg_chars
FROM sandbox.nasa_gcn_dev.gcn_circulars
GROUP BY event_type
ORDER BY total DESC;

-- Circulars para RAG (filtro por tamanho)
SELECT 
    circular_id, 
    event_type,
    subject,
    word_count,
    LENGTH(document_text) as doc_text_length
FROM sandbox.nasa_gcn_dev.gcn_circulars
WHERE word_count > 50
ORDER BY created_on DESC
LIMIT 20;

-- ============================================================================
-- SILVER LAYER - gcn_notices (RAG)
-- ============================================================================

-- Validar campos extraídos
SELECT 
    mission, 
    mission_name, 
    messenger, 
    notice_id, 
    alert_type,
    alert_tense,
    ra, 
    dec, 
    ra_dec_error,
    document_text
FROM sandbox.nasa_gcn_dev.gcn_notices
LIMIT 10;

-- Distribuição por missão e messenger
SELECT 
    mission_name, 
    messenger,
    alert_tense,
    COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_notices
GROUP BY mission_name, messenger, alert_tense
ORDER BY total DESC;

-- Notices com coordenadas válidas
SELECT 
    notice_id,
    mission_name,
    ra,
    dec,
    ra_dec_error,
    trigger_time
FROM sandbox.nasa_gcn_dev.gcn_notices
WHERE ra IS NOT NULL AND dec IS NOT NULL
LIMIT 20;

-- Campos específicos de neutrinos
SELECT 
    notice_id,
    mission_name,
    n_events,
    nu_energy,
    p_astro,
    luminosity_distance
FROM sandbox.nasa_gcn_dev.gcn_notices
WHERE messenger = 'Neutrino'
LIMIT 10;

-- ============================================================================
-- SILVER LAYER - igwn_gwalert (RAG)
-- ============================================================================

-- Validar campos extraídos e document_text
SELECT 
    superevent_id, 
    alert_type, 
    group,
    pipeline,
    instruments,
    prob_bns,
    prob_bbh,
    document_text
FROM sandbox.nasa_gcn_dev.igwn_gwalert
WHERE superevent_id IS NOT NULL
LIMIT 10;

-- Verificar formatação dos instrumentos (não deve ter colchetes ou aspas)
SELECT instruments, topic
FROM sandbox.nasa_gcn_dev.igwn_gwalert 
WHERE instruments LIKE '%[%' OR instruments LIKE '%"%'
LIMIT 5;

-- Verificar alertas significativos
SELECT 
    superevent_id,
    significant,
    far,
    prob_has_ns,
    prob_has_remnant
FROM sandbox.nasa_gcn_dev.igwn_gwalert
WHERE significant = 'true';

-- ============================================================================
-- SILVER LAYER - Outras tabelas
-- ============================================================================

-- gcn_classic_text
SELECT 
    event_type, 
    COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_classic_text
GROUP BY event_type
ORDER BY total DESC;

-- gcn_classic_voevent
SELECT 
    event_type, 
    COUNT(*) as total
FROM sandbox.nasa_gcn_dev.gcn_classic_voevent
GROUP BY event_type
ORDER BY total DESC;

-- igwn_gwalert movido para seção RAG acima

-- gcn_heartbeat (monitoramento)
SELECT 
    COUNT(*) as total_heartbeats,
    MIN(kafka_timestamp) as first_heartbeat,
    MAX(kafka_timestamp) as last_heartbeat
FROM sandbox.nasa_gcn_dev.gcn_heartbeat;

-- ============================================================================
-- MÉTRICAS GERAIS - Pipeline Health
-- ============================================================================

-- Resumo de todas as tabelas Silver
SELECT 'gcn_classic_binary' as table_name, COUNT(*) as records FROM sandbox.nasa_gcn_dev.gcn_classic_binary
UNION ALL
SELECT 'gcn_classic_text', COUNT(*) FROM sandbox.nasa_gcn_dev.gcn_classic_text
UNION ALL
SELECT 'gcn_classic_voevent', COUNT(*) FROM sandbox.nasa_gcn_dev.gcn_classic_voevent
UNION ALL
SELECT 'gcn_circulars', COUNT(*) FROM sandbox.nasa_gcn_dev.gcn_circulars
UNION ALL
SELECT 'gcn_notices', COUNT(*) FROM sandbox.nasa_gcn_dev.gcn_notices
UNION ALL
SELECT 'igwn_gwalert', COUNT(*) FROM sandbox.nasa_gcn_dev.igwn_gwalert
UNION ALL
SELECT 'gcn_heartbeat', COUNT(*) FROM sandbox.nasa_gcn_dev.gcn_heartbeat
ORDER BY records DESC;
