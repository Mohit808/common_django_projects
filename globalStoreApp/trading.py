
from rest_framework.views import APIView
from globalStoreApp.custom_response import *



import yfinance as yf

# Define tickers
# btc = yf.Ticker("BTC-USD")
# eth = yf.Ticker("ETH-USD")
# bnb = yf.Ticker("BNB-USD") #  Binance Coin
# ada = yf.Ticker("ADA-USD") #  Cardano Coin
# sol = yf.Ticker("SOL-USD") #  Solana Coin
# srp = yf.Ticker("XRP-USD") #  XRP Coin
# doge = yf.Ticker("DOGE-USD") #  doge Coin
# dot = yf.Ticker("DOT-USD") #  Polkadot Coin
# ltc = yf.Ticker("LTC-USD") #  Litecoin
# avax = yf.Ticker("AVAX-USD") #  Avalanche

# Get historical data (last 7 days, hourly)
# btc_data = btc.history(period="7d", interval="1h")
# eth_data = eth.history(period="7d", interval="1h")

# Print the last few entries
# print("BTC-USD (last 5 rows):")
# print(btc_data.tail())

# print("\nETH-USD (last 5 rows):")
# print(eth_data.tail())




tickers = [
    "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD",
    "XRP-USD", "DOGE-USD", "DOT-USD", "LTC-USD", "AVAX-USD"
]

# Get historical data (last 7 days, hourly)
data = yf.download(tickers=tickers, period="1d", interval="5m", group_by='ticker')


# # Print last 2 rows of each
# for ticker in tickers:
#     print(f"\n{ticker} (last 2 rows):")
#     print(data[ticker].tail(2))
#     print(len(data[ticker]), "rows in total")





class GetTrading(APIView):
    def get(self, request,pk=None):
        data = yf.download(tickers=tickers, period="1d", interval="5m", group_by='ticker')
        latest_data = {}

        for ticker in tickers:
            ticker_data = data[ticker]
            if not ticker_data.empty:
                last_row = ticker_data.iloc[-1]
                latest_data[ticker] = last_row.to_dict()

        return customResponse(message= f'Fetch data successfully', status=200  ,data=latest_data)