# GCN Classic Binary - RAG Optimization

## Visão Geral
A tabela `gcn_classic_binary` processa pacotes binários antigos do GCN. A ingestão Bronze já implementa o parsing de structs binários, mas para o pipeline de RAG, criamos um campo consolidado `document_text`.

## Schema Otimizado

| Campo | Tipo | Origem | Descrição |
|-------|------|--------|-----------|
| `pkt_type_name` | STRING | Parsed | Nome descritivo do pacote (ex: `SK_SUPERNOVA`) |
| `trig_num` | LONG | Parsed | ID do trigger se disponível |
| `burst_datetime` | TIMESTAMP | Parsed | Data calculada a partir do TJD/SOD |
| `burst_ra/dec` | DOUBLE | Parsed | Coordenadas celestes |
| `document_text` | STRING | **Calculado** | Texto consolidado para RAG |

## Estratégia de RAG

Ao contrário de textos livres, estes dados são altamente estruturados. O `document_text` é gerado concatenando os campos-chave em formato legível:

```text
TYPE: SK_SUPERNOVA | TRIG_NUM: 10082 | DATE: 2025-12-31T23:22:43.020000 | RA: 270.8199, DEC: 31.46
```

Isto permite que LLMs compreendam o contexto completo do evento binário sem precisar consultar múltiplas colunas numéricas.

## Validação

Query para verificar a extração:

```sql
SELECT pkt_type_name, burst_datetime, burst_ra_deg, burst_dec_deg, document_text 
FROM sandbox.nasa_gcn_dev.gcn_classic_binary 
LIMIT 5;
```
