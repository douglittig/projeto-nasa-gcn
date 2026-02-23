# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão Geral do Projeto

Pipeline de dados da NASA GCN (Gamma-ray Coordinates Network) usando Databricks Asset Bundles e Lakeflow Declarative Pipelines. Ingere alertas astronômicos em tempo real do stream Kafka da NASA através de uma arquitetura medallion (Bronze -> Silver -> Gold).

**Stack:** Databricks Asset Bundles, Spark Declarative Pipelines (SDP), PySpark, NASA GCN Kafka, gerenciador de pacotes `uv`.

## Protocolo de Trabalho

**IMPORTANTE:** Antes de executar qualquer alteração no código, SEMPRE seguir este protocolo:

### 1. Diálogo Inicial (OBRIGATÓRIO)

```
┌─────────────────────────────────────────────────────────────┐
│  USUÁRIO apresenta o problema/requisito                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  CLAUDE analisa e sugere abordagens                         │
│  - Explica os trade-offs                                    │
│  - Apresenta opções quando aplicável                        │
│  - Identifica riscos ou dependências                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  USUÁRIO dá o OK para prosseguir                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  CLAUDE executa seguindo o dev-workflow                     │
└─────────────────────────────────────────────────────────────┘
```

### 2. Fluxo de Desenvolvimento (dev-workflow)

Após o OK do usuário, seguir SEMPRE este fluxo:

1. `git checkout -b feature/<nome>` - Criar branch
2. Implementar as alterações
3. `pytest tests/ -v` - Rodar testes unitários
4. `./deploy.sh` - Deploy em dev
5. `./deploy.sh run-only` - Executar e validar pipeline em dev
6. `git commit` + `git push` - Commit e push
7. `gh pr create` - Criar PR
8. `gh pr merge --delete-branch` - Merge após aprovação
9. (Opcional) `TARGET=prod ./deploy.sh` - Deploy em prod

**Nunca fazer commit direto na main.** Todas as alterações passam por PR.

Ver skill `/dev-workflow` para detalhes completos.

## Comandos Comuns

```bash
# Instalar dependências
uv sync --dev

# Executar todos os testes
pytest

# Executar teste específico
pytest tests/test_utils.py::test_decode_utf8 -v

# Executar testes com cobertura
pytest --cov=nasa_gcn --cov-report=term-missing

# Lint e correção automática
ruff check src/ tests/ --fix

# Formatar código
ruff format src/ tests/

# Verificação de tipos
mypy src/

# Validar configuração do bundle
databricks bundle validate

# Deploy e execução (carrega credenciais do .env automaticamente)
./deploy.sh run

# Apenas deploy
./deploy.sh

# Executar job sem fazer novo deploy
./deploy.sh run-only

# Deploy para produção
TARGET=prod ./deploy.sh run
```

## Arquitetura

O pipeline usa uma **arquitetura medallion com 3 pipelines** SDP (Spark Declarative Pipelines) separados:

```
NASA GCN Kafka Stream
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PIPELINE BRONZE (bronze_pipeline.py)                       │
│  └─ gcn_raw: Todas as mensagens brutas do Kafka             │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PIPELINE SILVER (silver_pipeline.py)                       │
│  ├─ gcn_circulars      (relatórios escritos por humanos)    │
│  ├─ gcn_notices        (alertas JSON gerados por máquina)   │
│  ├─ gcn_classic_text   (formato texto legado)               │
│  ├─ gcn_classic_voevent (XML VOEvent)                       │
│  ├─ gcn_classic_binary  (pacotes binários parseados)        │
│  ├─ gcn_gwalert        (ondas gravitacionais)               │
│  └─ gcn_heartbeat      (saúde do sistema)                   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PIPELINE GOLD (gold_pipeline.sql)                          │
│  ├─ gcn_events_summary (narrativas de eventos enriquecidas) │
│  └─ gcn_daily_stats    (agregações diárias)                 │
└─────────────────────────────────────────────────────────────┘
```

**Orquestração do Job:** `nasa_gcn.job.yml` executa os pipelines sequencialmente: `validate → bronze → silver → gold → report`

## Restrições Críticas

### Bootstrap de Ambiente (Free Edition)

Os pipelines usam `_bootstrap.py` para resolver imports no Free/Community Edition do Databricks.

**Por quê:** O Free Edition não suporta wheels gerenciados ou repositórios Git com PYTHONPATH automático. O módulo centraliza a manipulação de `sys.path` que seria necessária em cada pipeline.

**Como funciona:**
```python
# No pipeline (bronze_pipeline.py, silver_pipeline.py)
import _bootstrap
_bootstrap.setup_environment(spark)  # spark é global no contexto SDP
```

**Contraste Pedagógico - Free Edition vs Produção:**
- **Free Edition (atual)**: Resolução de path em runtime via `sys.path.insert`
- **Produção Real**: Construir Python Wheel (`.whl`) e declarar no `libraries` do YAML:
  ```yaml
  libraries:
    - whl: /Volumes/catalog/schema/wheels/nasa_gcn-1.0.0-py3-none-any.whl
  ```

Ver `_bootstrap.py` para documentação completa sobre a arquitetura.

### Parser Binário Embutido no Pipeline Silver

`silver_pipeline.py` contém **lógica do parser binário embutida** (linhas 61-196) que deve permanecer sincronizada com `binary_parser.py`.

**Por quê:** O DLT serverless do Databricks não consegue importar módulos customizados de forma confiável nos executores Spark. UDFs requerem que todo código esteja inline.

