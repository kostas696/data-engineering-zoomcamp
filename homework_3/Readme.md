# 📌 NYC Yellow Taxi Data Processing with BigQuery and GCS

## 🚀 Project Overview
This project involves processing **Yellow Taxi Trip Records (Jan - June 2024)** by:
- **Downloading** Parquet files from NYC Taxi Data.
- **Uploading** them to **Google Cloud Storage (GCS)**.
- **Creating External & Materialized Tables** in **BigQuery**.
- **Answering analytical questions** based on SQL queries.

---

## 1️⃣ Data Ingestion Using Python (`dlt`)
We used **`dlt`** and **Google Cloud Storage (GCS)** for data ingestion.

### 📜 Python Script (`load_data_dlt.py`)
The script automates downloading, uploading, and loading data into BigQuery.

(See full script in project folder.)

---

## 2️⃣ BigQuery Table Setup

### 🔹 Create an External Table
```sql
CREATE OR REPLACE EXTERNAL TABLE `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_external`
OPTIONS ( 
  format = 'PARQUET',
  uris = ['gs://data-engineering-kostas696/yellow_tripdata_2024-*.parquet']
);
```

### 🔹 Create a Regular Table
```sql
CREATE OR REPLACE TABLE `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`
AS
SELECT * FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_external`;
```

---

## 3️⃣ Answering the BigQuery Questions

### ✅ Q1: Count of Records in 2024 Yellow Taxi Data
```sql
SELECT COUNT(*) AS total_records
FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`;
```
✅ **Answer:** **20,332,093**

🖼 **Screenshot:**
![Yellow Taxi 2024 Row Count](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_1.JPG)

---

### ✅ Q2: Distinct `PULocationID` + Estimated Bytes Read
```sql
SELECT COUNT(DISTINCT PULocationID) AS unique_pu_locations
FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_external`;
```
📊 **Bytes Read:**
- **External Table:** `0 MB`
- **Materialized Table:** `155.12 MB`
✅ **Answer:** **0 MB for the External Table and 155.12 MB for the Materialized Table**

🖼 **Screenshot:**
![External Table Amount of data](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_21.JPG)

🖼 **Screenshot:**
![Materialized Table Amount of data](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_22.JPG)
---

### ✅ Q3: Why Do Queries Process Different Bytes?
```sql
SELECT PULocationID FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`;
SELECT PULocationID, DOLocationID FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`;
```
✅ **Answer:**  
BigQuery is **columnar**, so querying **one column vs. two columns** affects performance.  
**Querying two columns requires scanning more data than querying one column.**

---

### ✅ Q4: How Many Records Have `fare_amount = 0`?
```sql
SELECT COUNT(*) FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`
WHERE fare_amount = 0;
```
✅ **Answer:** **8,333**

🖼 **Screenshot:**
![Records of fare_amount of 0](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_4.JPG)

---

### ✅ Q5: Best Strategy for Optimized Table in BigQuery
```sql
CREATE TABLE `platinum-lead-450019-j6.nyc_taxi_data_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS SELECT * FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`;
```
✅ **Answer:** **Partition by `tpep_dropoff_datetime`, Cluster by `VendorID`**

---

### ✅ Q6: Distinct `VendorID` Query + Bytes Read
```sql
SELECT DISTINCT VendorID 
FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
📊 **Bytes Read:**
- **Non-Partitioned Table:** `310.24 MB`
- **Partitioned Table:** `26.84 MB`
✅ **Answer:** **310.24 MB (non-partitioned), 26.84 MB (partitioned)**

🖼 **Screenshot:**
![Non-partitioned table](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_61.JPG)

🖼 **Screenshot:**
![Partitioned table](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_62.JPG)

---

### ✅ Q7: Where is the External Table Data Stored?
✅ **Answer:** **GCP Bucket**

---

### ✅ Q8: Should You Always Cluster in BigQuery?
✅ **Answer:** **False**
- **Clustering helps performance**, but **not always needed** if queries are not filtering/sorting based on clustered columns.

---

### ✅ Q9: Bytes Read for `SELECT COUNT(*)` Query
```sql
SELECT COUNT(*) FROM `platinum-lead-450019-j6.nyc_taxi_data.yellow_taxi_trips`;

🖼 **Screenshot:**
![Partitioned table](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_3/screenshots/question_9.JPG)

```
📊 **Bytes Read:**  
- **Materialized Table:** `0 MB`
✅ **Explanation:**  
- **The estimated bytes read for a SELECT COUNT(*) query on a materialized table will typically be 0 MB because BigQuery uses metadata to answer the query without scanning the data.**

---

## 📌 Summary
✅ **Successfully processed, uploaded, and queried NYC Taxi data using Google Cloud & BigQuery.**  
✅ **Implemented best practices for partitioning, clustering, and optimized queries.**  
🚀 **This setup allows efficient data processing at scale!** 🎯
