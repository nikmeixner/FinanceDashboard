import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import yfinance as yf
import datetime as dt
from pandas_datareader import data

pd.core.common.is_list_like = pd.api.types.is_list_like

today = dt.datetime.today().strftime('%Y-%m-%d')
hist = (dt.datetime.today()-dt.timedelta(7)).strftime('%Y-%m-%d')

df = data.DataReader('GOOG', 'yahoo', hist, today)

#--------------------------------------------------------
#Dic for x-axis

date_dict_day = {
    "1 Year": 365,
    "1y": 365,
    "1 Month": 30,
    "1mo": 30,
    "1 Week": 7,
    "1 Day": 1,
    "1d": 1
}

date_dict_hour = {
    "1 Year": 365*24,
    "1y": 365*24,
    "1 Month": 30*24,
    "1mo": 30*24,
    "1 Week": 7*24,
    "1 Day": 1*24,
    "1d": 1*24,
    "1 Hour": 1*1,
    "1h": 1*1,
}

date_dict_minute = {
    "1 Month": 30*24*60,
    "1mo": 30*24*60,
    "1 Week": 7*24*60,
    "1 Day": 1*24*60,
    "1d": 1*24*60,
    "1 Hour": 1*1*60,
    "1h": 1*1*60,
    "1m": 1*1*1
}

#----------------------------------------------------------


def get_x_axis(time, intervall):
    date = []
    if (intervall == "1d"):
        xtime = date_dict_day[time]
        xintervall = date_dict_day[intervall]
        
    if (intervall == "1h"):
        xtime = date_dict_hour[time]
        xintervall = date_dict_hour[intervall]

    if (intervall == "1m"):
        xtime = date_dict_minute[time]
        xintervall = date_dict_minute[intervall]

    x = int(xtime) / int(xintervall)
    y = int(x)
    r = y*xintervall
    #for i in range (0,y):
    #    t = i*xintervall+1
    #    date.append(t)
    return r
    
