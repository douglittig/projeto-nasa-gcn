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

# Validar variáveis obrigatórias
if [ -z "$GCN_CLIENT_ID" ] || [ -z "$GCN_CLIENT_SECRET" ]; then
    echo "❌ Variáveis GCN_CLIENT_ID e GCN_CLIENT_SECRET são obrigatórias!"
    exit 1
fi

# Exportar variáveis para o Databricks Bundle
export BUNDLE_VAR_gcn_client_id="$GCN_CLIENT_ID"
export BUNDLE_VAR_gcn_client_secret="$GCN_CLIENT_SECRET"

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
