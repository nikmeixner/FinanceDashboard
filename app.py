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
from dash.exceptions import PreventUpdate

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
                    className="dropdownClass",
                    options= [
                    {"label": "Palantir", "value": "PLTR"},
                    {"label": "Nio", "value": "NIO"},
                    {"label": "Nel Asa", "value": "NLLSF"}],
                    multi = False,
                    value = "PLTR",
                    style={ 'background-color': '#212121',
                            'border-color': "#17d0b7",
                                    } ,

        ),
        html.Div([
            html.H2("Chart"),
            html.Div([
                html.P(id="p_timespan",children="Timespan"),
                dcc.Dropdown(
                            className="dropdownClass",
                            id = "time",
                            options= [
                            {"label": "1 Day", "value": "1d"},
                            {"label": "1 Month", "value": "1mo"},
                            {"label": "1 Year", "value": "1y"},
                            {"label": "YTD", "value": "ytd"}],
                            multi = False,
                            value = "1y",
                            style={ 'background-color': '#212121',
                                    'border-color': "#17d0b7",
                                            },
                ),
                html.P(id="p_intervall", children="Intevall"),
                dcc.Dropdown(
                            id = "intervall",
                            className="dropdownClass",
                            options= [
                            {"label": "1 Minute", "value": "1m"},
                            {"label": "1 Hour", "value": "1h"},
                            {"label": "1 Day", "value": "1d"},
                            {"label": "1 Month", "value": "1mo"}],
                            multi = False,
                            value = "1h",
                            style={ 'background-color': '#212121',
                                    'border-color': "#17d0b7",
                                            },
            )], id="Chart_Dropdown_Container2"),
        ], id="Chart_Dropdown_Container"),
        ],id="dropdowns"),
    html.Div([
        html.P(children="Current Price: "),
        html.P(className="dynamic_stock_data", id="cp"),
        html.P(children="Market Cap: "),
        html.P(className="dynamic_stock_data", id="mc", children=""),
        html.P(children="Float: "),
        html.P(className="dynamic_stock_data", id="ff", children=""),
        html.P(children="Short Volume: "),
        html.P(className="dynamic_stock_data", id="sv", children=""),
        html.P(children="Short Ratio: "),
        html.P(className="dynamic_stock_data", id="sr", children=""),
        html.P(children="Ebitda: "),
        html.P(className="dynamic_stock_data", id="eb", children=""),
    ], id="stock_data_container"),
    html.Div([
            html.P(id="ticker_name"),
            html.Img(id="ticker_logo"),
            html.P(id="ticker_desc"),
        ], id = "company_data_container"),
    ], id="grid_container"),
    html.Div([
    dcc.Graph(
        id="time-series-chart",),
    ], id="graph_container"),
    html.Div([
        html.H1(children="Extended Company Data"),
        html.Div([
            html.P(children="52 Week Change: "),
            html.P(id="52v", children="Value"),
            html.P(children="Enterprise to Ebitda: "),
            html.P(id="EtEv", children="Value"),
            html.P(children="Enterprise to Revenue: "),
            html.P(id="EtRv", children="Value"),
            html.P(children="Profit Margins: "),
            html.P(id="PMv", children="Value"),
            html.P(children="Average Daily Volume 3 Months: "),
            html.P(id="adv3mv", children="Value"),
            html.P(children="Average Daily Volume 10 Days: "),
            html.P(id="adv10dv", children="Value"),
            html.P(children="Revenue Growth: "),
            html.P(id="rgv", children="Value"),
            html.P(children="Operating Cashflow: "),
            html.P(id="opcv", children="Value"),
            html.P(children="Free Cashflow: "),
            html.P(id="fcv", children="Value"),
            html.P(children="Total Revenue"),
            html.P(id="trv", children="Value"),
            html.P(children="Estimated earnings previous Q: "),
            html.P(id="eepqv", children="Value"),
            html.P(children="Actual earnings previous Q: "),
            html.P(id="aepqv", children="Value"),
            html.P(children="Recommendation: "),
            html.P(id="rv", children="Value"),
    ], id="inner_extended_company_data_container"),
    ], id="extended_company_data_container"),
    html.Div([
        html.H1(children="News"),
            html.Div([
                html.Div([
                    html.H3(id="news1_p", children=""),
                    html.P(id="desc1_p", children=""),
                    html.A(id="url1_p", children="Link"),
                ], id="article1"),
                html.Div([
                    html.H3(id="news2_p", children=""),
                    html.P(id="desc2_p", children=""),
                    html.A(id="url2_p", children="Link"),
                ],id="article2"),
                html.Div([
                    html.H3(id="news3_p", children=""),
                    html.P(id="desc3_p", children=""),
                    html.A(id="url3_p", children="Link"),
                ],id="article3"),
                html.Div([
                    html.H3(id="news4_p", children=""),
                    html.P(id="desc4_p", children=""),
                    html.A(id="url4_p", children="Link"),
                ],id="article4"),
        ], id="inner_news_container"),
    ], id="news_container"),
], id="grid_container_uno")

