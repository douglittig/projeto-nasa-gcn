# Débito Técnico & Melhorias

## Matriz de Priorização (Criticidade vs. Complexidade)

| ID | Item | Criticidade | Complexidade | Impacto | Sprint |
|:--:|:-----|:-----------:|:----------:|:-------|:------:|
| **1** | **Duplicação do Parser Binário** | 🔴 Alta | 🟠 Média | Custo de manutenção, risco de inconsistência | 3 |
| **2** | **Teste Falhando** | 🔴 Alta | 🟢 Baixa | CI quebrado, confiabilidade dos testes | 1 |
| **3** | **Cobertura de Testes** | 🟠 Média | 🔴 Alta | Risco de regressão, sem testes SDP/config | 2 |
| **4** | **Tratamento Genérico de Erros** | 🟠 Média | 🟡 Média | Falhas silenciosas, dificuldade de debug | 2 |
| **5** | **Implementação CI/CD** | 🟠 Média | 🟡 Média | Processo manual, erro humano | 3 |
| **6** | **Integração Vector Store** | 🟠 Média | 🔴 Alta | Gargalo de escalabilidade RAG | Backlog |
| ~~**7**~~ | ~~**Configuração de Streaming**~~ | ✅ | ✅ | ~~N/A - SDP gerencia checkpoints~~ | ✅ |
| **8** | **Valores Hardcoded** | 🟡 Baixa | 🟢 Baixa | Dificuldade de teste/staging | 2 |
| ~~**9**~~ | ~~**Performance - Queries de Count**~~ | ✅ | ✅ | ~~Lento em tabelas grandes (3M+ linhas)~~ | ✅ |
| **10** | **Limites de Versão de Dependências** | 🟡 Baixa | 🟢 Baixa | Risco de breaking changes | 1 |
| ~~**11**~~ | ~~**SDP Auto-Optimize**~~ | ✅ | ✅ | ~~Small files no Bronze~~ | ✅ |
| ~~**12**~~ | ~~**Expectations de Qualidade de Dados**~~ | ✅ | ✅ | ~~Dados ruins silenciosos no Silver~~ | ✅ |
| **13** | **Auto-geração de Documentação** | 🟡 Baixa | 🟡 Média | Overhead de manutenção manual | Backlog |
| ~~**14**~~ | ~~**Auto-Optimize no Silver**~~ | ✅ | ✅ | ~~Small files nas tabelas Silver~~ | ✅ |

---

## Planejamento de Sprints

### 🏃 Sprint 1: Vitórias Rápidas (1 semana)
Foco: Baixo esforço, alto impacto

- **#2** - Corrigir teste falhando (test_get_logger)
- ~~**#9** - Otimizar queries de count~~ ✅
- **#10** - Adicionar limites superiores de dependências
- ~~**#11** - Adicionar table properties Auto-Optimize no Bronze~~ ✅

### 🏃 Sprint 2: Qualidade & Confiabilidade (2 semanas)
Foco: Testes e tratamento de erros

- **#3** - Aumentar cobertura de testes (pipelines SDP, config)
- **#4** - Melhorar tratamento de erros
- **#8** - Tornar valores hardcoded configuráveis
- ~~**#12** - Adicionar Data Quality Expectations nas tabelas Silver~~ ✅

### 🏃 Sprint 3: Arquitetura & DevOps (3 semanas)
Foco: Melhorias estruturais

- **#1** - Resolver duplicação do parser binário
- **#5** - Implementar CI/CD
- ~~**#7** - Configurar streaming seguro~~ ✅ (N/A - SDP gerencia checkpoints)

### 📦 Backlog: Melhorias Futuras
- **#6** - Migração para Vector Store em produção
- **#13** - Auto-geração de documentação
- ~~**#14** - Auto-Optimize nas tabelas Silver~~ ✅
- ~~Change Data Feed para CDC downstream~~ ✅ (implementado em Gold)
- ~~CLUSTER BY AUTO para camada Gold~~ ✅ (convertido para SQL)

---

## Itens Pendentes (Detalhes)

### 1. Duplicação do Parser Binário 🔴
- **Problema**: Lógica do parser binário duplicada em `binary_parser.py` e `silver_pipeline.py`
  - `binary_parser.py:203-374` (original, fonte da verdade)
  - `silver_pipeline.py:61-196` (cópia para compatibilidade com UDF)
  - Dict `PACKET_TYPE_NAMES` (196 entradas) duplicado
