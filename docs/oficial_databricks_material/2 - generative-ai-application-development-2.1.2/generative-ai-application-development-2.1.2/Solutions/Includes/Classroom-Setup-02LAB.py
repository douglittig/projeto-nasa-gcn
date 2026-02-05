# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

DA = DBAcademyHelper()
DA.init()

# COMMAND ----------

def create_product_text_table(vs_source_table_fullname):
    """
    Load a dataset from marketplace, process it, and save it as a Spark DataFrame table.
    """
    
    DA.validate_table("bright_data_etsy_dataset.datasets.etsy")

    dataset = spark.sql("SELECT product_id AS id, CONCAT('## Title: ', title, '\n\n ## Description: ', item_details) AS product FROM bright_data_etsy_dataset.datasets.etsy")

    vs_source_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.product_text"
    dataset.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(vs_source_table_fullname)

    # Enable Change Data Feed for Delta table
    spark.sql(f"ALTER TABLE {vs_source_table_fullname} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")