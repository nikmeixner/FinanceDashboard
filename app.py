import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import yfinance as yf
from pandas_datareader import data
import datetime as dt

#-----------------------------------------------------
external_stylesheets = ["style.css"]
df = px.data.stocks()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#make data.Datareader work
pd.core.common.is_list_like = pd.api.types.is_list_like
#-----------------------------------------------------


#-----------------------------------------------------
# Layout Elements
app.layout = html.Div([
    html.H1("Dashboard"),
    html.Div([
    html.Div([
        html.H2("Stock"),
        dcc.Dropdown(
                    id = "ticker",
                    options= [
                    {"label": "Palantir", "value": "PLTR"},
                    {"label": "Nio", "value": "NIO"},
                    {"label": "Nel Asa", "value": "NEL.OL"}],
                    multi = False,
                    value = "PLTR",
        ),
        html.Div([
            html.H2("Chart"),
        dcc.Dropdown(
                    children="Timeframe",
                    title="Timeframe",
                    id = "time",
                    options= [
                    {"label": "1 Day", "value": "1d"},
                    {"label": "1 Month", "value": "1mo"},
                    {"label": "1 Year", "value": "1y"},
                    {"label": "YTD", "value": "ytd"}],
                    multi = False,
                    value = "1mo",
        ),
        dcc.Dropdown(
                    id = "intervall",
                    options= [
                    {"label": "1 Minute", "value": "1m"},
                    {"label": "1 Hour", "value": "1h"},
                    {"label": "1 Day", "value": "1d"},
                    {"label": "1 Month", "value": "1mo"}],
                    multi = False,
                    value = "1d",
        )], id="Chart_Dropdown_Container"),
        ],id="dropdowns"),
    html.Div([
        html.P(children="Current Price:"),
        html.P(children="Market Cap:"),
        html.P(children="Free Float/ Float:"),
        html.P(children="Short Volume:"),
        html.P(children="Short Ratio:"),
        html.P(children="Short Volume:"),
    ], id="stock_data_container"),
    html.Div([
            html.P(id="ticker_name"),
            html.Img(id="ticker_logo"),
            html.P(id="ticker_desc"),
        ], id = "company_data_container"),
    ], id="grid_container"),
    html.Div([
    dcc.Graph(id="time-series-chart"),
    ], id="graph_container"),
], id="grid_container_uno")

#-----------------------------------------------------


#-----------------------------------------------------
# Callback for Dropdown
@app.callback(
    [Output("time-series-chart", "figure"),
    Output("ticker_name", "children"),
    Output("ticker_logo", "src"),
    Output("ticker_desc", "children")],
    [Input("ticker", "value"),
    Input("time", "value"),
    Input("intervall", "value")])

def update_data(ticker, time, intervall):
    data = yf.download(ticker, period = time, interval = intervall)
    df = data
    date = get_number_of_time(ticker, time, intervall)
    company = yf.Ticker(ticker)
    info = company.info
    
    #cd hat richtige Daten aber kann nicht returned werden weil Tuple nicht serializable in JSON sind
    cd = pd.DataFrame().from_dict(info, orient="index").T
    cd = cd[["logo_url", "shortName", "longBusinessSummary"]]
    ls = cd["longBusinessSummary"].values[0]
    lu = cd["logo_url"].values[0]
    sn = cd["shortName"].values[0]
    
    fig = px.line(df, x=date, y="Close")
    return fig, sn, lu, ls

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

#--------------------------------------------------------

#--------------------------------------------------------
# X-Axis

def get_number_of_time(ticker, time, intervall):
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
    time_count = y * xintervall
    get_dates(ticker, time_count)

def get_dates(ticker, time_count):
    #get today date
    today = dt.datetime.today().strftime('%Y-%m-%d')
    #get history date 
    #difference between days, hours, etc?
    hist = (dt.datetime.today()-dt.timedelta(time_count)).strftime('%Y-%m-%d')

    df = data.DataReader(ticker, 'yahoo', hist, today)

app.run_server(debug=True)