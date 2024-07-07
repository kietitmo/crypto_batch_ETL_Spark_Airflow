# Getting Crypto BTC-UST K-lines from Cryptocurrency Exchange with Apache Airflow and Spark.

Using airflow to schedule spark jobs to run daily to get data about K-lines of BTC-USDT from 3 exchanges Binance, Bybit and BingX.

![pipeline](./assets/photos/pipeline.png)

### Project Structure

The DAG sparking_flow includes the following tasks:

* start: A PythonOperator that prints "Jobs started".
* fetch_binance: A SparkSubmitOperator that submits a Python Spark job to get data from Binance.
* fetch_bybit:  A SparkSubmitOperator that submits a Python Spark job to get data from Bybit.
* fetch_bingX:  A SparkSubmitOperator that submits a Python Spark job to get data from BingX.
* end: A PythonOperator that prints "Jobs completed successfully".

These tasks are executed in a sequence where the start task triggers the Spark jobs in parallel, and upon their completion, the end task is executed.

### Prerequisites

Before setting up the project, ensure you have the following:

* Docker and Docker Compose 
* Apache Airflow Docker image.
* Apache Spark Docker image and configured to work with Airflow.
* Apache Hadoop Docker image.
* Docker volumes for Airflow DAGs, logs, and Spark jobs are properly set up.

These tasks are executed in a sequence where the start task triggers the Spark jobs in parallel, and upon their completion, the end task is executed.


### Installation

To run this project using Docker, follow command:

```
$ docker-compose up -d
```

## Check if you can access

Airflow: http://localhost:8080
* username: airflow
* password: airflow

Spark Master: http://localhost:9090

Postgres - Database airflow: http://localhost:5432
* Database: airflow
* User: airflow
* Password: airflow

Hadoop HDFS
* Namnode: http://localhost:9870
* Resource manager: http://localhost:8088

### How to run a DAG to test

1. Configure spark connection acessing airflow web UI http://localhost:8080 and going to Connections

![connection-menu](./assets/photos/connection-menu.png)

2. Add Spark and Telegram connection:

![connection-add](./assets/photos/add-spark-conn.png)

![connections](./assets/photos/connections.png)

Variable for telegram connection

![vars](./assets/photos/vars.png)

3. Run DAG:

![run-dag](./assets/photos/etl_sucessful_running.png)

Failure situation -> notify to telegram:

![fail running](./assets/photos/sent_noti.png)

![fail running](./assets/photos/messages.png)

4. Check the spark application in the Spark Master web UI (http://localhost:9090)

![spark-master](./assets/photos/spark-master.png)

5. Check datalake (HDFS)

![datalake](./assets/photos/datalake.png)

![datalake](./assets/photos/datalake2.png)

![datalake](./assets/photos/datalake3.png)

![datalake](./assets/photos/datalake4.png)


