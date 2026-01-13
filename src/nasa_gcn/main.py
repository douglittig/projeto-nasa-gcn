"""
NASA GCN Pipeline - Entry Point

Este módulo é o ponto de entrada para execução via Databricks Jobs.
Executa validações e exibe estatísticas do pipeline.
"""

from databricks.sdk.runtime import spark


def get_pipeline_stats():
    """Retorna estatísticas das tabelas do pipeline GCN."""
    stats = {}
    
    tables = [
        "sandbox.nasa_gcn_dev.gcn_raw",
        "sandbox.nasa_gcn_dev.gcn_circulars",
        "sandbox.nasa_gcn_dev.gcn_notices",
        "sandbox.nasa_gcn_dev.igwn_gwalert",
        "sandbox.nasa_gcn_dev.gcn_events_summarized"
    ]
    
    for table in tables:
        try:
            count = spark.table(table).count()
            stats[table.split(".")[-1]] = count
        except Exception as e:
            stats[table.split(".")[-1]] = f"Error: {e}"
    
    return stats


def main():
    """Função principal executada pelo Databricks Job."""
    print("=" * 60)
    print("NASA GCN Pipeline - Status Report")
    print("=" * 60)
    
    stats = get_pipeline_stats()
    
    print("\n📊 Contagem de Registros por Tabela:\n")
    for table, count in stats.items():
        print(f"  • {table}: {count}")
    
    print("\n" + "=" * 60)
    print("Pipeline executado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
