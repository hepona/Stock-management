from chart import *
from statistics import median, mean, mode
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import DoubleType
import re
from pyspark.sql import SparkSession
from iexfinance.refdata import get_symbols

from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from icecream import ic


@st.cache_resource
def get_or_create_spark_session():
    """Creates or retrieves a cached SparkSession"""
    if "spark_session" not in st.session_state:
        spark = SparkSession.builder.appName("StockApp").getOrCreate()
        st.session_state["spark_session"] = spark
    return st.session_state["spark_session"]


load_dotenv()
API_KEY = os.environ.get("apikey")
spark = get_or_create_spark_session()


def fix_coltype(df):
    """Fix column types in a Spark DataFrame."""
    for col_name in df.columns:
        sample_value = df.select(col_name).head()[0]

        if sample_value is None:
            continue
        if re.match(r"^-?\d+(\.\d+)?$", str(sample_value)):
            try:
                df = df.withColumn(col_name, col(col_name).cast(DoubleType()))
                print(f"{col_name} modified to double")
            except:
                pass
        elif re.match(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$", str(sample_value)):
            try:
                df = df.withColumn(col_name, to_timestamp(col(col_name)))
                print(f"{col_name} modified to timestamp")
            except:
                pass

    return df


def get_stock_data(symbol):
    """Get stock data from API by period of time"""
    today = datetime.now()
    start = datetime(today.year, 1, 1)
    end = datetime(today.year, today.month, today.day)

    try:
        start, end = st.date_input(
            "Select an interval",
            [start, end],
            format="MM/DD/YYYY",
        )
    except Exception as e:
        st.error(
            f"Start and end dates must be before the current date: {e}",
            icon="📆",
        )
        return

    df = get_historical_data(symbol, start, end, token=API_KEY, output_format="pandas")
    ic(df.dtypes)
    df = df.dropna()
    df = df.astype(str)
    df_pyspark = spark.createDataFrame(df)
    df_pyspark = fix_coltype(df_pyspark)
    ic(df_pyspark.dtypes)

    return df_pyspark


@st.cache_data
def symbol_lst():
    """retrieve all symbols from iexcloud"""
    return get_symbols(token=API_KEY)
