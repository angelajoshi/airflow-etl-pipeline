

# Airflow AWS S3 Integration

This project demonstrates how to use Apache Airflow with AWS S3 to monitor and process files in an S3 bucket. It shows how to use sensors like `S3KeySensor` to wait for specific files to be uploaded to an S3 bucket before triggering tasks in your DAGs.

## Table of Contents
- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Airflow Connections Configuration](#airflow-connections-configuration)
- [License](#license)

## Project Overview
This project demonstrates how to create an Apache Airflow DAG that interacts with AWS S3 using the `S3KeySensor`. The `S3KeySensor` is used to monitor an S3 bucket for a specific file (`bucket_key`). Once the file is available, it triggers downstream tasks.

### Main features:
- Use of **S3KeySensor** to wait for file presence in an S3 bucket
- Integration with AWS using **IAM credentials**
- Example of **Airflow connection** for AWS integration
- Configuration of **AWS secret keys** and region via Airflow Connections

## Requirements
- Apache Airflow (version 2.x or later)
- Python 3.x
- AWS account with an S3 bucket
- Boto3 for AWS SDK
- Pandas (for data processing, optional)
- Spotipy (optional, for Spotify integration)
- Pdfminer (optional, for PDF extraction)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/airflow-aws-s3-integration.git
   cd airflow-aws-s3-integration
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv airflow_env
   source airflow_env/bin/activate
   ```

3. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` includes:
   - apache-airflow
   - apache-airflow-providers-amazon
   - boto3
   - pandas
   - spotipy (optional)
   - pdfminer (optional)

## Setup

1. **Airflow Setup:**

   - Initialize the Airflow database if this is your first time using Airflow:

     ```bash
     airflow db init
     ```

2. **Configure AWS credentials:**

   - Add AWS credentials in the Airflow Connections UI or via the command line:

     ```bash
     airflow connections add 'aws_default' \
         --conn-type 'aws' \
         --conn-extra '{"aws_access_key_id": "YOUR_AWS_ACCESS_KEY", "aws_secret_access_key": "YOUR_AWS_SECRET_KEY", "region_name": "us-east-1"}'
     ```

   Alternatively, you can set environment variables directly:

   ```bash
   export AWS_ACCESS_KEY_ID='YOUR_AWS_ACCESS_KEY'
   export AWS_SECRET_ACCESS_KEY='YOUR_AWS_SECRET_KEY'
   export AWS_DEFAULT_REGION='us-east-1'
   ```

3. **Create the S3 bucket:**

   Make sure you have an S3 bucket in your AWS account. You can create one in the AWS console or use the AWS CLI.

4. **Add a sample DAG:**

   Example DAG files like `new.py` are located in the `dags` folder. These files contain logic that listens for new files in the specified S3 bucket.

   Sample DAG (`new.py`):

   ```python
   from airflow import DAG
   from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
   from airflow.operators.dummy_operator import DummyOperator
   from datetime import datetime

   # Define default_args for the DAG
   default_args = {
       'owner': 'airflow',
       'start_date': datetime(2025, 1, 24),
       'retries': 1
   }

   # Create a DAG
   with DAG('aws_s3_sensor_example', default_args=default_args, schedule_interval=None) as dag:
       # Define tasks
       start_task = DummyOperator(task_id='start')

       # S3KeySensor to wait for the presence of a file in the S3 bucket
       s3_sensor = S3KeySensor(
           task_id='check_s3_file',
           bucket_name='your-s3-bucket-name',
           bucket_key='your-file-path/',  # the file or prefix to monitor
           aws_conn_id='aws_default',  # the connection ID to your AWS credentials
           poke_interval=30,  # interval in seconds between checks
           timeout=600  # maximum time to wait for the file
       )

       # Define task order
       start_task >> s3_sensor
   ```

## Usage

1. **Start the Airflow web server:**

   ```bash
   airflow webserver --port 8080
   ```

2. **Start the Airflow scheduler:**

   ```bash
   airflow scheduler
   ```

3. **Access the Airflow UI:**
   Open your browser and go to `http://localhost:8080`. You should be able to see your DAG listed there. Trigger the DAG manually or set a schedule interval to run it automatically.

4. **Monitor S3 sensor task:**
   The task `check_s3_file` will run periodically and monitor the specified S3 bucket (`bucket_name`) and file path (`bucket_key`). Once the file is available, the task will trigger the downstream task.

## Airflow Connections Configuration

- **AWS Connection**:
  Airflow uses connections to interact with external systems, such as AWS. Make sure your connection (`aws_default`) is configured correctly to access S3.

  To set it up via CLI, use the following:

  ```bash
  airflow connections add 'aws_default' \
      --conn-type 'aws' \
      --conn-extra '{"aws_access_key_id": "YOUR_AWS_ACCESS_KEY", "aws_secret_access_key": "YOUR_AWS_SECRET_KEY", "region_name": "us-east-1"}'
  ```

  Alternatively, you can configure the connection via the UI by navigating to **Admin > Connections** and creating a new AWS connection.

