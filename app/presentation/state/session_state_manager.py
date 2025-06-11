import streamlit as st
from presentation.controllers.portfolio_controller import PortfolioController
from shared.portfolio_logger import print_log
from datetime import datetime
import pandas as pd
import yfinance as YF

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


def fetch_historical_data(ticker) -> pd.DataFrame:
    print(f"Fetching historical data for ticker {ticker}")
    df = pd.DataFrame()
    try:
        df = YF.Ticker(ticker).history(period="max")
        df.index = df.index.tz_localize(None)
    except Exception as e:
        print_log(
            f"Error fetching historical data for ticker {ticker}: {e}", type="ERROR"
        )
    return df


def initialize_session_state():
    print_log("Retrieving session state")
    if "initialized" not in st.session_state:
        print_log("Initializing session state", type="SUCCESS")

        st.session_state.initialized = True
        st.session_state.hist_data = {
            ticker: fetch_historical_data(ticker) for ticker in TICKERS
        }

        st.session_state.portfolio_controller = PortfolioController()
        st.session_state.portfolio_controller.build_portfolio_from_file()

        print_log("Session state initialized", type="SUCCESS")
