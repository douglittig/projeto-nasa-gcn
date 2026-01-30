#!/bin/bash
# ==============================================================================
# NASA GCN Pipeline - Deploy & Run Script
# ==============================================================================
# Uso:
#   ./deploy.sh              # Apenas deploy
#   ./deploy.sh run          # Deploy + executa job
#   ./deploy.sh run-only     # Apenas executa job (sem deploy)
# ==============================================================================

set -e

# Carregar variáveis do .env
if [ -f .env ]; then
    source .env
else
    echo "❌ Arquivo .env não encontrado!"
    echo "   Copie .env.example para .env e configure suas credenciais."
    exit 1
fi

# Função para decodificar Base64
decode_base64() {
    echo "$1" | base64 -d 2>/dev/null || echo ""
}

# Carregar credenciais (prioridade: Base64 > Plain-text)
CLIENT_ID=""
CLIENT_SECRET=""

# Tentar carregar versões Base64 primeiro
if [ -n "$GCN_CLIENT_ID_B64" ]; then
    CLIENT_ID=$(decode_base64 "$GCN_CLIENT_ID_B64")
    if [ -n "$CLIENT_ID" ]; then
        echo "🔒 Credenciais carregadas (Base64-encoded)"
    fi
fi

if [ -n "$GCN_CLIENT_SECRET_B64" ]; then
    CLIENT_SECRET=$(decode_base64 "$GCN_CLIENT_SECRET_B64")
fi

# Fallback para versões plain-text
if [ -z "$CLIENT_ID" ] && [ -n "$GCN_CLIENT_ID" ]; then
    CLIENT_ID="$GCN_CLIENT_ID"
    echo "⚠️  Credenciais carregadas (plain-text) - considere usar Base64"
fi

if [ -z "$CLIENT_SECRET" ] && [ -n "$GCN_CLIENT_SECRET" ]; then
    CLIENT_SECRET="$GCN_CLIENT_SECRET"
fi

# Validar que credenciais foram carregadas
if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
    echo "❌ Erro: Credenciais não encontradas!"
    echo ""
    echo "   Configure credenciais no arquivo .env usando uma das opções:"
    echo ""
    echo "   Opção 1 (RECOMENDADO): Base64-encoded"
    echo "     python scripts/encode_credentials.py"
    echo "     # Cole o output no .env"
    echo ""
    echo "   Opção 2: Plain-text (apenas desenvolvimento)"
    echo "     GCN_CLIENT_ID=your_id"
    echo "     GCN_CLIENT_SECRET=your_secret"
    exit 1
fi

# Exportar variáveis para o Databricks Bundle
export BUNDLE_VAR_gcn_client_id="$CLIENT_ID"
export BUNDLE_VAR_gcn_client_secret="$CLIENT_SECRET"

# Configurações
TARGET="${TARGET:-dev}"
PROFILE="${PROFILE:-dltreinamentos.data@gmail.com}"

echo "============================================================"
echo "NASA GCN Pipeline - Deploy Script"
echo "============================================================"
echo "  Target:  $TARGET"
echo "  Profile: $PROFILE"
echo "============================================================"

case "${1:-deploy}" in
    deploy)
        echo "🚀 Deploying bundle..."
        databricks bundle deploy -t "$TARGET" -p "$PROFILE"
        echo "✅ Deploy concluído!"
        ;;
    run)
        echo "🚀 Deploying bundle..."
        databricks bundle deploy -t "$TARGET" -p "$PROFILE"
        echo "✅ Deploy concluído!"
        echo ""
        echo "🏃 Executando job..."
        databricks bundle run nasa_gcn_job -p "$PROFILE"
        ;;
    run-only)
        echo "🏃 Executando job..."
        databricks bundle run nasa_gcn_job -p "$PROFILE"
        ;;
    *)
        echo "Uso: $0 [deploy|run|run-only]"
        exit 1
        ;;
esac
