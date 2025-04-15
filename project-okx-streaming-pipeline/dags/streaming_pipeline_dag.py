from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

# DAG default arguments
default_args = {
    'owner': 'soufleros_kostas',
    'retries': 1,
    'email_on_failure': False,
    'email_on_retry': False
}

# Define DAG
with DAG(
    dag_id='crypto_streaming_pipeline',
    schedule_interval='*/5 * * * *',
    start_date=days_ago(1),
    catchup=False,
    default_args=default_args,
    description='Kafka → GCS → Spark → BQ → Validation with email alert',
    tags=['streaming', 'crypto', 'spark', 'bigquery']
) as dag:

    # Spark job to transform data and load to BigQuery
    spark_transform = BashOperator(
        task_id='spark_gcs_to_bq',
        bash_command="""
        $SPARK_HOME/bin/spark-submit \
        --jars $SPARK_JARS \
        $SPARK_JOB_PATH
        """,
        env={
            "SPARK_HOME": "{{ var.value.SPARK_HOME }}",
            "SPARK_JARS": "{{ var.value.SPARK_JARS }}",
            "SPARK_JOB_PATH": "{{ var.value.SPARK_JOB_PATH }}"
        }
    )

    # Validation step to ensure BQ was loaded
    validate_bq = BashOperator(
        task_id='validate_data_in_bq',
        bash_command="python3 $VALIDATION_SCRIPT_PATH",
        env={
            "VALIDATION_SCRIPT_PATH": "{{ var.value.VALIDATION_SCRIPT_PATH }}"
        }
    )

    # Email alert if failure occurs
    email_alert = EmailOperator(
        task_id='email_on_failure',
        to='soufleros.kostas@gmail.com',
        subject='[Airflow] DAG {{ dag.dag_id }} failed!',
        html_content="""
        <p><strong>One or more tasks in DAG <code>{{ dag.dag_id }}</code> failed.</strong></p>
        <p>Check Airflow logs for details.</p>
        """,
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    # DAG dependencies
    spark_transform >> validate_bq
    [spark_transform, validate_bq] >> email_alert