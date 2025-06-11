from shared.portfolio_logger import print_log
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import pandas as pd


class AssetType(Enum):
    STOCK = "Stock"
    ETF = "ETF"
    NULL = "Null"


class Asset:
    def __init__(
        self,
        ticker: str,
        price: float,
        date: str,
        quantity: float,
        currency="EUR",
        asset_name: str = None,
        **kwargs,
    ):
        self.ticker = ticker
        self.price = price
        self.date = date if isinstance(date, str) else date.strftime("%Y-%m-%d")
        self.quantity = quantity
        self.currency = currency
        self.asset_name = asset_name
        self._value = None

    def __repr__(self):
        return f"{self.__class__.__name__}(ticker={self.ticker}, currency={self.currency}, quantity={self.quantity}, bought on date={self.date} with price={self.price})"


class NullAsset(Asset):
    def __init__(self, **kwargs):
        super().__init__(
            ticker="NullAsset",
            price=0,
            date=datetime.now().strftime("%Y-%m-%d"),
            quantity=0,
            currency="EUR",
        )
        self._asset_type: str = AssetType.NULL


class Stock(Asset):
    def __init__(self, ticker, price, date, quantity, currency="EUR", **kwargs):
        super().__init__(ticker, price, date, quantity, currency)
        self._asset_type: str = AssetType.STOCK
        self._estimated_quantity: bool = False
        self._estimated_price: bool = False


class ETF(Asset):
    def __init__(self, ticker, price, date, quantity, currency="EUR", **kwargs):
        super().__init__(ticker, price, date, quantity, currency)
        self._asset_type: str = AssetType.ETF
        self._estimated_quantity: bool = False
        self._estimated_price: bool = False


class AssetFactory:
    @staticmethod
    def create_asset(**kwargs):
        asset_type = kwargs.pop("asset_type")
        match asset_type:
            case AssetType.STOCK.value:
                print_log(f"Creating Stock asset: {kwargs}")
                return Stock(**kwargs)
            case AssetType.ETF.value:
                print_log(f"Creating ETF asset: {kwargs}")

                return ETF(**kwargs)
            case _:
                print_log(
                    f"Impossible to recognize asset type: {asset_type}. Creating Null asset: {kwargs}",
                    type="WARNING",
                )
                return NullAsset(**kwargs)

    @staticmethod
    def create_assets_from_df(df: pd.DataFrame) -> list[Asset]:
        """parse the dataframe and create a list of assets

        Args:
            df (pd.DataFrame): dataframe with the assets

        Returns:
            list[Asset]: list of `Asset` objects
        """
        df.columns = [col.lower().replace(" ", "_").strip() for col in df.columns]
        return [AssetFactory.create_asset(**row) for _, row in df.iterrows()]


if __name__ == "__main__":
    import pandas as pd
    from io import StringIO

    etf_entry = """Date,Asset Type,Ticker,Quantity,Price,Calculated Quantity,Currency,Investment,Asset Name
2025-01-06,ETF,APC.DE,0.844772,,NaN,EUR,200.0,'iShares Core S&P 500 UCITS ETF USD (Acc)'"""
    data = pd.read_csv(StringIO(etf_entry))
    assets = AssetFactory.create_assets_from_df(data)