- **Causa Raiz**: Ambiente serverless do SDP no Databricks não consegue importar módulos irmãos nos executores de UDF
- **Impacto**:
  - Correções de bugs devem ser aplicadas em dois lugares
  - Risco de inconsistência
  - ~300 linhas de código duplicado
- **Opções de Solução**:
  - **Opção A (Atual)**: Manter duplicação, aceitar custo de manutenção
  - **Opção B**: Script de injeção de código em tempo de build
  - **Opção C**: Spark UDF com `.addPyFile()` (pode não funcionar em serverless)
- **Recomendação**: Implementar injeção em tempo de build (Opção B)
  - Criar `scripts/build_pipeline.py` que injeta código do parser
  - Executar antes do deploy: `python scripts/build_pipeline.py && databricks bundle deploy`
  - Mantém fonte única da verdade
- **Esforço**: 4-6 horas

### 2. Teste Falhando 🔴
- **Problema**: `tests/main_test.py::test_get_logger` falha
- **Localização**: `tests/main_test.py:test_get_logger`
- **Erro**: `assert len(logger.handlers) >= 1` falha (len é 0)
- **Causa Raiz**: `get_logger()` define level mas não adiciona handler
- **Impacto**: CI quebrado, prejudica confiança nos testes
- **Solução**: Adicionar StreamHandler em `get_logger()` ou ajustar expectativa do teste
- **Esforço**: 15 minutos

### 3. Cobertura de Testes 🟠
- **Problema**: Cobertura de testes insuficiente (~7.3%)
  - Zero testes para pipelines SDP (`bronze_pipeline.py`, `silver_pipeline.py`, `gold_pipeline.py`)
  - Zero testes para `config.py` (lógica de credenciais)
  - Apenas funções utilitárias testadas em `main.py`
- **Impacto**: Alto risco de regressão, especialmente em transformações de pipeline
- **Solução**:
  - Adicionar testes de pipeline SDP com mocks de Spark
  - Adicionar testes de config com mocking de variáveis de ambiente
  - Testar funções principais (get_pipeline_stats, get_dlt_metrics)
- **Meta de Cobertura**: >60%
- **Esforço**: 2-3 dias

### 4. Tratamento Genérico de Erros 🟠
- **Problema**: Múltiplas instâncias de tratamento de exceção muito amplo
  - `config.py:45-46`: `except Exception: pass` (engole todos os erros)
  - `main.py:136-137`: Exceção genérica armazenada como string
  - `binary_parser.py:369-372`: Captura todas as exceções
- **Impacto**: Falhas silenciosas, dificuldade de debugging
- **Solução**:
  - Usar tipos de exceção específicos
  - Adicionar logging adequado no mínimo
  - Considerar padrões Result/Option para o parser
- **Exemplos**:
  ```python
  # Ruim
  try:
      result = operacao_arriscada()
  except Exception:
      pass

  # Bom
  try:
      result = operacao_arriscada()
  except ConnectionError as e:
      logger.error(f"Conexão falhou: {e}")
      raise
  except ValueError as e:
      logger.warning(f"Valor inválido: {e}")
      return valor_padrao
  ```
- **Esforço**: 4-6 horas

### 5. Implementação CI/CD 🟠
- **Problema**: Deploy é manual via `deploy.sh`
- **Impacto**: Risco de erro humano, sem testes automatizados em PR
- **Solução**: Workflow GitHub Actions
  ```yaml
  # .github/workflows/ci.yml
  - Executar testes (pytest)
  - Executar linting (ruff)
  - Executar verificação de tipos (mypy)
  - Deploy em dev ao fazer merge de PR
  - Deploy em prod ao fazer merge na main
  ```
- **Esforço**: 1 dia

### 6. Integração Vector Store em Produção 🟠
- **Problema**: RAG usa Delta Table básica (`gcn_embeddings`)
- **Impacto**: Gargalo de escalabilidade, gerenciamento manual de índice
- **Solução**: Migrar para Databricks Vector Search
  - Indexação gerenciada
  - Recuperação de baixa latência
  - Auto-scaling
- **Esforço**: 1-2 semanas
- **Nota**: Requer workspace Databricks pago

### 8. Valores Hardcoded 🟡
- **Problema**: Valores de configuração hardcoded em `config.py`
  - Broker Kafka: `kafka.gcn.nasa.gov:9092`
  - Endpoint OAuth: `https://auth.gcn.nasa.gov/oauth2/token`
  - Padrões de tópicos: Linhas 71-78
