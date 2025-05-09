import plotly.express as px
import pandas as pd


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
