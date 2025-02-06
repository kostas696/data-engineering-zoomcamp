## 🚀 **Workflow Orchestration & ETL Pipeline - Kestra & GCP**
This repository contains our **Kestra workflow** and **BigQuery ETL pipeline** for processing **NYC Taxi data** and answering key quiz questions. The workflow orchestrates data ingestion, transformation, and loading into **Google Cloud Storage (GCS)** and **BigQuery**.

---

## 📌 **Quiz Questions & Answers**

### **1️⃣ What is the uncompressed file size of `yellow_tripdata_2020-12.csv`?**
✅ **Answer:** **128.3 MB**

🖼 **Screenshot:**
![Yellow Taxi December 2020 File Size](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_2/screenshots/question1.PNG)

**Steps to Verify:**
1. Executed the `06_gcp_taxi.yaml` flow in **Kestra**.
2. Disable the purge-files task in the flow above and allow storing CSV.
3. Checked file metadata to confirm the size.

---

### **2️⃣ What is the rendered value of the variable `file` when taxi=`green`, year=`2020`, and month=`04`?**
✅ **Answer:** **`green_tripdata_2020-04.csv`**

**Explanation:**
- The variable template is:  
  ```yaml
  {{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv
  ```
- Given `taxi=green`, `year=2020`, `month=04`, the rendered value is:  
  **`green_tripdata_2020-04.csv`**.

---

### **3️⃣ How many rows are there for the Yellow Taxi data for all CSV files in 2020?**
✅ **Answer:** **24,648,499**

🖼 **Screenshot:**
![Yellow Taxi 2020 Row Count](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_2/screenshots/question3.JPG)

**Steps to Verify:**
1. Ran **Kestra flow** to upload data to **BigQuery**.
2. Queried the total row count in BigQuery:
   ```sql
   SELECT COUNT(*) FROM `project_id.dataset.yellow_tripdata`
   WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020;
   ```
3. Verified the result.

---

### **4️⃣ How many rows are there for the Green Taxi data for all CSV files in 2020?**
✅ **Answer:** **1,734,051**

🖼 **Screenshot:**
![Green Taxi 2020 Row Count](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_2/screenshots/question4.JPG)

**Steps to Verify:**
1. Ran **Kestra flow** to process Green Taxi data.
2. Queried BigQuery:
   ```sql
   SELECT COUNT(*) FROM `project_id.dataset.green_tripdata`
   WHERE EXTRACT(YEAR FROM lpep_pickup_datetime) = 2020;
   ```
3. Confirmed the result.

---

### **5️⃣ How many rows are there for Yellow Taxi data in March 2021?**
✅ **Answer:** **1,925,152**

🖼 **Screenshot:**
![Yellow Taxi March 2021 Row Count](https://github.com/kostas696/data-engineering-zoomcamp/blob/main/homework_2/screenshots/question5.JPG)

**Steps to Verify:**
1. Queried BigQuery:
   ```sql
   SELECT COUNT(*) FROM `project_id.dataset.yellow_tripdata`
   WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2021
   AND EXTRACT(MONTH FROM tpep_pickup_datetime) = 3;
   ```
2. Verified row count.

---

### **6️⃣ How to configure timezone to New York in a Schedule trigger?**
✅ **Answer:** **`Add a timezone property set to America/New_York`**

**Correct Configuration:**
```yaml
triggers:
  - id: daily_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: "America/New_York"
```
This ensures the trigger aligns with New York’s timezone.

---

## 🚀 **How to Run**
### **1️⃣ Setup Google Cloud**
- Enable **BigQuery** & **Cloud Storage**.
- Create a **Service Account** & download the JSON key.

### **2️⃣ Set Up Kestra**
```sh
docker-compose up -d
```
- Open **Kestra UI** at `http://localhost:8080`.

### **3️⃣ Run the ETL Pipeline**
- Execute **`06_gcp_taxi.yaml`** in **Kestra UI**.
- Run **Backfill Execution** to load all 2020 data.

### **4️⃣ Verify in BigQuery**
- Run queries to check row counts.

---

## 📌 **Key Learnings**
- **Kestra** simplifies workflow orchestration for **ETL pipelines**.
- **Google Cloud Storage (GCS)** is used as a **data lake**.
- **BigQuery** efficiently handles large-scale **taxi trip data**.
- **Backfill executions** enable processing of **historical datasets**.

---

