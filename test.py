#!/usr/bin/env python3
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,isnan, when, count
import pandas as pd
# sqlContext.sql("set spark.sql.shuffle.partitions=10")
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
# data = [
#     ("James","CA",np.NaN), ("Julia","",None),
#     ("Ram",None,200.0), ("Ramya","NULL",np.NAN)
# ]
# df =spark.createDataFrame(data,["name","state","number"])
# df.show()

# df.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in df.columns]
#    ).show()

# pandas_df = pd.DataFrame({
#     'A': [1, 2, 3],
#     'B': [4, 5, 6]
# })
# spark_df = spark.createDataFrame(pandas_df)
# spark_df.show()