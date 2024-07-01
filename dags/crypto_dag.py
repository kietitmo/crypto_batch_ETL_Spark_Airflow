import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime


dag = DAG(
    dag_id = "crypto_sparking_flow",
    default_args = {
        "owner": "Kiet Nguyen",
        "start_date": datetime(2024, 6, 29)
    },
    schedule_interval = "30 0 * * *"
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

fetch_binance = SparkSubmitOperator(
    task_id="fetch_from_binance",
    conn_id="spark-conn",
    application="jobs/fetch_binance.py",
    dag=dag
)

fetch_bybit = SparkSubmitOperator(
    task_id="fetch_from_bybit",
    conn_id="spark-conn",
    application="jobs/fetch_bybit.py",
    dag=dag
)

fetch_bingX = SparkSubmitOperator(
    task_id="fetch_from_bingX",
    conn_id="spark-conn",
    application="jobs/fetch_bingX.py",
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> [fetch_binance, fetch_bybit, fetch_bingX] >> end