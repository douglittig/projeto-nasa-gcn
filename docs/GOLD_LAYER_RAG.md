# Gold Layer - GCN Events Summarized

## Overview
A tabela `gcn_events_summarized` (Camada Gold) é a "Joia da Coroa" para o sistema de RAG. Ela não apenas limpa os dados, mas **agrega** e **contextualiza** informações de múltiplas fontes (Notices e Circulars) em torno de um único evento astronômico.

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

## Uso no RAG

Este é o alvo principal para **Vetorização**.
- **Embedding**: Gerar vetor apenas para o campo `scientific_narrative` (ou uma combinação de `alert_context` + `narrative`).
- **Retrieval**: Ao buscar "contrapartida óptica S190425z", o RAG recuperará este registro único, que contém toda a discussão da comunidade, em vez de retornar 50 fragmentos de circulares sem ordem.

## Pipeline de Vetorização

O script `src/vectorization_job.py` é responsável por transformar esta camada Gold em vetores para busca semântica.

1.  **Leitura**: Lê `gcn_events_summarized` (filtrando narrativas nulas).
2.  **Embedding**: Utiliza o modelo `BAAI/bge-m3` (via UDF Pandas com `sentence-transformers`) para gerar vectors de alta dimensão a partir da `scientific_narrative`.
3.  **Output**: Salva em `gcn_embeddings` (Delta Table preparada para Vector Search).

## Agente RAG

O protótipo `src/rag_agent.py` demonstra como consumir esses vetores:

1.  **Recuperação (Retrieval)**: O agente busca eventos semanticamente similares à pergunta do usuário (ex: "quais eventos têm contrapartida óptica?").
2.  **Geração (Generation)**: O LLM recebe o **Contexto Rico** (Narrativa Completa + Dados de Alerta) e gera uma resposta precisa e citável.