**Ao modificar o parser binário:**
1. Atualize `binary_parser.py` (fonte da verdade)
2. Sincronize manualmente as mudanças para `silver_pipeline.py:61-196`
3. Mantenha o dict `PACKET_TYPE_NAMES` sincronizado

### Pegadinhas do SDP (Spark Declarative Pipelines)

- `spark` é uma **variável global** no contexto SDP - não é importada, mas está disponível em runtime
- UDFs no SDP não conseguem importar de módulos irmãos nos executores - todo código deve estar inline no arquivo da UDF
- Pipelines Silver/Gold usam `spark.readStream.table()` para ler de tabelas de outros pipelines
- Cada pipeline tem sua própria configuração de catalog/schema via `spark.conf.get()`
- Usar `from pyspark import pipelines as dp` (não `import dlt`)
- **`cluster_by` não é suportado** em `@dp.materialized_view()` no Python API - usar SQL com `CLUSTER BY AUTO` como alternativa
- **Sintaxe `CLUSTER BY AUTO`**: Usar **sem parênteses** - `CLUSTER BY AUTO` (correto) vs `CLUSTER BY (AUTO)` (incorreto - interpreta AUTO como coluna)

### Configurações SDP Implementadas

**Auto-Optimize (Bronze + Silver):**
```python
table_properties={
    "delta.autoOptimize.optimizeWrite": "true",
    "delta.autoOptimize.autoCompact": "true",
}
```

**Data Quality Expectations (Silver):**
```python
@dp.expect_or_drop("valid_id", "id IS NOT NULL")
```
- `gcn_circulars`: valid_circular_id, valid_event_id
- `gcn_notices`: valid_notice_id
- `gcn_classic_binary`: valid_parse (parse_error IS NULL)
- `gcn_gwalert`: valid_event_id

**Change Data Feed (Gold):**
```python
table_properties={"delta.enableChangeDataFeed": "true"}
```

### Gerenciamento de Credenciais

O Databricks Community Edition **não** suporta a API de Secrets. Credenciais são armazenadas em `.env` (ignorado pelo git):

```bash
# Preferido: Codificado em Base64
GCN_CLIENT_ID_B64=...
GCN_CLIENT_SECRET_B64=...

# Alternativa: Texto puro
GCN_CLIENT_ID=...
GCN_CLIENT_SECRET=...
```

Use `python scripts/encode_credentials.py` para codificar credenciais. O `deploy.sh` detecta e decodifica Base64 automaticamente.

### Schema do Unity Catalog

- Dev: `sandbox.bronze`, `sandbox.silver`, `sandbox.gold`
- Prod: `nasa_gcn.bronze`, `nasa_gcn.silver`, `nasa_gcn.gold`

## Fluxo de Desenvolvimento

### Adicionando Novo Tópico GCN

1. Adicione o schema em `src/nasa_gcn/schemas.py` (se necessário)
2. Adicione definição `@dp.table` em `src/nasa_gcn/pipelines/silver_pipeline.py`
3. Atualize o padrão de filtro para corresponder ao novo tópico

### Adicionando Nova Agregação Gold

1. Adicione nova `MATERIALIZED VIEW` em `src/nasa_gcn/pipelines/gold_pipeline.sql`
2. Use `CLUSTER BY AUTO` para otimização automática de layout
3. Referencie tabelas Silver via `${silver_catalog}.${silver_schema}.table_name`

```sql
CREATE OR REPLACE MATERIALIZED VIEW nova_agregacao
COMMENT 'Descrição da agregação'
CLUSTER BY AUTO
AS
SELECT ...
FROM `${silver_catalog}`.`${silver_schema}`.tabela_silver;
```

### Problemas Conhecidos

- **Teste falhando:** `tests/main_test.py::test_get_logger` - asserção de handler do logger falha
- **Contagens lentas:** `main.py` usa `.count()` em tabelas grandes (3M+ linhas) - considerar event log do SDP
- **Exceções genéricas:** `config.py:45-46` e `binary_parser.py:369-372` engolem erros silenciosamente

Veja `TECHNICAL_DEBT.md` para rastreamento completo de issues e planejamento de sprints.

## Arquivos Principais

| Arquivo | Propósito |
|---------|-----------|
| `src/nasa_gcn/pipelines/_bootstrap.py` | Setup de ambiente (Free Edition workaround) |
| `src/nasa_gcn/pipelines/bronze_pipeline.py` | Bronze: Ingestão Kafka para `gcn_raw` |
| `src/nasa_gcn/pipelines/silver_pipeline.py` | Silver: Parsing por tópico (7 tabelas) |
| `src/nasa_gcn/pipelines/gold_pipeline.sql` | Gold: Agregações e enriquecimentos (SQL com CLUSTER BY AUTO) |
| `src/nasa_gcn/binary_parser.py` | Decodificador de pacotes binários GCN (fonte da verdade) |
| `src/nasa_gcn/schemas.py` | Schemas PySpark para todos os tópicos GCN |
| `src/nasa_gcn/config.py` | Configuração do Kafka e credenciais |
| `src/nasa_gcn/main.py` | Relatório de status e métricas do pipeline |
| `deploy.sh` | Script de deploy com tratamento de credenciais |
| `databricks.yml` | Configuração do asset bundle |
| `resources/nasa_gcn.job.yml` | Orquestração do job (DAG de pipelines) |
| `resources/pipelines/*.yml` | Configurações individuais dos pipelines |

## Documentação

- `docs/GCN_*_RAG.md` - Documentação de contexto RAG para cada tópico GCN
- `docs/GOLD_LAYER.md` - Lógica de enriquecimento da camada Gold
- `TECHNICAL_DEBT.md` - Rastreamento de issues e planejamento de sprints
