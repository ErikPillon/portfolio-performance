from dataclasses import dataclass


@dataclass
class Stock:
    ticker: str
    date: str
    quantity: int = None
    price: float = None
    currency: str = "EUR"
    asset_name: str = None
    dividend_paying: str = False
    _estimated_quantity: bool = False
    _estimated_price: bool = False


@dataclass
class ETF:
    ticker: str
    date: str
    quantity: int = None
    price: float = None
    currency: str = "EUR"
    asset_name: str = None

    _estimated_quantity: bool = False
    _estimated_price: bool = False


class AssetFactory:
    @staticmethod
    def create_asset(asset_type, **kwargs):
        if asset_type == "stock":
            return Stock(**kwargs)
        elif asset_type == "etf":
            return ETF(**kwargs)
        else:
            raise ValueError(f"Unknown asset type: {asset_type}")
