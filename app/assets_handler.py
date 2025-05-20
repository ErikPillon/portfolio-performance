import pandas as pd
import yfinance as YF
from datetime import datetime
import streamlit as st

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


@st.cache_data(ttl=60 * 60 * 12)
def fetch_yf_data(ticker: str):
    df = YF.Ticker(ticker).history(period="max")
    df.index = df.index.tz_localize(None)
    return df


class AssetsHandler:
    def __init__(self):
        self.last_import = None
        self.hist_data = {}
        self._preload_hist_data()
        (self.data, self.bonds) = self.import_data()
        self._load_hist_data()
        self.get_calculated_quantity()

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
        return (
            pd.read_excel(path, sheet_name="Stocks"),
            pd.read_excel(path, sheet_name="Summary"),
        )

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

    def get_total_capital_invested(self):
        return self.data["Investment"].sum()

    def get_calculated_quantity(self):
        for index, row in self.data.iterrows():
            closing_price = self.get_daily_closing(
                ticker=row["Ticker"], date=row["Date"]
            )
            self.data.loc[index, "Price"] = closing_price
            self.data.loc[index, "CalculatedQuantity"] = (
                row["Investment"] / closing_price
            )

    def get_daily_closing(self, ticker, date):
        # breakpoint()
        if date > self.hist_data[ticker].index.max():
            date = self.hist_data[ticker].index.max()
        return self.hist_data[ticker].loc[date]["Close"]

    def get_data(self):
        return self.data

    def get_bonds(self):
        return self.bonds

    def get_first_date(self):
        return self.data["Date"].min()

    def get_all_currencies(self):
        return self.data["Currency"].unique()

    def get_all_tickers(self):
        return self.data["Ticker"].unique()

    def get_portfolio_size_on_date(self, date):
        return sum(
            row["Quantity"] * self.get_daily_closing(row["Ticker"], date)
            for _, row in self.data.iterrows()
        )

    def get_estimated_portfolio_size_on_date(self, date):
        return sum(
            row["CalculatedQuantity"] * self.get_daily_closing(row["Ticker"], date)
            for _, row in self.data.iterrows()
        )

    def get_total_bonds_invested(self):
        """
        Calculates the total amount of capital invested in bonds.

        Returns:
        float: The sum of all investments in bonds.
        """
        return self.bonds["Invested"].sum()


if __name__ == "__main__":
    assets_handler = AssetsHandler()
    # print(assets_handler.data)
    print(
        f"Portfolio size on {datetime.now().date()}: {assets_handler.get_portfolio_size_on_date(datetime.now())} EUR"
    )  # print(assets_handler.get_portfolio_size_on_date(datetime.now().date()))
    print(f"Total investment: {assets_handler.get_total_value()} EUR")
    print(
        f"Total estimated investment: {assets_handler.get_estimated_portfolio_size_on_date(datetime.now())} EUR"
    )
