import yfinance as yf

def fetch_data(symbol='RELIANCE.NS', start='2022-06-01', end='2024-06-01'):
    df = yf.download(symbol, start=start, end=end, interval='1d')
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    return df

data = fetch_data()
print(data.tail())
