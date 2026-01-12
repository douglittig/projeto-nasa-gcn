# GCN Circulars - Schema para RAG

Documentação da tabela `gcn_circulars` otimizada para pipelines de Retrieval-Augmented Generation (RAG).

---

## Schema da Tabela

### Campos Extraídos do JSON

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `circular_id` | INT | ID único do circular GCN | `43046` |
| `event_id` | STRING | Identificador do evento astronômico | `GRB 251208B` |
| `subject` | STRING | Título/assunto do circular | `GRB 251208B: Fermi GBM Observation` |
| `body` | STRING | Conteúdo completo do relatório | Texto do astrônomo |
| `submitter` | STRING | Autor completo com email | `A. von Kienlin at MPE <azk@mpe.mpg.de>` |
| `submitter_name` | STRING | Nome do autor (extraído, trimmed) | `Andreas von Kienlin at MPE` |
| `submitter_email` | STRING | Email do autor (extraído) | `azk@mpe.mpg.de` |
| `submitted_how` | STRING | Método de submissão | `email` ou `web` |
| `created_on` | TIMESTAMP | Data/hora de criação | `2025-12-09 11:52:05` |

### Campos Derivados para RAG

| Campo | Tipo | Descrição | Uso RAG |
|-------|------|-----------|---------|
| `event_type` | STRING | Tipo extraído do eventId | Filtro por categoria (GRB, GW, SN) |
| `word_count` | INT | Número de palavras no body | Filtrar docs muito curtos |
| `char_count` | INT | Número de caracteres no body | Estimativa de tokens (~4 chars/token) |
| `document_text` | STRING | Texto formatado para embedding | **Input principal para vetorização** |

### Metadados Técnicos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `circular_json` | STRING | JSON original completo |
| `topic` | STRING | Tópico Kafka (`gcn.circulars`) |
| `kafka_timestamp` | TIMESTAMP | Timestamp da mensagem no Kafka |
| `ingestion_timestamp` | TIMESTAMP | Quando ingerido no Databricks |
| `silver_processed_timestamp` | TIMESTAMP | Quando processado na Silver |
| `silver_processed_date` | DATE | Data de processamento |

---

## Formato do `document_text`

O campo `document_text` é formatado especificamente para embedding:

```
SUBJECT: GRB 251208B: Fermi GBM Observation
EVENT: GRB 251208B
AUTHOR: Andreas von Kienlin at MPE
---
[conteúdo completo do body]
```

---

## Queries de Exemplo

### Listar circulars por evento
```sql
SELECT circular_id, subject, submitter_name, created_on
FROM sandbox.nasa_gcn_dev.gcn_circulars
WHERE event_id = 'GRB 251208B'
ORDER BY created_on;
```

### Filtrar por tipo de evento
```sql
SELECT event_type, COUNT(*) as total, AVG(word_count) as avg_words
FROM sandbox.nasa_gcn_dev.gcn_circulars
GROUP BY event_type
ORDER BY total DESC;
```

### Buscar circulars para RAG (filtro por tamanho)
```sql
SELECT circular_id, document_text, word_count, char_count
FROM sandbox.nasa_gcn_dev.gcn_circulars
WHERE word_count > 50 AND event_type = 'GRB'
ORDER BY created_on DESC
LIMIT 100;
```

### Estimar tokens (~4 chars por token)
```sql
SELECT circular_id, subject, 
       word_count, char_count,
       ROUND(char_count / 4) as estimated_tokens
FROM sandbox.nasa_gcn_dev.gcn_circulars
ORDER BY char_count DESC
LIMIT 10;
```

---

## Referências

- [GCN Circulars Archive](https://gcn.gsfc.nasa.gov/gcn3_archive.html)
- [GCN JSON Schema](https://gcn.nasa.gov/schema/v6.0.0/gcn/circulars.schema.json)