- **Impacto**: Difícil de testar, não pode usar servidores de staging/mock
- **Solução**: Mover para variáveis de configuração
  ```python
  KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER", "kafka.gcn.nasa.gov:9092")
  ```
- **Esforço**: 1-2 horas

### 10. Limites de Versão de Dependências 🟡
- **Problema**: Dependências sem limites superiores
  - `python-dotenv>=1.0.0` (sem limite superior)
  - `mypy`, `ruff` sem versão fixa
- **Impacto**: Risco de breaking changes em versões futuras
- **Solução**: Usar operador `~=`
  ```toml
  python-dotenv = "~=1.0"  # >=1.0, <2.0
  ```
- **Esforço**: 15 minutos

### 13. Auto-geração de Documentação 🟡
- **Problema**: Docs escritos manualmente em `docs/*.md`
- **Solução**: Auto-gerar a partir de metadados do SDP
  - Documentação de schema a partir de metadados das tabelas
  - Linhagem de dados a partir do DAG do SDP
- **Esforço**: 1 semana
- **Ferramentas**: Considerar scripts customizados, event log do SDP

---

## Itens Resolvidos (✅ Concluídos)

### Configuração de Streaming - Item Removido (2026-02-23)
- **Ação**: Item #7 removido da matriz de priorização
- **Motivo**: Não aplicável no contexto de Spark Declarative Pipelines (SDP)
  - **Checkpoints**: Gerenciados automaticamente pelo SDP - transparente para o desenvolvedor
  - **failOnDataLoss: "false"**: Aceitável em ambiente Free Edition/treinamento - se os offsets do Kafka expirarem, continua do `startingOffsets` configurado
- **Nota**: O item foi criado antes da migração para SDP, quando checkpoints precisavam ser configurados manualmente
- **Status**: ✅ Removido (N/A)

### Performance - Queries de Count (2026-03-11)
- **Ação**: Substituído `.count()` por `DESCRIBE DETAIL` em `main.py`
- **Mudança**: `get_table_count()` agora usa `spark.sql(f"DESCRIBE DETAIL {full_name}").collect()[0]["numRows"]`
- **Benefício**: Leitura de metadados Delta sem full table scan — ordens de magnitude mais rápido em tabelas com 3M+ linhas
- **Status**: ✅ Implementado & Deployado

### Módulo Bootstrap para Free Edition (2026-02-23)
- **Ação**: Extraído código de setup de path duplicado para módulo centralizado `_bootstrap.py`
- **Problema Original**: Bloco de `sys.path.insert` de ~25 linhas duplicado em cada pipeline, misturando infraestrutura com lógica de negócio
- **Mudanças**:
  - Criado `_bootstrap.py` com função `setup_environment(spark)` e documentação pedagógica
  - Refatorado `bronze_pipeline.py`: removidas 23 linhas de boilerplate
  - Refatorado `silver_pipeline.py`: removidas 25 linhas de boilerplate
  - Adicionada documentação em CLAUDE.md sobre contraste Free Edition vs Produção
- **Arquivos Modificados**:
  - `src/nasa_gcn/pipelines/_bootstrap.py` (novo)
  - `src/nasa_gcn/pipelines/bronze_pipeline.py`
  - `src/nasa_gcn/pipelines/silver_pipeline.py`
- **Benefício**: Separação de concerns, código DRY, valor pedagógico para treinamento
- **Status**: ✅ Implementado & Deployado

### CLUSTER BY AUTO no Gold via SQL (2026-02-22)
- **Ação**: Convertido Gold pipeline de Python para SQL para habilitar Liquid Clustering automático em materialized views
- **Mudanças**:
  - Criado `gold_pipeline.sql` com `CLUSTER BY AUTO` nas materialized views
  - Atualizado `gold.pipeline.yml` para usar arquivo SQL
  - Mantido `gold_pipeline.py` como referência (pode ser removido)
- **Arquivos Modificados**:
  - `src/nasa_gcn/pipelines/gold_pipeline.sql` (novo)
  - `resources/pipelines/gold.pipeline.yml`
