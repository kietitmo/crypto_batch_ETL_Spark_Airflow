import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago

from datetime import datetime

chat_id = Variable.get("CHAT_ID")

dag = DAG(
    dag_id = "crypto_sparking_flow",
    default_args = {
        "owner": "Kiet Nguyen",
        "start_date": days_ago(1),
        # "on_failure_callback":
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

send_message = TelegramOperator(
        task_id='send_message',
        telegram_conn_id='telegram-conn',  # Ensure this connection is set up in Airflow
        chat_id= chat_id,
        text = f'''
        **Hello from Airflow! 
        - Dag: crypto_sparking_flow
        - Time: {datetime.today()}
        - FAILURE TO EXECUTE.''',

        dag=dag,
        trigger_rule='one_failed'
    )

[start >> [fetch_binance, fetch_bybit, fetch_bingX] >> end] >> send_message