from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    dag_id='s3_file_check_dag',
    default_args=default_args,
    description='A simple DAG to check for an S3 file',
    schedule_interval=None,  # You can set a schedule or leave as None for manual triggering
    start_date=days_ago(1),
    catchup=False,
)

# S3 Bucket and Key details
bucket_name = 'airflow-project-bucket'  # Replace with your S3 bucket name
bucket_key = 'new-upload-1/spotify_raw_2024-11-19 21_08_59.667316.json'  # Replace with the key of the file you want to check

# S3KeySensor Task
s3_sensor = S3KeySensor(
    task_id='check_s3_key',
    bucket_name=bucket_name,
    bucket_key=bucket_key,
    aws_conn_id='aws_default',  # Make sure this connection is configured in Airflow
    poke_interval=60,  # Time between checks in seconds
    timeout=600,  # Timeout after 10 minutes
    mode='poke',  # You can also use 'reschedule' mode
    dag=dag,
)

# Example of an additional task (optional)
def process_file():
    # Code to process the file once it's available in S3
    print("File is available in S3, processing it...")

# You can add further tasks after the sensor, like processing the file
# Example of using PythonOperator to run a processing function after the sensor triggers
from airflow.operators.python_operator import PythonOperator

process_task = PythonOperator(
    task_id='process_s3_file',
    python_callable=process_file,
    dag=dag,
)

# Set task dependencies
s3_sensor >> process_task  # Process file only after S3 key is found
