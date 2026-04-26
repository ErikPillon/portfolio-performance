from domain.entities.assets import Stock, ETF, AssetFactory, Asset, AssetType
from domain.entities.bonds import Bond, BondFactory
from domain.entities.dividends import Dividend
from typing import List
from shared.portfolio_logger import print_log
from domain.entities.portfolio import Portfolio
import pandas as pd
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")


class PortfolioController:
    def __init__(self):
        self.portfolio: "Portfolio" = None

    def build_portfolio_from_file(self, file_path="data/Assets.xlsx"):
        self.portfolio = Portfolio.create_portfolio_from_file(file_path)

    def get_bonds(self) -> List[Bond]:
        return self.portfolio.bonds

    def get_assets(self) -> List[Asset]:
        return self.portfolio.assets

    def get_portfolio_evolution_figure(self):
        return {}

    def get_total_capital_invested(self):
        return self.portfolio.get_total_capital_invested_in_stocks(date=today)

    def get_total_capital_invested_in_stocks(self, date: str = today):
        return self.portfolio.get_total_capital_invested_in_stocks(date=date)

    def get_total_capital_invested_in_bonds(self, date: str = today):
        return self.portfolio.get_total_capital_invested_in_bonds(date=date)

    def get_portfolio_size_on_date(self, date: str = today):
        return 0

    def get_estimated_portfolio_size_on_date(self, date: str = today):
        return 0

    def get_portfolio_performance_on_date(self, date: str = today):
        return 0

    def get_projected_size_of_portfolio(self, rate: float = 0.06):
        return 0
