# GCN Classic VoEvent - RAG Optimization

## Visão Geral
A tabela `gcn_classic_voevent` armazena alertas no formato padronizado XML VoEvent. Otimizamos esta tabela para RAG extraindo campos-chave diretamente do XML e gerando um texto consolidado para embedding.

## Schema Otimizado

| Campo | Tipo | Origem (XPath) | Descrição |
|-------|------|----------------|-----------|
| `voevent_xml` | STRING | Value | XML completo decodificado |
| `ivorn` | STRING | `//VOEvent/@ivorn` | Identificador único do evento |
| `role` | STRING | `//VOEvent/@role` | Papel do evento (observation, prediction, test, utility) |
| `date` | TIMESTAMP | `//Who/Date` | Data do evento |
| `concept` | STRING | `//Why/Inference/Concept` | Classificação do evento (ex: `UVOT emergency`) |
| `document_text` | STRING | **Calculado** | Texto consolidado para RAG |

## Estratégia de Extração (XPath)

Utilizamos expressões XPath suportadas pelo Apache Spark (`xpath_string`) para navegar na estrutura XML:

```sql
expr("xpath_string(xml_str, '/*[local-name()=\"VOEvent\"]/@ivorn')")
```

Nota: Usamos `local-name()` para evitar complexidade com namespaces XML (`voe`, `xsi`).

## Estrutura do `document_text`

O campo `document_text` concatena os metadados principais para indexação semântica:

```text
ID: ivo://nasa.gsfc.gcn/SWIFT#UVOT_Emergency_... | ROLE: utility | DATE: 2026-01-01T02:21:16 | CONCEPT: UVOT emergency. | DESCRIPTION: Swift Satellite, UVOT Instrument
```

## Validação

Query para verificar a extração:

```sql
SELECT ivorn, role, date, concept, document_text 
FROM sandbox.nasa_gcn_dev.gcn_classic_voevent 
LIMIT 5;
```
