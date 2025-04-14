import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, TimestampType

# Logging
logging.basicConfig(level=logging.INFO)

# Environment variables
GCS_PATH = os.getenv("GCS_PATH", "gs://souf-de-zoomcamp-project/crypto/raw/*/*")
BQ_TABLE = os.getenv("BQ_TABLE", "crypto_streaming.prices")
TEMP_GCS_BUCKET = os.getenv("TEMP_GCS_BUCKET", "souf-de-zoomcamp-project")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("GCS to BigQuery") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1") \
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS") \
    .getOrCreate()

# Define schema
schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("priceUsd", StringType(), True),
    StructField("timestamp", LongType(), True)
])

# Read and parse NDJSON from GCS
df = spark.read.schema(schema).json(GCS_PATH)

# Type casting
df_cleaned = df \
    .withColumn("priceUsd", col("priceUsd").cast(DoubleType())) \
    .withColumn("time", (col("timestamp") / 1000).cast(TimestampType())) \
    .select("symbol", "priceUsd", "time")

logging.info(f"Number of records: {df_cleaned.count()}")
df_cleaned.show(5, truncate=False)

# Write to BigQuery
df_cleaned.write \
    .format("bigquery") \
    .option("table", BQ_TABLE) \
    .option("temporaryGcsBucket", TEMP_GCS_BUCKET) \
    .mode("append") \
    .save()