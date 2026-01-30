"""
NASA GCN Pipeline - Entry Point

Este módulo é o ponto de entrada para execução via Databricks Jobs.
Executa validações e exibe estatísticas do pipeline, incluindo métricas
de linhas processadas na última execução do DLT.
"""

import argparse
from typing import Any, Dict, List, Optional, Union

from databricks.sdk.runtime import spark

from nasa_gcn.utils import get_logger

# Initialize logger
logger = get_logger(__name__)

# Mapeamento de tabelas por camada (Medallion Architecture)
TABLE_LAYERS: Dict[str, List[str]] = {
    "🥉 BRONZE": ["gcn_raw"],
    "🥈 SILVER": [
        "gcn_classic_text",
        "gcn_classic_voevent",
        "gcn_classic_binary",
        "gcn_notices",
        "gcn_circulars",
        "igwn_gwalert",
        "gcn_heartbeat",
    ],
    "🥇 GOLD": ["gcn_events_summarized"],
}


def get_pipeline_id() -> Optional[str]:
    """
    Obtém o Pipeline ID do DLT dinamicamente.
    Procura por pipelines que escrevem no schema configurado.
    """
    from databricks.sdk import WorkspaceClient

    try:
        w = WorkspaceClient()
        pipelines = list(w.pipelines.list_pipelines())

        for pipeline in pipelines:
            # Procura pelo pipeline que usa nosso schema (considera prefixo [dev ...])
            # Ex: "[dev dltreinamentos_data] nasa_gcn_pipeline" ou "nasa_gcn_pipeline"
            if pipeline.name and "nasa_gcn" in pipeline.name.lower():
                return pipeline.pipeline_id
        return None
    except Exception as e:
        logger.error(f"Erro ao obter Pipeline ID: {e}")
        return None


def get_dlt_metrics(pipeline_id: str) -> Dict[str, int]:
    """
    Consulta o event_log do DLT para obter métricas da última execução.

    Retorna um dicionário com o número de linhas processadas por tabela:
    {"table_name": num_output_rows, ...}

    Nota: Tabelas streaming (Bronze/Silver) podem não reportar num_output_rows
    da mesma forma que tabelas batch (Gold).
    """
    if not pipeline_id:
        return {}

    try:
        # Query para obter métricas de flow_progress da última execução
        # O event_log() é uma table-valued function do Unity Catalog
        #
        # Status possíveis: QUEUED, STARTING, RUNNING, COMPLETED, FAILED,
        #                   SKIPPED, STOPPED, IDLE, EXCLUDED
        # - Tabelas batch (dlt.read) geralmente reportam COMPLETED
        # - Tabelas streaming (dlt.read_stream) podem reportar IDLE ou RUNNING
        query = f"""
        WITH latest_update AS (
            -- Encontra o update_id mais recente
            SELECT origin.update_id
            FROM event_log('{pipeline_id}')
            WHERE event_type = 'create_update'
            ORDER BY timestamp DESC
            LIMIT 1
        ),
        flow_metrics AS (
            -- Extrai métricas de cada flow (tabela) do último update
            -- Não filtra por status específico para capturar streaming e batch
            SELECT
                origin.flow_name AS table_name,
                details:flow_progress:status::STRING AS flow_status,
                details:flow_progress:metrics:num_output_rows::LONG AS rows_processed
            FROM event_log('{pipeline_id}')
            WHERE event_type = 'flow_progress'
              AND origin.update_id = (SELECT update_id FROM latest_update)
              AND details:flow_progress:metrics:num_output_rows IS NOT NULL
        )
        SELECT table_name, flow_status, SUM(rows_processed) as rows_processed
        FROM flow_metrics
        GROUP BY table_name, flow_status
        """

        result = spark.sql(query).collect()

        # Normaliza nomes: flow_name vem como "catalog.schema.table", queremos só "table"
        metrics: Dict[str, int] = {}
        for row in result:
            full_name = row.table_name
            # Extrai apenas o nome base da tabela (última parte após o último ponto)
            table_basename = full_name.split(".")[-1] if full_name else full_name
            # Soma caso haja múltiplos registros para a mesma tabela
            if table_basename in metrics:
                metrics[table_basename] += row.rows_processed
            else:
                metrics[table_basename] = row.rows_processed

        return metrics

    except Exception as e:
        logger.warning(f"Não foi possível obter métricas DLT: {e}")
        return {}


def get_pipeline_stats(catalog: str, schema: str) -> Dict[str, Dict[str, Union[int, str]]]:
    """Retorna estatísticas das tabelas do pipeline GCN (contagem total)."""
    stats: Dict[str, Dict[str, Union[int, str]]] = {}

    for layer_name, tables in TABLE_LAYERS.items():
        stats[layer_name] = {}
        for table_name in tables:
            full_name = f"{catalog}.{schema}.{table_name}"
            try:
                count = spark.table(full_name).count()
                stats[layer_name][table_name] = count
            except Exception as e:
                stats[layer_name][table_name] = f"Error: {e}"

    return stats


def format_number(value: Any) -> str:
    """Formata número com separador de milhar ou retorna string de erro."""
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="NASA GCN Pipeline Job")
    parser.add_argument("--catalog", type=str, default="sandbox", help="Unity Catalog name")
    parser.add_argument("--schema", type=str, default="nasa_gcn_dev", help="Schema name")
    return parser.parse_args()


def main() -> None:
    """Função principal executada pelo Databricks Job."""
    args = parse_args()

    print("=" * 60)
    print("NASA GCN Pipeline - Status Report")
    print(f"Catalog: {args.catalog} | Schema: {args.schema}")
    print("=" * 60)

    # Obtém contagens totais das tabelas
    stats = get_pipeline_stats(args.catalog, args.schema)

    # Obtém métricas DLT da última execução
    pipeline_id = get_pipeline_id()
    dlt_metrics = get_dlt_metrics(pipeline_id) if pipeline_id else {}

    if dlt_metrics:
        print("\n📊 Métricas da última execução do pipeline")
        print("-" * 40)

    for layer, tables in stats.items():
        print(f"\n{layer}")
        print("-" * 40)

        for table_name, total_count in tables.items():
            total_str = format_number(total_count)

            # Verifica se temos métricas DLT para esta tabela
            rows_processed = dlt_metrics.get(table_name)

            if rows_processed is not None and rows_processed > 0:
                print(
                    f"  • {table_name}: {total_str} (total) | +{rows_processed:,} (última execução)"
                )
            else:
                print(f"  • {table_name}: {total_str}")

    print("\n" + "=" * 60)
    print("Pipeline executado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
