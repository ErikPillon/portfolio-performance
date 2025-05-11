import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta


class Visualiser:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def get_data(self):
        return self.orchestrator.assets_handler.get_data()

    def get_asset_evolution(self):
        portfolio = self.orchestrator.get_portfolio_timeseries()
        data = portfolio.sum(axis=1)
        data.name = "Value"
        data.index.name = "Date"
        fig = px.line(
            data,
            x=data.index,
            y=data.values,
            title="Portfolio Evolution",
            labels={"x": "Date", "y": "Portfolio Size"},
        )
        # Prefix y-axis tick labels with euro sign
        fig.update_yaxes(tickprefix="€")

        return fig

    def get_portfolio_performance(self):
        portfolio_performance = self.orchestrator.get_portfolio_performance()
        return self.orchestrator.visualize_portfolio_evolution()

    def visualise_market_momentum(self, data, start_date=None, end_date=None):
        if start_date is None:
            start_date = datetime.now().date() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now().date()
        data["MA125"] = data["Close"].rolling(window=125, min_periods=1).mean()
        data = data[start_date:end_date]
        fig = px.line(
            data,
            x=data.index,
            y=["Close", "MA125"],
            title="Market Momentum",
            labels={"x": "Date", "y": "Price"},
        )
        return fig

    def visualise_market_volatility(self, data, start_date=None, end_date=None):
        if start_date is None:
            start_date = datetime.now().date() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now().date()
        data["MA50"] = data["Close"].rolling(window=50, min_periods=1).mean()
        data = data[start_date:end_date]
        fig = px.line(
            data,
            x=data.index,
            y=["Close", "MA50"],
            title="Market Volatility",
            labels={"x": "Date", "y": "VIX"},
        )
        return fig
