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

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

#### Opção A: Base64-encoded credentials (RECOMENDADO) 🔒

Para melhor segurança, use credenciais encodadas em Base64:

```bash
# Use o script helper para encodar suas credenciais
python scripts/encode_credentials.py
```

O script irá:
1. Solicitar suas credenciais (input oculto)
2. Codificá-las em Base64
3. Exibir os valores para copiar no `.env`

Cole a saída no arquivo `.env`:
```bash
GCN_CLIENT_ID_B64=c2V1X2NsaWVudF9pZF9hcXVp
GCN_CLIENT_SECRET_B64=c2V1X2NsaWVudF9zZWNyZXRfYXF1aQ==
```

#### Opção B: Plain-text credentials (apenas desenvolvimento)

Edite o arquivo `.env` diretamente:

```bash
GCN_CLIENT_ID=seu_client_id_aqui
GCN_CLIENT_SECRET=seu_client_secret_aqui
```

⚠️ **Importante**:
- O arquivo `.env` está no `.gitignore` e **não será commitado**
- Base64 é ofuscação, NÃO encriptação (veja seção de segurança abaixo)

### 🔐 Segurança de Credenciais

#### Limitações do Databricks Community Edition

O **Databricks Community Edition (Free)** possui limitações importantes:

- ❌ **Não suporta** Databricks Secrets API
- ❌ **Não suporta** integração com Azure Key Vault / AWS Secrets Manager
- ❌ **Não suporta** Service Principals
- ✅ **Suporta apenas** variáveis de ambiente e configuração de jobs

#### Nossa Abordagem: Base64 Encoding

Para mitigar riscos no Free Edition, implementamos **Base64 encoding**:

**O que Base64 oferece:**
- ✅ Ofuscação básica contra visualização acidental
- ✅ Reduz exposição em logs e screenshots
- ✅ Dificulta exposição em process inspection
- ✅ Compatível com Community Edition

**O que Base64 NÃO oferece:**
- ❌ **NÃO é encriptação** - pode ser facilmente decodificado
- ❌ **NÃO protege** contra acessos maliciosos
- ❌ **NÃO substitui** gerenciamento adequado de secrets

#### Para Ambiente de Produção

Se você migrar para um workspace pago do Databricks, **recomendamos fortemente** usar:

1. **Databricks Secrets** (recomendado)
   ```python
   dbutils.secrets.get(scope="gcn_secrets", key="client_id")
   ```
   - [Documentação oficial](https://docs.databricks.com/security/secrets/index.html)

2. **Azure Key Vault** (Azure)
   - Integração nativa com Databricks
   - [Documentação](https://docs.databricks.com/security/secrets/secret-scopes.html#azure-key-vault-backed-scopes)

3. **AWS Secrets Manager** (AWS)
   - Integração via Secrets Scopes
   - [Documentação](https://docs.databricks.com/security/secrets/secret-scopes.html#aws-secrets-manager-backed-scopes)

#### Best Practices

- 🔒 Use Base64 encoding no Community Edition
- 🔄 Rotacione credenciais periodicamente
- 📝 Nunca commite o arquivo `.env`
- 🚨 Monitore logs para exposições acidentais
- 🎯 Planeje migração para Databricks Secrets ao escalar

> 💡 **Nota**: Esta configuração foi projetada para balancear segurança e compatibilidade com o Databricks Free Edition. Para produção, sempre use soluções enterprise de gerenciamento de secrets.


## 📦 Databricks Asset Bundles

### Validar bundle

```bash
databricks bundle validate
```

### 🚀 Deploy e Execução (Recomendado)

Use o script `deploy.sh` que carrega as credenciais do `.env` automaticamente:

```bash
# Apenas deploy (envia código para o Databricks)
./deploy.sh

# Deploy + executa o job completo
./deploy.sh run

# Apenas executa o job (sem fazer novo deploy)
./deploy.sh run-only
```

**Saída esperada:**
```
============================================================
NASA GCN Pipeline - Deploy Script
============================================================
  Target:  dev
  Profile: dltreinamentos.data@gmail.com
============================================================
🚀 Deploying bundle...
✅ Deploy concluído!
🏃 Executando job...
```

Após a execução, o Status Report exibe **métricas de linhas processadas**:
```
🥉 BRONZE
  • gcn_raw: 3,385,887 (total) | +726 (última execução)

🥈 SILVER
  • gcn_classic_text: 15,381 (total) | +4 (última execução)
  • gcn_heartbeat: 3,334,431 (total) | +713 (última execução)
  ...

🥇 GOLD
  • gcn_events_summarized: 125 (total) | +125 (última execução)
```

> 💡 As métricas são obtidas do [Event Log do DLT](https://docs.databricks.com/en/delta-live-tables/observability.html), consultando `num_output_rows` de cada tabela.

### Configurações Avançadas

```bash
# Deploy para produção
TARGET=prod ./deploy.sh run

# Usar outro perfil do Databricks
PROFILE=meu-perfil ./deploy.sh run
```

### Deploy Manual (Alternativa)

Se preferir executar manualmente sem o script:

```bash
source .env
export BUNDLE_VAR_gcn_client_id=$GCN_CLIENT_ID
export BUNDLE_VAR_gcn_client_secret=$GCN_CLIENT_SECRET
databricks bundle deploy -t dev
databricks bundle run nasa_gcn_job
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
| `gcn_events_summarized` | **Gold** | Joia da Coroa: Eventos consolidados com narrativa ([Docs](docs/GOLD_LAYER.md)) |

## 🔗 Referências

- [NASA GCN Documentation](https://gcn.nasa.gov/docs)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Lakeflow Declarative Pipelines](https://docs.databricks.com/delta-live-tables/index.html)
- [uv Package Manager](https://docs.astral.sh/uv/)

## 📄 Licença

MIT
