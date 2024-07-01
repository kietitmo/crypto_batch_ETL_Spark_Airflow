import requests
import json 
import pandas as pd
from datetime import datetime, timedelta

# Get time 
now = datetime.now()

start_of_yesterday = datetime(now.year, now.month, now.day) - timedelta(days=1)

end_of_yesterday = start_of_yesterday + timedelta(hours=23, minutes=59, seconds=59)

start_of_yesterday_timestamp = int(start_of_yesterday.timestamp() * 1000)
end_of_yesterday_timestamp = int(end_of_yesterday.timestamp() * 1000)


# Get data from api of binance

res = requests.get(f'https://api-testnet.bybit.com/v5/market/kline?category=linear&symbol=BTCUSD&interval=5&start={start_of_yesterday_timestamp}&end={end_of_yesterday_timestamp}&limit=300')
response = json.loads(res.text)
data = response['result']['list']
columns = ['Open_time',
    'Open_price', 
    'High_price', 
    'Low_price', 
    'Close_price', 
    'Volume', 
    'turnover'
]

# Using spark to load in to datalake
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName('spark-app-fetch-from-bybit') \
    .getOrCreate()

dataframe = spark.createDataFrame(data, columns).drop('turnover').orderBy(['Open_time'], ascending=[True])
dataframe.show()

# Write into hdfs
date = str(start_of_yesterday).split(' ')[0]
dataframe.repartition(2) \
    .write.parquet(f'hdfs://namenode:8020/home/datalake/BTCUSDT_klines/bybit/{date}',mode='overwrite')