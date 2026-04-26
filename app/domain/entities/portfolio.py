from shared.portfolio_logger import print_log
from dataclasses import dataclass, field
import pandas as pd
from typing import Dict, List
from domain.entities.assets import Asset, AssetFactory
from domain.entities.bonds import Bond, BondFactory
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")


class Portfolio:
    def __init__(self, assets: List[Asset] = [], bonds: List[Bond] = []):
        self._assets: List[Asset] = assets
        self._bonds: List[Bond] = bonds
        # self._time_series = TimeSeriesHandler()

    def __repr__(self) -> str:
        return (
            f"Portfolio(name={self.name}, assets={self._assets}, bonds={self._bonds})"
        )

    @staticmethod
    def create_portfolio(
        name: str, assets: List[Asset] = [], bonds: List[Bond] = []
    ) -> "Portfolio":
        return Portfolio(name=name, assets=assets, bonds=bonds)

    @staticmethod
    def create_portfolio_from_file(file_path: str) -> "Portfolio":
        if file_path.endswith(".xlsx"):
            assets_df = pd.read_excel(file_path, sheet_name="Stocks")
            bonds_df = pd.read_excel(file_path, sheet_name="Bonds")
        elif file_path.endswith(".csv"):
            raise NotImplementedError
        else:
            print_log("Unsupported file format", type="ERROR")
            raise ValueError("Unsupported file format")

        assets = AssetFactory.create_assets_from_df(assets_df)
        # bonds = BondFactory.create_bonds_from_df(pd.DataFrame())
        bonds = []
        return Portfolio(assets=assets, bonds=bonds)

    @property
    def assets(self) -> List[Asset]:
        return self._assets

    @property
    def bonds(self) -> List[Bond]:
        return self._bonds

    def get_total_investment_by_asset_type(self) -> Dict[str, float]:
        return {}

    def get_total_value(self) -> float:
        return 0

    def get_total_investment_by_bond_type(self) -> Dict[str, float]:
        return {}

    def get_total_bonds_invested(self) -> float:
        """
        Calculates the total amount of capital invested in bonds.

        Returns:
        float: The sum of all investments in bonds.
        """
        return 0

    def get_total_capital_invested_in_stocks(self, date: str = today) -> float:
        return sum(asset.price for asset in self.assets if asset.date <= date)

    def get_total_capital_invested_in_bonds(self, date: str = today) -> float:
        return sum(bond.invested for bond in self.bonds if bond.date <= date)
