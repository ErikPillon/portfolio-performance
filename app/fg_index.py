import streamlit as st
import yfinance as yf
from visualiser import Visualiser


@st.cache_data(ttl=60 * 60 * 12)
def fetch_financial_data():
    data = {}
    S_and_P_500 = yf.Ticker("^GSPC").history(period="max")
    S_and_P_500.index = S_and_P_500.index.tz_localize(None)
    data["S_and_P_500"] = S_and_P_500
    VIX = yf.Ticker("^VIX").history(period="max")
    VIX.index = VIX.index.tz_localize(None)
    data["VIX"] = VIX
    return data


class FGIndex:
    def __init__(self):
        self.financial_data = fetch_financial_data()
        self.visualiser = Visualiser(orchestrator=self)
        pass

    def get_market_momentum_fig(self):
        return self.visualiser.visualise_market_momentum(
            data=self.financial_data["S_and_P_500"]
        )

    def get_market_volatility_fig(self):
        return self.visualiser.visualise_market_volatility(
            data=self.financial_data["VIX"]
        )
