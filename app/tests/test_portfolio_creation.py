import pytest
import pandas as pd
from io import StringIO
from domain.entities.assets import Asset, AssetFactory, ETF, Stock, AssetType, NullAsset

sample_data = """
Date,Asset Type,Ticker,Quantity,Price,Calculated Quantity,Currency,Investment,Asset Name
2025-01-06,Stock,CSSPX.MI,0.325770,,NaN,EUR,200.0,Google
2025-01-06,Stock,EUNL.DE,1.889287,,NaN,EUR,200.0,Nasdaq
2025-01-06,ETF,APC.DE,0.844772,,NaN,EUR,200.0,'iShares Core S&P 500 UCITS ETF USD (Acc)'
2025-01-29,ETF,XEON.DE,3.927853,,NaN,EUR,500.0,'Xtrackers II EUR Overnight Rate Swap UCITS ETF 1C'
2025-01-29,ETF,XEOD.DE,3.927853,,NaN,EUR,500.0,'Xtrackers II EUR Overnight Rate Swap UCITS ETF 1D'
2025-02-03,Stock,CSSPX.MI,0.811661,,NaN,EUR,500.0,Google
2025-02-03,ETF,VWCE.DE,3.631873,,NaN,EUR,500.0,'iShares Global Water UCITS ETF USD (Dist)'
2025-02-17,ETF,IQQQ.DE,1.576789,,NaN,EUR,100.0,'iShares Core MSCI World UCITS ETF USD (Acc)'
2025-03-03,Stock,CSSPX.MI,0.829490,,NaN,EUR,500.0,Google
2025-03-17,ETF,IQQQ.DE,1.620745,,NaN,EUR,100.0,'iShares Core MSCI World UCITS ETF USD (Acc)'
2025-04-02,Stock,CSSPX.MI,0.907803,,NaN,EUR,500.0,Google
2025-04-04,ETF,NAQ.F,15.243902,,NaN,EUR,1000.3,'Vanguard FTSE All-World UCITS ETF USD Accumulating'
2025-04-16,ETF,IQQQ.DE,1.717327,,NaN,EUR,100.0,'iShares Core MSCI World UCITS ETF USD (Acc)'
2025-04-16,ETF,IQQQ.DE,1.576292,63.65,NaN,EUR,100.0,'iShares Core MSCI World UCITS ETF USD (Acc)'
2025-05-02,Stock,1GOOGL.MI,0.346308,,NaN,EUR,50.0,'Apple Inc.'
2025-05-02,ETF,NAQ.F,0.733030,,NaN,EUR,50.0,'Vanguard FTSE All-World UCITS ETF USD Accumulating'
2025-05-02,Stock,CSSPX.MI,0.945680,,NaN,EUR,500.0,Google
2025-05-02,ETF,VWCE.DE,4.032908,,NaN,EUR,500.0,'iShares Global Water UCITS ETF USD (Dist)'
2025-05-02,ETF,APC.DE,0.272538,183.46,NaN,EUR,50.0,'iShares Core S&P 500 UCITS ETF USD (Acc)'
2025-05-16,ETF,APC.DE,0.264998,188.68,NaN,EUR,50.0,'iShares Core S&P 500 UCITS ETF USD (Acc)'
2025-05-16,ETF,NAQ.F,0.685400,72.95,NaN,EUR,50.0,'Vanguard FTSE All-World UCITS ETF USD Accumulating'
        """

assets_df = pd.read_csv(StringIO(sample_data))


@pytest.fixture(autouse=True)
def asset_factory():
    return AssetFactory


def test_asset_factory_with_null_asset(asset_factory):
    assert asset_factory is not None
    null_entry = """Date,Asset Type,Ticker,Quantity,Price,Calculated Quantity,Currency,Investment,Asset Name
2025-01-06,,CSSPX.MI,0.325770,,NaN,EUR,200.0,Google"""
    data = pd.read_csv(StringIO(null_entry))
    assets = AssetFactory.create_assets_from_df(data)
    assert len(assets) == 1
    assert assets[0]._asset_type == AssetType.NULL
    assert isinstance(assets[0], NullAsset)


def test_asset_factory_with_etf_asset(asset_factory):
    assert asset_factory is not None
    etf_entry = """Date,Asset Type,Ticker,Quantity,Price,Calculated Quantity,Currency,Investment,Asset Name
2025-01-06,ETF,APC.DE,0.844772,,NaN,EUR,200.0,'iShares Core S&P 500 UCITS ETF USD (Acc)'"""
    data = pd.read_csv(StringIO(etf_entry))
    assets = AssetFactory.create_assets_from_df(data)
    assert len(assets) == 1
    assert assets[0]._asset_type == AssetType.ETF
    assert isinstance(assets[0], ETF)


def test_asset_factory_with_stock_asset(asset_factory):
    assert asset_factory is not None
    entry = """Date,Asset Type,Ticker,Quantity,Price,Calculated Quantity,Currency,Investment,Asset Name
2025-02-03,Stock,CSSPX.MI,0.811661,,NaN,EUR,500.0,Google"""
    data = pd.read_csv(StringIO(entry))
    assets = AssetFactory.create_assets_from_df(data)
    assert len(assets) == 1
    assert assets[0]._asset_type == AssetType.STOCK
    assert isinstance(assets[0], Stock)


def test_asset_factory_with_empty_df(asset_factory):
    assert asset_factory is not None
    data = pd.DataFrame()
    assets = AssetFactory.create_assets_from_df(data)
    assert len(assets) == 0


def test_asset_factory_with_invalid_asset_type(asset_factory):
    assert asset_factory is not None
    entry = """Date,Asset Type,Ticker,Quantity,Price,Calculated Quantity,Currency,Investment,Asset Name
2025-02-03,Invalid,CSSPX.MI,0.811661,,NaN,EUR,500.0,Google"""
    data = pd.read_csv(StringIO(entry))
    assets = AssetFactory.create_assets_from_df(data)
    assert len(assets) == 1
    assert assets[0]._asset_type == AssetType.NULL
    assert isinstance(assets[0], NullAsset)


def test_assets_creation_from_df(asset_factory):
    assert asset_factory is not None
    assets = AssetFactory.create_assets_from_df(assets_df)
    assert len(assets) == assets_df.shape[0]
    assert all(asset._asset_type != AssetType.NULL for asset in assets)
    assert all(isinstance(asset, Stock) or isinstance(asset, ETF) for asset in assets)
