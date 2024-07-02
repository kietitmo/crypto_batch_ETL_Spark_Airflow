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

res = requests.get(f'https://api1.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&startTime={start_of_yesterday_timestamp}&endTime={end_of_yesterday_timestamp}')
response = json.loads(res.text)

columns=[
    'Open_time',
    'Open_price',
    'High_price',
    'Low_price',
    'Close_price',
    'Volume',
    'Close_time',
    'Quote_asset_volume',
    'Number_of_trades',
    'Taker_buy_base_asset_volume',
    'Taker_buy_quote_asset_volume',
    'Unused_field_ignore'
]

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import *

# Using spark to save data into datalake (hdfs)

spark = SparkSession.builder \
    .appName('spark-app-fetch-from-binance') \
    .getOrCreate()

dataframe = spark.createDataFrame(response, columns).select(['Open_time', 'Open_price', 'High_price', 'Low_price', 'Close_price', 'Volume'])
dataframe.show()

date= str(start_of_yesterday).split(' ')[0]
dataframe.repartition(2).write.parquet(f'hdfs://namenode:8020/home/datalake/BTCUSDT_klines/binance/{date}', mode='overwrite')


