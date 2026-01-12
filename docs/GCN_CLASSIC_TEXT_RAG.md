# GCN Classic Text - RAG Optimization

## Visão Geral
A tabela `gcn_classic_text` armazena alertas recebidos no formato legado de texto puro (Classic GCN). Para otimizar o uso em RAG (Retrieval-Augmented Generation), aplicamos extrações via Regex para estruturar metadados importantes sem perder o conteúdo original.

## Schema Otimizado

| Campo | Tipo | Origem | Descrição |
|-------|------|--------|-----------|
| `message_key` | STRING | Kafka | Chave da mensagem kafka |
| `message_text` | STRING | Kafka Value | Texto completo do alerta decodificado |
| `event_type` | STRING | Topic | Extraído do tópico (ex: `SWIFT_UVOT_EMERGENCY`) |
| `title` | STRING | **Regex** | Título extraído do corpo (ex: `GCN/SWIFT NOTICE`) |
| `notice_type` | STRING | **Regex** | Tipo de notificação (ex: `Swift-UVOT Emergency`) |
| `notice_date` | STRING | **Regex** | Data extraída do corpo (ex: `Thu 01 Jan 26 02:21:16 UT`) |
| `document_text` | STRING | **Calculado** | Cópia do `message_text` para padronização de RAG |

## Estratégia de RAG

### 1. Extração de Metadados
Como os alertas "Classic" não possuem estrutura JSON, utilizamos Expressões Regulares (Regex) para extrair campos-chave diretamente do corpo do texto (`text_decoded`):

- **Título**: `TITLE:\s+(.*?)(?=\n)`
- **Data**: `NOTICE_DATE:\s+(.*?)(?=\n)`
- **Tipo**: `NOTICE_TYPE:\s+(.*?)(?=\n)`

Isso permite filtros mais eficientes no Vector Database (ex: filtrar apenas alertas de 2026 ou de um tipo específico).

### 2. Document Text
Para estes alertas, o próprio conteúdo textual já é otimizado para leitura humana e contem pares `CHAVE: VALOR`. Portanto, o campo `document_text` é uma réplica direta do `message_text`, garantindo compatibilidade com o pipeline de embedding que espera essa coluna.

## Exemplo de Dados

```text
TITLE:           GCN/SWIFT NOTICE
NOTICE_DATE:     Thu 01 Jan 26 02:21:16 UT
NOTICE_TYPE:     Swift-UVOT Emergency
...
COMMENTS:        SWIFT UVOT Emergency.
```

**Campos Extraídos:**
- `title`: "GCN/SWIFT NOTICE"
- `notice_date`: "Thu 01 Jan 26 02:21:16 UT"
- `notice_type`: "Swift-UVOT Emergency"

## Validação

Queries para validar a extração:

```sql
SELECT title, notice_type, notice_date, document_text 
FROM sandbox.nasa_gcn_dev.gcn_classic_text 
WHERE title IS NOT NULL 
LIMIT 5;
```