- **Nota Técnica**: A sintaxe correta é `CLUSTER BY AUTO` (sem parênteses). Com parênteses `CLUSTER BY (AUTO)` o parser interpreta "AUTO" como nome de coluna.
- **Benefício**: Databricks otimiza automaticamente as chaves de clustering baseado nos padrões de query
- **Status**: ✅ Implementado & Deployado

### Auto-Optimize no Silver (2026-02-21)
- **Ação**: Adicionadas table properties `delta.autoOptimize` em todas as 7 tabelas Silver
- **Mudanças**:
  - Adicionado `delta.autoOptimize.optimizeWrite: "true"` - otimiza tamanho dos arquivos durante escrita
  - Adicionado `delta.autoOptimize.autoCompact: "true"` - compacta small files automaticamente
- **Tabelas Modificadas**: gcn_circulars, gcn_notices, gcn_classic_text, gcn_classic_voevent, gcn_classic_binary, gcn_gwalert, gcn_heartbeat
- **Arquivo Modificado**: `silver_pipeline.py`
- **Benefício**: Reduz acúmulo de small files em todas as tabelas de streaming Silver
- **Status**: ✅ Implementado & Deployado

### Data Quality Expectations no Silver (2026-02-21)
- **Ação**: Adicionados decoradores `@dp.expect_or_drop` nas tabelas Silver para validação de dados
- **Mudanças**:
  - `gcn_circulars`: valid_circular_id, valid_event_id
  - `gcn_notices`: valid_notice_id
  - `gcn_classic_binary`: valid_parse (parse_error IS NULL)
  - `gcn_gwalert`: valid_event_id
- **Arquivo Modificado**: `silver_pipeline.py`
- **Benefício**: Dados inválidos são descartados automaticamente, garantindo qualidade no Silver
- **Status**: ✅ Implementado & Deployado

### Change Data Feed no Gold (2026-02-21)
- **Ação**: Habilitado Change Data Feed nas materialized views Gold para suporte a CDC downstream
- **Mudanças**:
  - Adicionado `delta.enableChangeDataFeed: "true"` em `gcn_events_summary`
  - Adicionado `delta.enableChangeDataFeed: "true"` em `gcn_daily_stats`
- **Arquivo Modificado**: `gold_pipeline.py`
- **Benefício**: Permite rastreamento eficiente de mudanças para consumidores downstream
- **Status**: ✅ Implementado & Deployado

### SDP Auto-Optimize no Bronze (2026-02-21)
- **Ação**: Adicionadas table properties `delta.autoOptimize` na tabela Bronze `gcn_raw`
- **Mudanças**:
  - Adicionado `delta.autoOptimize.optimizeWrite: "true"` - otimiza tamanho dos arquivos durante escrita
  - Adicionado `delta.autoOptimize.autoCompact: "true"` - compacta small files automaticamente
- **Arquivo Modificado**: `bronze_pipeline.py:48-56`
- **Benefício**: Reduz acúmulo de small files da ingestão Kafka de alta frequência
- **Status**: ✅ Implementado & Deployado

### Migração DLT para SDP (2026-02-21)
- **Ação**: Migrou todos os pipelines de Delta Live Tables (DLT) para Spark Declarative Pipelines (SDP)
- **Mudanças**:
  - Alterado `import dlt` para `from pyspark import pipelines as dp`
  - Atualizados decoradores de `@dlt.table` para `@dp.table` e `@dp.materialized_view`
  - Alterado `dlt.read_stream()` para `spark.readStream.table()`
  - Adicionado Liquid Clustering (`cluster_by`) em todas as tabelas
  - Adicionado `per-file-ignores` no `pyproject.toml` para variável global `spark`
  - Removido `dlt_pipeline.py` legado (arquivo monolítico de 341 linhas)
- **Arquivos Modificados**:
  - `bronze_pipeline.py` - Ingestão Kafka
  - `silver_pipeline.py` - Parsing por tópico (7 tabelas)
  - `gold_pipeline.py` - Agregações (2 materialized views)
  - `pyproject.toml` - Configuração Ruff
- **Status**: ✅ Implementado & Deployado

### Erros de Linting/MyPy Corrigidos (2026-02-21)
- **Ação**: Corrigidos erros F821 para variável `spark` indefinida
- **Solução**: Adicionado per-file-ignores no pyproject.toml para arquivos de pipeline
- **Status**: ✅ Implementado

### Boilerplate DLT Eliminado (2026-02-21)
- **Ação**: Removido `dlt_pipeline.py` monolítico durante migração SDP
- **Nota**: Cada camada agora tem seu próprio arquivo de pipeline focado
- **Status**: ✅ Resolvido por mudança de arquitetura

