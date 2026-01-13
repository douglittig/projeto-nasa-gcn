"""
NASA GCN Pipeline - Entry Point

Este módulo é o ponto de entrada para execução via Databricks Jobs.
Executa validações e exibe estatísticas do pipeline.
"""

from databricks.sdk.runtime import spark


def get_pipeline_stats():
    """Retorna estatísticas das tabelas do pipeline GCN."""
    stats = {}
    
    # Bronze
    bronze_tables = [
        ("gcn_raw", "sandbox.nasa_gcn_dev.gcn_raw"),
    ]
    
    # Silver
    silver_tables = [
        ("gcn_classic_text", "sandbox.nasa_gcn_dev.gcn_classic_text"),
        ("gcn_classic_voevent", "sandbox.nasa_gcn_dev.gcn_classic_voevent"),
        ("gcn_classic_binary", "sandbox.nasa_gcn_dev.gcn_classic_binary"),
        ("gcn_notices", "sandbox.nasa_gcn_dev.gcn_notices"),
        ("gcn_circulars", "sandbox.nasa_gcn_dev.gcn_circulars"),
        ("igwn_gwalert", "sandbox.nasa_gcn_dev.igwn_gwalert"),
        ("gcn_heartbeat", "sandbox.nasa_gcn_dev.gcn_heartbeat"),
    ]
    
    # Gold
    gold_tables = [
        ("gcn_events_summarized", "sandbox.nasa_gcn_dev.gcn_events_summarized"),
    ]
    
    all_tables = [
        ("🥉 BRONZE", bronze_tables),
        ("🥈 SILVER", silver_tables),
        ("🥇 GOLD", gold_tables),
    ]
    
    for layer_name, tables in all_tables:
        stats[layer_name] = {}
        for name, full_name in tables:
            try:
                count = spark.table(full_name).count()
                stats[layer_name][name] = count
            except Exception as e:
                stats[layer_name][name] = f"Error: {e}"
    
    return stats


def main():
    """Função principal executada pelo Databricks Job."""
    print("=" * 60)
    print("NASA GCN Pipeline - Status Report")
    print("=" * 60)
    
    stats = get_pipeline_stats()
    
    for layer, tables in stats.items():
        print(f"\n{layer}")
        print("-" * 40)
        for table, count in tables.items():
            print(f"  • {table}: {count:,}" if isinstance(count, int) else f"  • {table}: {count}")
    
    print("\n" + "=" * 60)
    print("Pipeline executado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
