import streamlit as st
from icecream import ic
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
import os
from dotenv import load_dotenv
from iexfinance.refdata import get_symbols
from iexfinance.stocks import get_historical_data
from datetime import datetime
import pandas as pd
from pyspark.sql.types import DoubleType, StringType, TimestampType
from pyspark.sql import functions as F
from chart import *
from helper import *


@st.cache_resource
def get_or_create_spark_session():
    """Creates or retrieves a cached SparkSession"""
    if "spark_session" not in st.session_state:
        spark = SparkSession.builder.appName("StockApp").getOrCreate()
        st.session_state["spark_session"] = spark
    return st.session_state["spark_session"]


spark = get_or_create_spark_session()
load_dotenv()
API_KEY = os.environ.get("apikey")


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
            f"Please select a valid date range. Start and end dates must be before the current date: {e}",
            icon="📆",
        )
        return

    df = get_historical_data(symbol, start, end, token=API_KEY, output_format="pandas")
    ic(df.dtypes)
    df = df.dropna()
    df = df.astype(str)
    df = fix_coltype(df)
    df_pyspark = spark.createDataFrame(df)
    ic(df_pyspark.dtypes)

    return df_pyspark


st.title("Stock Management Web-app")


@st.cache_data
def symbol_lst():
    return get_symbols(token=API_KEY)


sym = st.selectbox("Choose a company from where to retrieve data:", symbol_lst())
stock_data = get_stock_data(sym)
if stock_data:
    st.write(stock_data)
bar_plot(stock_data, "symbol", "volume")
