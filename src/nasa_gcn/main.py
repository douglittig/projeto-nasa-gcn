"""
NASA GCN Pipeline - Entry Point

Este módulo é o ponto de entrada para execução via Databricks Jobs.
Executa validações e exibe estatísticas do pipeline, incluindo métricas
de linhas processadas na última execução dos pipelines DLT.

Arquitetura Medallion:
  nasa_gcn.bronze.raw → nasa_gcn.silver.* → nasa_gcn.gold.*
"""

import argparse
from typing import Any, Dict, List, Optional, Union

from databricks.sdk.runtime import spark

from nasa_gcn.utils import get_logger

# Initialize logger
logger = get_logger(__name__)

# Mapeamento de tabelas por camada (Medallion Architecture)
# Estrutura: {layer_name: {schema_arg: [table_names]}}
TABLE_LAYERS: Dict[str, Dict[str, List[str]]] = {
    "🥉 BRONZE": {
        "bronze": ["gcn_raw"],
    },
    "🥈 SILVER": {
        "silver": [
            "gcn_circulars",
            "gcn_notices",
            "gcn_classic_text",
            "gcn_classic_voevent",
            "gcn_classic_binary",
            "gcn_gwalert",
            "gcn_heartbeat",
        ],
    },
    "🥇 GOLD": {
        "gold": [
            "gcn_events_summary",
            "gcn_daily_stats",
        ],
    },
}


def get_pipeline_ids() -> Dict[str, Optional[str]]:
    """
    Obtém os Pipeline IDs dos 3 pipelines DLT dinamicamente.
    Retorna dict com {layer: pipeline_id}.
    """
    from databricks.sdk import WorkspaceClient

    pipelines_found: Dict[str, Optional[str]] = {
        "bronze": None,
        "silver": None,
        "gold": None,
    }

    try:
        w = WorkspaceClient()
        pipelines = list(w.pipelines.list_pipelines())

        for pipeline in pipelines:
            if not pipeline.name:
                continue
            name_lower = pipeline.name.lower()
            if "bronze" in name_lower and "nasa" in name_lower:
                pipelines_found["bronze"] = pipeline.pipeline_id
            elif "silver" in name_lower and "nasa" in name_lower:
                pipelines_found["silver"] = pipeline.pipeline_id
            elif "gold" in name_lower and "nasa" in name_lower:
                pipelines_found["gold"] = pipeline.pipeline_id

        return pipelines_found
    except Exception as e:
        logger.error(f"Erro ao obter Pipeline IDs: {e}")
        return pipelines_found


def get_dlt_metrics(pipeline_id: str) -> Dict[str, int]:
    """
    Consulta o event_log do DLT para obter métricas da última execução.

    Retorna um dicionário com o número de linhas processadas por tabela:
    {"table_name": num_output_rows, ...}
    """
    if not pipeline_id:
        return {}

    try:
        query = f"""
        WITH latest_update AS (
            SELECT origin.update_id
            FROM event_log('{pipeline_id}')
            WHERE event_type = 'create_update'
            ORDER BY timestamp DESC
            LIMIT 1
        ),
        flow_metrics AS (
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

        metrics: Dict[str, int] = {}
        for row in result:
            full_name = row.table_name
            table_basename = full_name.split(".")[-1] if full_name else full_name
            if table_basename in metrics:
                metrics[table_basename] += row.rows_processed
            else:
                metrics[table_basename] = row.rows_processed

        return metrics

    except Exception as e:
        logger.warning(f"Não foi possível obter métricas DLT: {e}")
        return {}


def get_table_count(catalog: str, schema: str, table: str) -> Union[int, str]:
    """Retorna contagem de uma tabela ou mensagem de erro."""
    full_name = f"{catalog}.{schema}.{table}"
    try:
        return spark.table(full_name).count()
    except Exception as e:
        return f"Error: {e}"


def format_number(value: Any) -> str:
    """Formata número com separador de milhar ou retorna string de erro."""
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="NASA GCN Pipeline Job")
    parser.add_argument(
        "--catalog",
        type=str,
        default="nasa_gcn",
        help="Unity Catalog name"
    )
    parser.add_argument(
        "--schema-bronze",
        type=str,
        default="bronze",
        help="Schema for Bronze layer"
    )
    parser.add_argument(
        "--schema-silver",
        type=str,
        default="silver",
        help="Schema for Silver layer"
    )
    parser.add_argument(
        "--schema-gold",
        type=str,
        default="gold",
        help="Schema for Gold layer"
    )
    return parser.parse_args()


def main() -> None:
    """Função principal executada pelo Databricks Job."""
    args = parse_args()

    schemas = {
        "bronze": args.schema_bronze,
        "silver": args.schema_silver,
        "gold": args.schema_gold,
    }

    print("=" * 60)
    print("NASA GCN Pipeline - Status Report")
    print(f"Catalog: {args.catalog}")
    print(f"Schemas: bronze={schemas['bronze']}, silver={schemas['silver']}, gold={schemas['gold']}")
    print("=" * 60)

    # Obtém métricas DLT da última execução de cada pipeline
    pipeline_ids = get_pipeline_ids()
    all_dlt_metrics: Dict[str, int] = {}

    for layer, pid in pipeline_ids.items():
        if pid:
            metrics = get_dlt_metrics(pid)
            all_dlt_metrics.update(metrics)

    if all_dlt_metrics:
        print("\n📊 Métricas da última execução dos pipelines")
        print("-" * 40)

    # Itera por cada camada
    for layer_name, schema_tables in TABLE_LAYERS.items():
        print(f"\n{layer_name}")
        print("-" * 40)

        for schema_key, tables in schema_tables.items():
            schema = schemas[schema_key]

            for table_name in tables:
                total_count = get_table_count(args.catalog, schema, table_name)
                total_str = format_number(total_count)

                # Verifica se temos métricas DLT para esta tabela
                rows_processed = all_dlt_metrics.get(table_name)

                if rows_processed is not None and rows_processed > 0:
                    print(
                        f"  • {args.catalog}.{schema}.{table_name}: "
                        f"{total_str} (total) | +{rows_processed:,} (última execução)"
                    )
                else:
                    print(f"  • {args.catalog}.{schema}.{table_name}: {total_str}")

    print("\n" + "=" * 60)
    print("Pipeline executado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
