import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime
"""charts"""
warn = "⚠️"


def error_XequY():
    return st.error("Please choose a X value different than Y", icon=warn)


def histogram(data, x, y=None):
    """create histogram chart"""
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    if x == y:
        error_XequY()
    elif x_dtype == "object":
        st.error("X should be a numeric variable for an histogram", icon=warn)
    elif y and y_dtype == "object":
        st.error("Y should be a numeric variable for an histogram", icon=warn)
    else:
        if y:
            fig = px.histogram(data, x=x, y=y)
        else:
            fig = px.histogram(data, x=x)
        fig.update_xaxes(title_text="Stock")
        fig.update_yaxes(title_text="Date")
        st.plotly_chart(fig, use_container_width=True)


def plot_candlestick(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Convert the 'priceDate' column to datetime
    data['priceDate'] = pd.to_datetime(data['priceDate'], format="%Y-%m-%d %H:%M:%S")

    # Extract the date part only
    only_date = data['priceDate'].dt.date

    fig.add_trace(go.Candlestick(
        x=only_date,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='Candlesticks'
    ))

    fig.update_layout(
        title='Candlestick Chart with Volume',
        xaxis_title='Stock',
        yaxis_title='Date'
    )

    st.plotly_chart(fig)