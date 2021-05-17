import requests
import dash
import pandas as pd

url = "https://yahoo-finance-low-latency.p.rapidapi.com/v8/finance/chart/AAPL"

querystring = {"events":"div,split"}

headers = {
    'x-rapidapi-key': "58dd54d54amsh8adbafe422f4dbfp1bc21djsn1137a529195e",
    'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)