#-----------------------------------------------------


##--------------------------------------------------------
##Callback for Stock Data
# current Price != previousClose
@app.callback(
    [Output("cp", "children"),
    Output("mc", "children"),
    Output("ff", "children"),
    Output("sv", "children"),
    Output("sr", "children"),
    Output("eb", "children")],
    [Input("ticker", "value")])
#Function for updating Stock Data
def update_stock_data(ticker):
    stock_data = yf.download(ticker)
    daf = stock_data
    company = yf.Ticker(ticker)
    info = company.info
    cd = pd.DataFrame().from_dict(info, orient="index").T
    previousClose = cd[["previousClose"]].values[0]
    marketCap = cd[["marketCap"]].values[0]
    SharesShort = cd[['sharesShort']].values[0]
    #heldPercentageInstitutions = cd[['heldPercentInstitutions']].values[0]
    shortRatio = cd[['shortRatio']].values[0]
    floatShare = cd[['floatShares']].values[0]
    #impliedSharesOutstanding = cd[['impliedSharesOutstanding']].values[0]
    ebitda = cd[['enterpriseToEbitda']].values[0]
    return previousClose, marketCap, floatShare, SharesShort, shortRatio, ebitda   
#-----------------------------------------------------
#Callback für Live-Price

#-----------------------------------------------------
# Callback for Dropdown & Chart
@app.callback(
    [Output("time-series-chart", "figure"),
    Output("ticker_name", "children"),
    Output("ticker_logo", "src"),
    Output("ticker_desc", "children")],
    [Input("ticker", "value"),
    Input("time", "value"),
    Input("intervall", "value")])
# Function for updating Chart & Dropdowns
def update_data(ticker, time, intervall):
    data = yf.download(ticker, period = time, interval = intervall)
    df = data
    date = get_number_of_time(ticker, time, intervall)
    company = yf.Ticker(ticker)
    info = company.info

    #company data
    cd = pd.DataFrame().from_dict(info, orient="index").T
    cd = cd[["logo_url", "shortName", "longBusinessSummary"]]
    ls = cd["longBusinessSummary"].values[0]
    lu = cd["logo_url"].values[0]
    sn = cd["shortName"].values[0]

    #stock data

    
    fig = px.line(df, 
        x=date, 
        y="Close", 
        color_discrete_map={"": '#ff1178'},
        template="plotly_dark").update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#17d0b7'),
            yaxis=dict(
                showline=True,
                showticklabels=True,
                linecolor='#17d0b7'),
                )
    return fig, sn, lu, ls

#--------------------------------------------------------
#Callback für Extended Company Data
@app.callback(
    [Output("52v", "children"),
    Output("EtEv", "children"),
    Output("EtRv", "children"),
    Output("PMv", "children"),
    Output("adv3mv", "children"),
    Output("adv10dv", "children"),
    Output("rgv", "children"),
    Output("opcv", "children"),
    Output("fcv", "children"),
    Output("trv", "children"),
    Output("rv", "children"),],
    Input("ticker", "value")
)

