#!/usr/bin/env python3
import requests
import pandas as pd
import json

# url = "https://financialmodelingprep.com/api/v3/stock/list/?apikey=FhIL1uu8SKjkLpra0v0QtXWYTFuC5LaG"
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'

response = requests.get(url)
# response.raise_for_status()  # Raise an exception for non-200 status codes
data = json.loads(response.text)
print(data)