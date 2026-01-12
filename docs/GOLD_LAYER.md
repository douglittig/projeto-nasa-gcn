# Gold Layer - GCN Events Summarized

## Overview
A tabela `gcn_events_summarized` (Camada Gold) é a "Joia da Coroa" do pipeline. Ela não apenas limpa os dados, mas **agrega** e **contextualiza** informações de múltiplas fontes (Notices e Circulars) em torno de um único evento astronômico.

## Objetivo
Fornecer um **Documento Unificado** para cada evento (ex: `GRB 230101A` ou `S190425z`), contendo:
1.  **Narrativa Científica**: Consolidação de todos os relatórios humanos (Circulars) sobre o evento.
2.  **Contexto Factual**: Dados duros (Timestamp, Classificação, Instrumentos) vindos dos alertas automáticos (Notices/GW Alerts).

## Schema

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `event_id` | STRING | Identificador único (ex: `GRB 230101A`, `S190425z`) |
| `event_time` | TIMESTAMP | Data/hora do evento (ou da primeira circular) |
| `circular_count` | LONG | Quantidade de circulares associadas |
| `scientific_narrative` | STRING | Texto concatenado de todas as circulares (Corpo do RAG) |
| `alert_type` | STRING | Tipo do alerta (ex: `PRELIMINARY`, `Initial`) |
| `alert_context` | STRING | Dados do Notice formatados para RAG (Probabilidades, RA/Dec) |
| `gold_processed_timestamp` | TIMESTAMP | Data de processamento |

## Estratégia de Construção

1.  **Agregação de Circulares**: Agrupa `gcn_circulars` por `event_id`. O campo `scientific_narrative` é gerado concatenando o `document_text` de todas as mensagens, separadas por `---`.
2.  **Enriquecimento com GW Alerts**: Faz um *Left Join* com `igwn_gwalert` usando `superevent_id` (mapeado para `event_id`). Isso traz dados precisos como classificação de ondas gravitacionais (BNS, BBH).
