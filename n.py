import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

tickers = ["AAPL","KO","TSLA"]

end_date = datetime.today()
start_date = end_date - timedelta(days = 1000 * 365)

close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start = start_date, end = end_date)
    close_df[ticker] = data["Close"]
    
print(close_df)

output_folder = r"{}".format(os.getcwd())
output_file = os.path.join(output_folder, "stock_prices.xlsx")

close_df.to_excel(output_file)