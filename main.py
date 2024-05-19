import streamlit as st
from icecream import ic
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
import os
from dotenv import load_dotenv
from iexfinance.refdata import get_symbols
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock

from datetime import datetime, timedelta
import pandas as pd
from pyspark.sql.types import DoubleType, StringType, TimestampType
from chart import *
from helper import *


# spark = get_or_create_spark_session()
# load_dotenv()
# API_KEY = os.environ.get("apikey")

try:
    st.title("Stock Management Web-app")

    sym = st.selectbox("Choose a company from where to retrieve data:", symbol_lst())
    stock_data = get_stock_data(sym)

    if stock_data:
        # st.write(stock_data)
        plot_candlestick(stock_data.toPandas())
        # stock_data_piv = (stock_data.toPandas()).pivot(index='symbol', columns='priceDate', values='close')
        histogram(stock_data.toPandas(), "priceDate","close")
    st.write("IEX Cloud (linked to https://iexcloud.io)")

except Exception as e:
    st.error(f"Error:{e}")
