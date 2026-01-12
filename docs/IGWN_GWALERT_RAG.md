# Otimização RAG: Tabela `igwn_gwalert`

Este documento descreve as otimizações realizadas na tabela `igwn_gwalert` (Silver Layer) para facilitar a indexação e recuperação via RAG (Retrieval-Augmented Generation).

## Objetivo
Transformar os alertas de ondas gravitacionais (IGWN) brutos (JSON aninhado) em um formato tabular enriquecido, extraindo probabilidades de classificação, propriedades do evento e instrumentos, além de gerar um campo de texto (`document_text`) consolidado para busca semântica.

## Schema da Tabela Silver

A tabela `igwn_gwalert` processada contém os seguintes campos principais:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `gwalert_json` | STRING | JSON original completo decodificado. |
| `superevent_id` | STRING | ID do evento (ex: `MS251221j` ou `S190425z`). |
| `alert_type` | STRING | Tipo de alerta (`INITIAL`, `UPDATE`, `RETRACTION`). |
| `time_created` | STRING | Timestamp de criação do alerta. |
| `group` | STRING | Grupo de análise (ex: `CBC`, `Burst`). |
| `pipeline` | STRING | Pipeline de detecção (ex: `gstlal`, `cwb`). |
| `instruments` | STRING | Lista limpa de interferômetros (ex: `H1,L1,V1`). |
| `far` | STRING | False Alarm Rate (taxa de falso alarme). |
| `significant` | STRING | Booleano indicando se o evento é significativo. |
| `gracedb_url` | STRING | Link para o evento no GraceDB. |

### Campos de Classificação (Probabilidades)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `prob_bns` | STRING | Probabilidade de ser Binary Neutron Star. |
| `prob_nsbh` | STRING | Probabilidade de ser Neutron Star - Black Hole. |
| `prob_bbh` | STRING | Probabilidade de ser Binary Black Hole. |
| `prob_terrestrial` | STRING | Probabilidade de ser ruído terrestre. |

### Campos de Propriedades
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `prob_has_ns` | STRING | Probabilidade de conter estrela de nêutrons. |
| `prob_has_remnant` | STRING | Probabilidade de ter remanescente (matéria pós-fusão). |

## Campo `document_text` para RAG

O campo `document_text` consolida as informações mais críticas em uma única string formatada, pronta para embedding:

**Formato:**
```text
ID: [superevent_id] | TYPE: [alert_type] | GROUP: [group] | PIPELINE: [pipeline] | INSTRUMENTS: [instruments] | SIGNIFICANT: [significant] | URL: [gracedb_url]
```

**Exemplo Real:**
```text
ID: S190425z | TYPE: INITIAL | GROUP: CBC | PIPELINE: gstlal | INSTRUMENTS: L1,V1 | SIGNIFICANT: true | URL: https://gracedb.ligo.org/superevents/S190425z/view/
```

> **Nota:** As probabilidades numéricas (BNS, BBH, etc.) foram mantidas como colunas separadas para permitir filtros precisos (ex: `WHERE prob_bns > 0.9`), mas não foram incluídas no texto principal do RAG para evitar poluição visual e alucinações com números flutuantes complexos. O RAG pode recuperar o registro pelo ID ou instrumentos e o LLM pode consultar as colunas de probabilidade se necessário, ou podemos adicionar um resumo textual (ex: "High BNS probability") futuramente.

## Transformações Implementadas

1.  **Limpeza de Instrumentos:**
    *   Original: `["H1","L1"]` (JSON array string)
    *   Transformado: `H1,L1` (String limpa via `regexp_replace`).
2.  **Achatamento de JSON:**
    *   Campos aninhados como `event.classification.BNS` foram promovidos para colunas de nível superior (`prob_bns`).
3.  **Filtragem de Nulos:**
    *   O `document_text` é construído com `concat_ws`, que ignora automaticamente partes nulas, garantindo que o texto final seja limpo mesmo em alertas incompletos.

## Queries de Validação

Verificar a extração dos campos e a formatação do texto:

```sql
SELECT 
    superevent_id, 
    alert_type, 
    instruments, 
    prob_bns, 
    document_text 
FROM igwn_gwalert 
LIMIT 10;
```
