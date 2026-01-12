"""
Vectorization Job for NASA GCN RAG.

Reads the Gold Layer (gcn_events_summarized), generates embeddings for the 'scientific_narrative',
and stores the results in a Delta Table (ready for Databricks Vector Search).

Prerequisites:
    pip install sentence-transformers
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, col
import pandas as pd
from typing import Iterator

def run_vectorization():
    # Initialize Spark
    spark = SparkSession.builder.appName("GCN_Vectorization").getOrCreate()

    # Configuration
    GOLD_TABLE = "sandbox.nasa_gcn_dev.gcn_events_summarized"
    VECTOR_TABLE = "sandbox.nasa_gcn_dev.gcn_embeddings"
    # Using a small, high-performance model suitable for scientific text
    EMBEDDING_MODEL = "BAAI/bge-m3"

    print(f"Reading Gold Layer: {GOLD_TABLE}")
    df_gold = spark.table(GOLD_TABLE).filter(col("scientific_narrative").isNotNull())

    # -----------------------------------------------------------------------------
    # Vectorization UDF (using pandas_udf for efficiency on GPU/CPU)
    # -----------------------------------------------------------------------------
    @pandas_udf("array<float>")
    def generate_embeddings(text_series: pd.Series) -> pd.Series:
        # Import inside UDF to ensure it runs on executors
        from sentence_transformers import SentenceTransformer
        
        # Load model (cached per executor)
        model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Generate embeddings
        # encode returns numpy array, convert to list for Spark ArrayType
        embeddings = model.encode(text_series.tolist(), show_progress_bar=False)
        return pd.Series(embeddings.tolist())

    # -----------------------------------------------------------------------------
    # Execution
    # -----------------------------------------------------------------------------
    print(f"Generating embeddings using {EMBEDDING_MODEL}...")

    df_vectors = df_gold.select(
        col("event_id"),
        col("event_time"),
        col("scientific_narrative"),
        generate_embeddings(col("scientific_narrative")).alias("embedding")
    )

    # Write to Delta
    print(f"Writing embeddings to {VECTOR_TABLE}...")
    df_vectors.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(VECTOR_TABLE)
    
    print("Vectorization complete!")

if __name__ == "__main__":
    run_vectorization()
