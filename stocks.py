import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def create_portfolio_sheet(tickers):
    end_date = datetime.today()
    start_date = start_dates["10Y"]
    close_df = pd.DataFrame()

    for ticker in tickers:
        data = yf.download(ticker,start=start_date,end=end_date)
        close_df[ticker] = data["Close"]

    output_folder = r"{}".format(os.getcwd())
    output_file = os.path.join(output_folder, "portfolio_history.xlsx")
    close_df.to_excel(output_file)

def get_start_date(num_days):
    return datetime.today() - timedelta(days = num_days)

def get_stock(ticker:str,time_frame:str):
    end_date = datetime.today()
    start_date = start_dates[time_frame]
    close_df = pd.DataFrame()

    data = yf.download(ticker,start=start_date,end=end_date)
    close_df[ticker] = data["Close"]
    return close_df

def get_ytd():
    year = str(datetime.today().year)
    return year + "-1-1"

start_dates = {"1D":get_start_date(1),
               "1W":get_start_date(7),
               "1M":get_start_date(30),
               "6M":get_start_date(180),
               "YTD":get_ytd(),
               "1Y":get_start_date(365),
               "2Y":get_start_date(730),
               "5Y":get_start_date(1826),
               "10Y":get_start_date(3652)}

# TEST:
# tickers = ["AAPL","KO","TSLA"]
# create_portfolio_sheet(tickers)

# print(get_stock("AAPL","1W"))