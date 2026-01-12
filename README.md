# NASA GCN Data Pipeline

Pipeline de ingestão de dados da NASA GCN (Gamma-ray Coordinates Network) usando Databricks Asset Bundles e Lakeflow Declarative Pipelines.

## � Índice

- [📋 Pré-requisitos](#-pré-requisitos)
- [🚀 Configuração do Ambiente Local](#-configuração-do-ambiente-local)
- [🔑 Configurar Credenciais NASA GCN](#-configurar-credenciais-nasa-gcn)
- [📦 Databricks Asset Bundles](#-databricks-asset-bundles)
- [🏗️ Arquitetura](#️-arquitetura)
- [📊 Tabelas](#-tabelas)
- [🔗 Referências](#-referências)


## �📋 Pré-requisitos

- Python 3.11+
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/databricks-cli.html) v0.200+
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes Python)
- Conta no [Databricks Free Edition](https://www.databricks.com/try-databricks)
- Credenciais da [NASA GCN](https://gcn.nasa.gov/quickstart)

## 🚀 Configuração do Ambiente Local

### 1. Instalar o uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```
> 📖 [Documentação oficial do uv](https://docs.astral.sh/uv/getting-started/installation/)

### 2. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/projeto-nasa-gcn.git
cd projeto-nasa-gcn
```

### 3. Criar ambiente virtual e instalar dependências

```bash
uv sync --dev
```

Isso criará um ambiente virtual em `.venv/` com todas as dependências.

### 4. Instalar Databricks CLI

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# Ou via Homebrew
brew install databricks/tap/databricks
```
> 📖 [Documentação oficial do Databricks CLI](https://docs.databricks.com/dev-tools/cli/install.html)

### 5. Configurar autenticação do Databricks

```bash
databricks configure
```

Informe:
- **Host**: URL do seu workspace (ex: `https://dbc-xxxxx.cloud.databricks.com`)
- **Token**: Gere em Settings > Developer > Access Tokens

> 📖 [Documentação de autenticação](https://docs.databricks.com/dev-tools/cli/authentication.html)

### 6. Verificar configuração

```bash
databricks auth profiles
```

## 🔑 Configurar Credenciais NASA GCN

### 1. Criar conta no GCN

Acesse [gcn.nasa.gov](https://gcn.nasa.gov) e crie uma conta.

### 2. Obter credenciais Kafka

1. Faça login no [GCN](https://gcn.nasa.gov)
2. Vá em **Quickstart** > **Credentials**
3. Copie o `Client ID` e `Client Secret`

> 📖 [Documentação do GCN Kafka](https://gcn.nasa.gov/docs/client)

### 3. Configurar credenciais no projeto

Copie o arquivo de exemplo e preencha suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```bash
GCN_CLIENT_ID=seu_client_id_aqui
GCN_CLIENT_SECRET=seu_client_secret_aqui
```

⚠️ **Importante**: O arquivo `.env` está no `.gitignore` e **não será commitado**.


## 📦 Databricks Asset Bundles

### Validar bundle

```bash
databricks bundle validate
```

### Deploy para desenvolvimento

```bash
# Carrega variáveis do .env e faz deploy
. ./.env && databricks bundle deploy --target dev \
  --var gcn_client_id=$GCN_CLIENT_ID \
  --var gcn_client_secret=$GCN_CLIENT_SECRET
```

### Executar pipeline

```bash
# Usando BUNDLE_VAR_* environment variables
. ./.env && \
  BUNDLE_VAR_gcn_client_id=$GCN_CLIENT_ID \
  BUNDLE_VAR_gcn_client_secret=$GCN_CLIENT_SECRET \
  databricks bundle run nasa_gcn_pipeline
```


> 📖 [Documentação do Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)

## 🏗️ Arquitetura

```
┌──────────────────┐
│  NASA GCN Kafka  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    gcn_raw       │  Bronze
│  (todas msgs)    │
└────────┬─────────┘
         │
    ┌────┴────┬────────┬────────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ text  │ │voevent│ │binary │ │notices│ │circu- │ │igwn_  │ │heart- │
│       │ │       │ │       │ │       │ │lars   │ │gwalert│ │beat   │
└───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
                         Silver Layer
                              │
                              ▼
                        ┌─────────────┐
                        │ Gold Layer  │  gcn_events_summarized
                        └──────┬──────┘
                               ▼
                        ┌─────────────┐
                        │ Vectors/RAG │  gcn_embeddings
                        └─────────────┘

## 📊 Tabelas

| Tabela | Camada | Descrição |
|--------|--------|-----------|
| `gcn_raw` | Bronze | Todas as mensagens raw do Kafka |
| `gcn_classic_text` | Silver | Alertas em formato texto ([Docs RAG](docs/GCN_CLASSIC_TEXT_RAG.md)) |
| `gcn_classic_voevent` | Silver | Alertas em formato VoEvent XML ([Docs RAG](docs/GCN_CLASSIC_VOEVENT_RAG.md)) |
| `gcn_classic_binary` | Silver | Alertas em formato binário ([Docs RAG](docs/GCN_CLASSIC_BINARY_RAG.md)) |
| `gcn_notices` | Silver | Novos alertas em formato JSON ([Docs RAG](docs/GCN_NOTICES_RAG.md)) |
| `gcn_circulars` | Silver | Circulares astronômicas ([Docs RAG](docs/GCN_CIRCULARS_RAG.md)) |
| `igwn_gwalert` | Silver | Alertas de ondas gravitacionais ([Docs RAG](docs/IGWN_GWALERT_RAG.md)) |
| `gcn_heartbeat` | Silver | Mensagens de teste/heartbeat |
| `gcn_events_summarized` | **Gold** | Joia da Coroa: Eventos consolidados com narrativa ([Docs](docs/GOLD_LAYER_RAG.md)) |

## 🔗 Referências

- [NASA GCN Documentation](https://gcn.nasa.gov/docs)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Lakeflow Declarative Pipelines](https://docs.databricks.com/delta-live-tables/index.html)
- [uv Package Manager](https://docs.astral.sh/uv/)

## 📄 Licença

MIT
