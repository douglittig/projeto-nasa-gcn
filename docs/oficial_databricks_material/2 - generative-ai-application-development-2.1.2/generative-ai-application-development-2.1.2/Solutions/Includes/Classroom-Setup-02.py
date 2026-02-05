# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

from pyspark.sql import functions as F

DA = DBAcademyHelper()
DA.init()

# create dataset
source_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.dais_text"

df = spark.read.load(f"{DA.paths.datasets.dais}/dais_delta")

df = df.withColumn("id", F.monotonically_increasing_id())
df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(source_table_fullname)
spark.sql(f"ALTER TABLE {source_table_fullname} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

print("Dataset is created successfully.")