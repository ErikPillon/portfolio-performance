from assets_handler import AssetsHandler
from visualiser import Visualiser
from processor import Processor
import pandas as pd


class Orchestrator:
    def __init__(self):
        self.assets_handler = AssetsHandler()
        self.visualiser = Visualiser()
        self.processor = Processor(self)
        self.assets = self.get_assets()

    def get_assets(self):
        return self.assets_handler.get_data()

    def get_bonds(self):
        return self.assets_handler.bonds

    def get_sub_interval_data(self, ticker, start_date, end_date=None):
        return self.assets_handler.get_sub_interval_data(ticker, start_date, end_date)

    def get_portfolio_timeseries(self):
        return self.aggregate_time_series(list(self.iterate_assets()))

    def iterate_assets(self):
        for _, asset in self.assets.iterrows():
            ticker = asset["Ticker"]
            start_date = asset["Date"]
            quantity = asset["Quantity"]
            yield self.get_asset_timeseries(ticker, start_date, quantity)

    def get_asset_timeseries(self, ticker, start_date, quantity=1):
        """
        Returns the time series of the given asset multiplied by the quantity.

        Parameters:
        ticker (str): Ticker symbol of the asset
        date (str): Date in 'YYYY-MM-DD' format
        quantity (int): Quantity of the asset

        Returns:
        pandas.Series: Time series of the asset multiplied by the quantity
        """
        data = self.get_sub_interval_data(ticker, start_date)["Close"] * quantity
        data.name = ticker
        return data

    def aggregate_time_series(self, time_series_list):
        """
        Aggregates a list of time series values with unique dates.

        Parameters:
        time_series_list (list): List of pandas.Series objects

        Returns:
        pandas.DataFrame: Aggregated time series values with unique dates
        """
        aggregated = pd.concat(time_series_list, axis=1)
        return aggregated.groupby(aggregated.index).sum()

    def visualize_portfolio_evolution(self):
        return self.visualiser.get_asset_evolution()

    def get_portfolio_performance(self):
        return self.processor.get_portfolio_performance()

    def get_total_capital_invested(self):
        return self.assets_handler.get_total_capital_invested()

    def get_portfolio_size_on_date(self, date):
        return self.assets_handler.get_portfolio_size_on_date(date)

    def get_estimated_portfolio_size_on_date(self, date):
        return self.assets_handler.get_estimated_portfolio_size_on_date(date)

    def visualize_bonds_distribution(self):
        return self.visualiser.get_bonds_distribution(bonds=self.assets_handler.bonds)

    def get_total_bonds_invested(self):
        return self.assets_handler.get_total_bonds_invested()


if __name__ == "__main__":
    o = Orchestrator()

    portfolio = o.get_portfolio_timeseries()
    print(portfolio)
