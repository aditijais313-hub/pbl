import yfinance as yf


def get_stock_history(ticker: str, period: str = "1mo"):
    df = yf.Ticker(ticker).history(period=period)
    return df.reset_index()
