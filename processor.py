import pandas as pd


class Processor:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def get_portfolio_performance(self):
        portfolio = self.orchestrator.get_portfolio_timeseries()
        return portfolio.sum(axis=1)

    def get_total_capital_invested(self):
        assets = self.orchestrator.get_assets()
        portfolio = self.orchestrator.get_portfolio_timeseries()
        assets_evolution_df = pd.DataFrame(index=portfolio.index)

        assets_evolution_df["Investments"] = 0
        for _, asset in assets.iterrows():
            assets_evolution_df[asset["Date"]]["Investments"] += (
                asset["Quantity"]
                * self.orchestrator.get_sub_interval_data(
                    asset["Ticker", asset["Date"]], asset["Date"]
                )["Close"]
            )
        assets_evolution_df["Value"] = portfolio["Investments"].cumsum()
        return assets_evolution_df