def update_extendedc_data(ticker):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

    querystring = {"symbol":f"{ticker}"}

    headers = {
        'x-rapidapi-key': "58dd54d54amsh8adbafe422f4dbfp1bc21djsn1137a529195e",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    cd = response.json()
    #defaultdata
    etrv = cd["defaultKeyStatistics"]['enterpriseToRevenue']['fmt']
    etev =cd["defaultKeyStatistics"]['enterpriseToEbitda']['fmt']
    pmv = cd["defaultKeyStatistics"]['profitMargins']['fmt']
    oycv = cd["defaultKeyStatistics"]['52WeekChange']['fmt']

    #Trading Volume Data
    adv3mv =  cd["price"]["averageDailyVolume3Month"]['fmt']
    adv10dv = cd["price"]["averageDailyVolume10Day"]['fmt']

    #financial Data
    rgv =  cd["financialData"]["revenueGrowth"]['fmt']
    opcv =  cd["financialData"]["operatingCashflow"]['fmt']
    fcv = cd["financialData"]["freeCashflow"]['fmt']
    trv = cd["financialData"]["totalRevenue"]['fmt']
    rv = cd["financialData"]["recommendationKey"]

    #earning data
    eepqv = cd["earnings"]['earningsChart']['quarterly'][-1]['estimate']['fmt']
    aepqv = cd["earnings"]['earningsChart']['quarterly'][-1]['actual']['fmt']


    return oycv, etev, etrv, pmv, adv3mv, adv3mv, rgv, opcv, fcv, trv, rv

#--------------------------------------------------------------------------------
#update for earnings
@app.callback(
    [Output("eepqv", "children"),
    Output("aepqv", "children")],
    Input("ticker", "value")
)

def update_earnings(ticker):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

    querystring = {"symbol":f"{ticker}"}

    headers = {
        'x-rapidapi-key': "58dd54d54amsh8adbafe422f4dbfp1bc21djsn1137a529195e",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    cd = response.json()
    if (ticker == "NLLSF"):
        raise PreventUpdate
    eepqv = cd["earnings"]['earningsChart']['quarterly'][-1]['estimate']['fmt']
    aepqv = cd["earnings"]['earningsChart']['quarterly'][-1]['actual']['fmt']

    return eepqv, aepqv



#--------------------------------------------------------
#Callback für News
@app.callback(
    [Output("news1_p", "children"),
    Output("news2_p", "children"),
    Output("news3_p", "children"),
    Output("news4_p", "children"),
    Output("desc1_p", "children"),
    Output("desc2_p", "children"),
    Output("desc3_p", "children"),
    Output("desc4_p", "children"),
    Output("url1_p", "href"),
    Output("url2_p", "href"),
    Output("url3_p", "href"),
    Output("url4_p", "href")],
    Input("ticker", "value")
)
#get News, get Titels & URLs, Show x number of Titles + Urls for further research
def update_news(ticker):
    if (ticker == "NLLSF"):
            ticker = "Nel Asa"
    url = (f'https://newsapi.org/v2/everything?q= {ticker} &'
       'from= {today} &'
       'language=en&'
       'sortBy=relevancy&'
       'apiKey=275e219645414cb6b0595d7db588ae9b')

    response = requests.get(url).json()

    title_list=[]
    desc_list=[]
    url_list=[]

    for i in response["articles"]:
            titles = i["title"]
            title_list.append(titles)
            descs = i["description"]
            desc_list.append(descs)
            urls = i["url"]
            url_list.append(urls)

    return title_list[0], title_list[1], title_list[2], title_list[3], desc_list[0], desc_list[1], desc_list[2], desc_list[3], url_list[0], url_list[1], url_list[2], url_list[3]



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