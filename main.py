import streamlit as st

# import pandas as pd
# import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan, when, count
import os
from dotenv import load_dotenv
from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from datetime import datetime
import requests


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
    """get stock data from api by period of time"""
    today = datetime.now()
    start = datetime(today.year, 1, 1)
    end = datetime(today.year, today.month, today.day)

    try:
        start, end = st.date_input(
            "Select an interval",
            [start, end],
            format="MM/DD/YYYY",
        )
    except:
        st.error(
            f"Please select a valid date range, Start and end dates must be before current date",
            icon="📆",
        )
    df = get_historical_data(symbol, start, end, token=API_KEY)
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].astype(float)
    df_pyspark = spark.createDataFrame(df)
    cleaned_df = df_pyspark.na.drop()
    print(
        cleaned_df.select(
            [
                count(when(isnan(c) | col(c).isNull(), c)).alias(c)
                for c in cleaned_df.columns
            ]
        ).show()
    )
    return cleaned_df


st.title("Stock management Web-app")

sym = st.selectbox(
    "Choose a company from where to retrieve data :", get_symbols(token=API_KEY)
)
st.write(get_stock_data(sym))
