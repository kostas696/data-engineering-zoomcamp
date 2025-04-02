from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, TimestampType
from pyspark.sql.functions import to_timestamp

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

# Read and parse NDJSON-style file from GCS
input_path = "gs://souf-de-zoomcamp-project/crypto/raw/*/*"
df = spark.read.schema(schema).json(input_path)

# Cast types
df_cleaned = df \
    .withColumn("priceUsd", col("priceUsd").cast(DoubleType())) \
    .withColumn("time", (col("timestamp") / 1000).cast(TimestampType())) \
    .select("symbol", "priceUsd", "time")

print(f"Number of records: {df_cleaned.count()}")
df_cleaned.show(5, truncate=False)

# Write to BigQuery
df_cleaned.write \
    .format("bigquery") \
    .option("table", "crypto_streaming.prices") \
    .option("temporaryGcsBucket", "souf-de-zoomcamp-project") \
    .mode("append") \
    .save()