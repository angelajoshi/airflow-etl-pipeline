

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

Here's a sample **README** file for setting up Apache Airflow on Ubuntu (WSL) using a virtual environment. You can use this for your GitHub repository to guide others through the installation process.

---










# Apache Airflow Setup on Ubuntu (WSL)

This README describes how to set up Apache Airflow in a virtual environment on Ubuntu through **Windows Subsystem for Linux (WSL)**.

### Prerequisites:
- **WSL (Windows Subsystem for Linux)** installed on your machine.
- **Ubuntu** distribution installed on WSL.
- **Python 3** installed.

### Steps to Install Apache Airflow:

#### 1. **Update System Packages**
Run the following commands to update your system:
```bash
sudo apt update
sudo apt upgrade
```

#### 2. **Install PIP (Python Package Installer)**
To install Python packages, you will first need to install pip:
```bash
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install python-setuptools
sudo apt install python3-pip
```

#### 3. **Update WSL Configuration**
Make sure WSL can work properly with file mounts. Run:
```bash
sudo nano /etc/wsl.conf
```

Add the following lines to the file:
```ini
[automount]
root = /
options = "metadata"
```

Save and exit the file (`Ctrl + S`, then `Ctrl + X`).

#### 4. **Set Airflow Home Directory**
Decide on the location for your Airflow home directory. For example, you can set it to a directory under your Documents in Windows.

Run:
```bash
nano ~/.bashrc
```

Add the following line to the file:
```bash
export AIRFLOW_HOME=/mnt/c/users/YOURNAME/documents/airflow
```

Make sure to replace `YOURNAME` with your actual Windows username. Save and exit the file (`Ctrl + S`, then `Ctrl + X`).

#### 5. **Install Virtualenv**
Next, install **virtualenv** to create a Python virtual environment:
```bash
sudo apt install python3-virtualenv
```

#### 6. **Create and Activate the Virtual Environment**
Now, create a virtual environment named `airflow_env` and activate it:
```bash
virtualenv airflow_env
source airflow_env/bin/activate
```

#### 7. **Install Apache Airflow**
With the virtual environment activated, install Apache Airflow using `pip`:
```bash
pip install apache-airflow
```

#### 8. **Verify Airflow Installation**
To ensure that Airflow was installed successfully, run:
```bash
airflow info
```

If there are any errors or missing dependencies, install them as required.

#### 9. **Initialize the Airflow Database**
By default, Apache Airflow uses SQLite as its database. To initialize the Airflow database, run:
```bash
airflow db init
```

#### 10. **Start Airflow Web Server and Scheduler**
To start the Airflow web server and scheduler, run the following commands in two different terminal windows:

1. **Start the web server** (default port: 8080):
   ```bash
   airflow webserver --port 8080
   ```

2. **Start the scheduler**:
   ```bash
   airflow scheduler
   ```

#### 11. **Access Airflow Web UI**
Once the web server is running, you can access the Airflow Web UI by navigating to the following URL in your browser:
```
http://localhost:8080
```

Log in using the default credentials (user: `airflow`, password: `airflow`).

---

### Troubleshooting

- **Missing dependencies**: If `airflow info` shows missing dependencies, run the following to install them:
  ```bash
  pip install apache-airflow[extra]
  ```
  Replace `[extra]` with any additional dependencies like `[aws]` for AWS or `[postgres]` for PostgreSQL.

- **WSL Filesystem Issues**: If you encounter issues with file paths, try restarting the WSL instance or adjusting your WSL configuration.

---

### Additional Notes
- Apache Airflow runs on **Python 3.7+**, so ensure your Python version is up to date.
- Airflow's default **SQLite** database is suitable for small setups. For production use, consider configuring **PostgreSQL** or **MySQL** as the backend database.

---

By following the steps in this README, you should be able to set up Apache Airflow on your Ubuntu WSL instance and start using it for managing your workflows.




4. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   and
   ```bash
   pip install  apache-airflow apache-airflow-providers-amazon boto3  pandas   spotipy 
   ```
   
   The `requirements.txt` includes:
   - apache-airflow
   - apache-airflow-providers-amazon
   - boto3
   - pandas
   - spotipy
   
   
## Setup

1. **Configure AWS credentials:**

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


5. **Logging**
```bash
[logging]
remote_logging = True
remote_log_conn_id = aws_default  # Use the Airflow connection ID for AWS
remote_base_log_folder = s3://your-bucket-name/airflow-logs/  # Your S3 bucket path
```
config 
   
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

