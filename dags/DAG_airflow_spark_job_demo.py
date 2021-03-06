from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import os

srcDir = os.getcwd() + '/dags/src/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2016, 10, 14, 16, 12),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

with DAG('DAG_airflow_spark_job_demo', default_args=default_args, schedule_interval=timedelta(seconds=45)) as dag:

    start_dag = DummyOperator(task_id='START_dag')
    spark_job= BashOperator(
        task_id='spark-job-run',
        bash_command='python ' + srcDir + 'pyspark_demo.py ',
        dag=dag)
    spark_ml_job= BashOperator(
        task_id='spark-ml_job-run',
        bash_command='python ' + srcDir + 'Spark_ML_LinearRegression_demo.py ',
        dag=dag)
    end_dag = DummyOperator(task_id='END_dag')

    start_dag >> spark_job >> spark_ml_job >> end_dag
