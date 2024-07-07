from airflow import DAG
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Retrieve the chat ID from Airflow Variables
chat_id = '-4275272161'

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    # 'retries': 1,
}

def failing_task():
    return True

# Define the DAG
dag = DAG('telegram_notification_dag',
         default_args=default_args,
         schedule_interval='@daily',
         start_date=days_ago(1),
         catchup=False)

    # Task to send a message using the TelegramOperator
send_message = TelegramOperator(
        task_id='send_message',
        telegram_conn_id='telegram-conn',  # Ensure this connection is set up in Airflow
        chat_id=chat_id,
        text = '''
        Hello from Airflow! 
        Dag: crypto_sparking_flow
        FAILURE TO EXECUTE.''',

        dag=dag,
        trigger_rule='one_failed'
    )

fail_task = PythonOperator(
        task_id="failing_task", python_callable=failing_task, dag=dag
    )


[fail_task] >> send_message
