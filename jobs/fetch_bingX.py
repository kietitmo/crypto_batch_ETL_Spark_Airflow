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

res = requests.get(f'https://open-api.bingx.com/openApi/swap/v3/quote/klines?symbol=BTC-USDT&interval=5m&startTime={start_of_yesterday_timestamp}&endTime={end_of_yesterday_timestamp}')
response = json.loads(res.text)

data = response['data']


from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName('spark-app-fetch-from-bybit') \
    .master("local[*]") \
    .getOrCreate()


dataframe = spark.createDataFrame(data)\
                .withColumnRenamed('open', 'Open_price')\
                .withColumnRenamed('close', 'Close_price')\
                .withColumnRenamed('high', 'High_price')\
                .withColumnRenamed('low', 'Low_price')\
                .withColumnRenamed('time', 'Open_time')\
                .withColumnRenamed('volume', 'Volume')

# Using filter because in this df contain data of at 0h0m0s next day 
dataframe = dataframe.filter(dataframe.Open_time < end_of_yesterday_timestamp)\
                    .orderBy(['Open_time'], ascending=[True])
dataframe.show()

date= str(start_of_yesterday).split(' ')[0]
dataframe.repartition(2).write.parquet(f'hdfs://namenode:8020/home/datalake/BTCUSDT_klines/bingX/{date}', mode='overwrite')