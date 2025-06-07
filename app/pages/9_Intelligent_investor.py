import yfinance as yf
import streamlit as st
from presentation.state.session_state_manager import initialize_session_state
# from presentation.controllers.assets_controllers import AssetsController

# Page configuration
st.set_page_config(
    page_title="Intelligent Investor Dashboard", page_icon="💰", layout="wide"
)

# Initialize session state and dependencies
initialize_session_state()

# Initialize controller
# asset_controller = AssetsController()

# Page header
st.title("💰 Intelligent Investor Dashboard")
st.markdown("Analyze the fundamentals of your assets and make informed decisions.")


FUNDAMENTALS_DICT = {
    "Current Price": "currentPrice",
    "PE Ratio": "trailingPE",
    "PB Ratio": "priceToBook",
    "Dividend Yield": "dividendYield",
    "EPS (TTM)": "trailingEps",
    "Return on Equity": "returnOnEquity",
    "Debt to Equity": "debtToEquity",
    "Current Ratio": "currentRatio",
    "Revenue Growth (YoY)": "revenueGrowth",
    "5Y EPS Growth": "earningsQuarterlyGrowth",
}


def get_fundamentals(ticker_symbol, fundamentals_dict=FUNDAMENTALS_DICT):
    stock = yf.Ticker(ticker_symbol)

    # Basic info
    info = stock.info

    # Financial statements
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow

    fundamentals = {"Ticker": ticker_symbol}

    fundamentals.update(
        {
            key: info.get(value)
            for key, value in fundamentals_dict.items()
            if info.get(value) is not None
        }
    )
    return fundamentals