### Codificação Base64 de Credenciais (2026-01-30)
- **Ação**: Implementada codificação Base64 para credenciais NASA GCN para fornecer ofuscação básica no Databricks Community Edition.
- **Mudanças**:
  - Adicionada função `_decode_base64_credential()` em `config.py`
  - Atualizado `deploy.sh` para auto-detectar e decodificar credenciais Base64
  - Criado script auxiliar `scripts/encode_credentials.py`
  - Adicionada suíte de testes `scripts/test_base64_credentials.py`
  - Documentação de segurança abrangente no README
- **Status**: ✅ Implementado & Testado

### Cobertura de Type Hints
- **Ação**: Completadas anotações de tipo em `main.py` e `utils.py`. Adicionado `mypy` às dependências de dev e configurado no `pyproject.toml` para garantir verificação estrita de tipos.
- **Status**: ✅ Implementado

### Configuração Dinâmica em `main.py`
- **Ação**: Atualizado `databricks.yml` para definir variáveis `catalog` e `schema`. Configurados `nasa_gcn.job.yml` e configs de pipeline para usar essas variáveis. Refatorado `src/nasa_gcn/main.py` para aceitar `--catalog` e `--schema` via argumentos de linha de comando usando `argparse`.
- **Status**: ✅ Implementado

### Observabilidade & Logging
- **Ação**: Implementado utilitário central de logging em `src/nasa_gcn/utils.py`. Substituídos `print()` e `warnings.warn()` por logging estruturado (`logger.error`, `logger.warning`, `logger.info`) em `main.py` e `config.py`.
- **Status**: ✅ Implementado

### Modularização do Pipeline SDP (DRY & Integridade de Dados)
- **Ação**: Refatorados pipelines para usar lógica modularizada de `binary_parser.py`, `utils.py`, `schemas.py` e `config.py`. Eliminada duplicação de código onde possível.
- **Nota**: Parser binário ainda duplicado em `silver_pipeline.py` devido a limitações de UDF serverless (ver #1 acima)
- **Status**: ✅ Implementado (com limitação conhecida)

### Converter Pipeline DLT para Arquivo Python
- **Ação**: Convertido `src/pipeline.ipynb` para arquivos Python. Agora estruturado como `bronze_pipeline.py`, `silver_pipeline.py`, `gold_pipeline.py`.
- **Status**: ✅ Implementado

### Qualidade de Código & Linting
- **Ação**: Adicionado `ruff` às dependências `dev` no `pyproject.toml` e configurado tamanho de linha (100) e versão alvo (py310). Corrigidos erros de linting existentes em `src/nasa_gcn` e `tests`.
- **Status**: ✅ Implementado

### Refatorar `pipeline.ipynb` em Módulos
- **Ação**: Criado pacote `src/nasa_gcn` com `utils.py`, `schemas.py` e `binary_parser.py`.
- **Status**: ✅ Implementado

### Lógica Redundante
- **Ação**: Criadas funções utilitárias `decode_utf8` e `clean_json_id`.
- **Status**: ✅ Implementado

### Schemas Hardcoded
- **Ação**: Centralizados schemas em `src/nasa_gcn/schemas.py`.
- **Status**: ✅ Implementado

### Enriquecimento Avançado (Camada Gold)
- **Ação**: Criadas materialized views `gcn_events_summary` e `gcn_daily_stats` fazendo join de tabelas Silver.
- **Status**: ✅ Implementado

---

## Métricas

**Estado Atual:**
- Total de Código: ~1.500 linhas Python (3 arquivos de pipeline)
- Cobertura de Testes: ~7.3%
- Testes: 19 total (18 passando, 1 falhando)
- Itens Pendentes: 8
- Itens Críticos: 2
- Itens Sprint 1: 2 (estimativa 1 semana)
- Itens Sprint 2: 3 (estimativa 2 semanas)

**Estado Alvo (Pós Sprint 3):**
- Cobertura de Testes: >60%
- Todos os Testes: Passando
- Itens Críticos: 0
- CI/CD: Automatizado
- Qualidade de Código: Todo linting passando
- Qualidade de Dados: Expectations em todas as tabelas Silver

---

**Última Atualização**: 2026-03-11
**Próxima Revisão**: Após conclusão da Sprint 1
