from google.cloud import bigquery

# Set up BigQuery client
client = bigquery.Client()

# Define table
table_id = "platinum-lead-450019-j6.crypto_streaming.prices"

# Query to count rows from today
query = f"""
SELECT COUNT(*) as total
FROM `{table_id}`
WHERE DATE(time) = CURRENT_DATE()
"""

query_job = client.query(query)
result = query_job.result()
row = list(result)[0]

if row.total > 0:
    print(f"Validation passed: {row.total} rows found for today.")
else:
    raise ValueError("Validation failed: No rows found for today.")
