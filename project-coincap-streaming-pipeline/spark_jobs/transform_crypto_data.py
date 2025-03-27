from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name

# Initialize Spark
spark = SparkSession.builder.appName("CryptoPriceTransform").getOrCreate()

# Define input/output paths
INPUT_PATH = "gs://souf-de-zoomcamp-project/crypto/raw/*/*/*.json"
OUTPUT_PATH = "gs://souf-de-zoomcamp-project/crypto/processed/"

# Read JSON files
df = spark.read.json(INPUT_PATH, multiLine=True)

# Add metadata columns
df = df.withColumn("ingestion_time", current_timestamp())
df = df.withColumn("source_file", input_file_name())

# Explode each row (which is a dictionary of crypto prices)
from pyspark.sql.functions import explode, map_keys, col

df_exploded = df.select(explode("value").alias("crypto", "price")) \
                .withColumn("ingestion_time", col("ingestion_time")) \
                .withColumn("source_file", col("source_file"))

# Cast price to float
df_clean = df_exploded.withColumn("price", col("price").cast("float"))

# Write to GCS in Parquet format, partitioned by crypto
df_clean.write.mode("overwrite").partitionBy("crypto").parquet(OUTPUT_PATH)

print("✅ Transformation complete and saved to:", OUTPUT_PATH)
