import pandas as pd
import yfinance as YF
from datetime import datetime

# preload the most common tickers
TICKERS = [
    "1GOOGL.MI",
    "NAQ.F",
    "CSSPX.MI",
    "XEON.DE",
    "XEOD.DE",
    "IQQQ.DE",
    "EUNL.DE",
    "VWCE.DE",
    "APC.DE",
]


def fetch_yf_data(ticker: str):
    df = YF.Ticker(ticker).history(period="max")
    df.index = df.index.tz_localize(None)
    return df


class AssetsHandler:
    def __init__(self):
        self.last_import = None
        self.hist_data = {}
        self._preload_hist_data()
        self.data = self.import_data()
        self._load_hist_data()

        # self.sanity_check()

    def _preload_hist_data(self):
        for ticker in TICKERS:
            self.hist_data[ticker] = fetch_yf_data(ticker)
            print(f"Preloaded {ticker}")
        self.last_import = datetime.now().date()

    def _load_hist_data(self):
        if datetime.now().date() > self.last_import:
            self.hist_data = {}
        for ticker in self.data["Ticker"].unique():
            if ticker in self.hist_data:
                continue
            self.hist_data[ticker] = fetch_yf_data(ticker)
            print(f"Loaded {ticker}")
        self.last_import = datetime.now().date()

    def import_data(self, path="data/Assets.xlsx"):
        return pd.read_excel(path)

    def get_hist_data(self, ticker=None):
        if datetime.now().date() > self.last_import:
            self._load_hist_data()
        if ticker is None:
            return self.hist_data
        else:
            return self.hist_data[ticker]

    def get_sub_interval_data(self, ticker, start_date, end_date=None):
        if end_date is None:
            end_date = datetime.now().date()

        return self.hist_data[ticker].loc[start_date:end_date]

    def get_data(self):
        return self.data

    def get_first_date(self):
        return self.data["Date"].min()

    def get_all_currencies(self):
        return self.data["Currency"].unique()

    def get_all_tickers(self):
        return self.data["Ticker"].unique()


if __name__ == "__main__":
    assets_handler = AssetsHandler()
    breakpoint()
    print(assets_handler.get_sub_interval_data("1GOOGL.MI", "2022-05-02"))
