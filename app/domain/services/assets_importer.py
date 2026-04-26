import pandas as pd
import yfinance as YF
from datetime import datetime
import streamlit as st


@st.cache_data(ttl=60 * 60 * 12)
def fetch_yf_data(ticker: str):
    df = YF.Ticker(ticker).history(period="max")
    df.index = df.index.tz_localize(None)
    return df


class AssetsImporter:
    def __init__(self):
        (self.data, self.bonds) = self.import_data()
        self.get_calculated_quantity()

        # self.sanity_check()

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
