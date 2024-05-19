import streamlit as st
import pandas as pd
import plotly.express as px


"""charts"""
warn = "⚠️"


def error_XequY():
    return st.error("Please choose a X value different than Y", icon=warn)


def pie(data, x, y):
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    """create a pie chart"""
    if x_dtype in ["float64", "int64", "datetime64[ns]"]:
        st.error("X should always be a string (category)", icon=warn)
    elif y_dtype == "object":
        st.error("Y should always be a number (value)", icon=warn)
    elif x == y:
        error_XequY()
    elif x_dtype == "object" and y_dtype == "object":
        st.error("X and Y cannot be both of type string (category)", icon=warn)
    else:
        fig = px.pie(data, names=x, values=y)
        st.plotly_chart(fig)


def line_plot(data, x, y):
    """create a line plot"""
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    if x_dtype not in ["float64", "int64", "datetime64[ns]"]:
        st.error(
            "X should be a numeric variable for a line plot.",
            icon=warn,
        )
    elif y_dtype not in ["float64", "int64", "datetime64[ns]"]:
        st.error("Y should be a numeric variable for a line plot.", icon=warn)
    else:
        st.line_chart(data, x=x, y=y)


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
        st.plotly_chart(fig, use_container_width=True)


def boxplot(data, x, y):
    """create boxplot chart"""
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    if x_dtype != "str" or y_dtype == "str":
        st.error(
            "X should be a categorical variable and Y should be a numeric variable for a boxplot",
            icon=warn,
        )
    elif x == y:
        error_XequY()
    else:
        fig = px.box(data, x=x, y=y, points="all")
        st.plotly_chart(fig)


def bar_plot(data, x, y):
    """create bar plot"""
    x_dtype = data.select(x).dtypes[0][1]
    y_dtype = data.select(y).dtypes[0][1]
    if x_dtype != "string" or y_dtype == "string":
        st.error(
            "X should be a categorical variable and Y should be a numeric variable for a bar plot",
            icon=warn,
        )
    else:
        pandas_df = data.select(x, y).toPandas()
        st.bar_chart(pandas_df)



def kde_plot(data, x, y):
    """create kde plot"""
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    if x_dtype == "str" or y_dtype == "str":
        st.error(
            "X and Y should be numeric variable for a KDE plot",
            icon=warn,
        )
    elif x == y:
        error_XequY()
    else:
        fig = px.density_contour(data, x=x, y=y)
        st.plotly_chart(fig)


def scatter_chart(data, x, y):
    """create scatter chart"""
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    if x_dtype == "str" or y_dtype == "str":
        st.error(
            "X and Y should be numeric variable for a scatter plot",
            icon=warn,
        )
    elif x == y:
        error_XequY()
    else:
        st.scatter_chart(data, x=x, y=y)


def violin_plot(data, x, y):
    """create violin plot"""
    x_dtype = data[x].dtype
    y_dtype = data[y].dtype
    if x_dtype != "object" or y_dtype == "object":
        st.error(
            "X should be a categorical variable and Y should be a numeric variable for a violin plot",
            icon=warn,
        )
    elif x == y:
        error_XequY()
    else:
        fig = px.violin(data, x=x, y=y)
        st.plotly_chart(fig)


def heatmap(data):
    """create heatmap"""
    fig = px.imshow(data)
    st.plotly_chart(fig, theme="streamlit")
