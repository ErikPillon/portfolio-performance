import pytest

from domain.entities.portfolio import Portfolio
from domain.entities.assets import Stock, ETF, NullAsset
from domain.entities.bonds import Bond


@pytest.fixture(autouse=True)
def portfolio():
    return Portfolio(name="Test Portfolio")


def test_create_portfolio():
    portfolio = Portfolio.create_portfolio("Test Portfolio")
    assert portfolio.name == "Test Portfolio"
    assert portfolio._assets == []


def test_get_portfolio_total_investment(portfolio):
    assets = [
        Stock(
            ticker="",
            price=10,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=30,
            date="2023-01-01",
            quantity=1,
        ),
        Stock(
            ticker="",
            price=10,
            date="2023-01-01",
            quantity=1,
        ),
        NullAsset(
            ticker="",
            price=10,
            date="",
            quantity=None,
        ),
    ]

    portfolio._assets = assets
    assert portfolio.get_total_investment() == 60


def test_portfolio_check_null_assets_sum_zero(portfolio):
    assets = [
        Stock(
            ticker="",
            price=10,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=30,
            date="2023-01-01",
            quantity=1,
        ),
        NullAsset(
            ticker="",
            price=10,
            date="",
            quantity=None,
        ),
    ]

    portfolio._assets = assets
    assert portfolio.check_null_assets() == 10


def test_portfolio_check_null_assets(portfolio):
    assets = [
        NullAsset(
            ticker="",
            price=0,
            date="2023-01-01",
            quantity=1,
        ),
        NullAsset(
            ticker="",
            price=0,
            date="2025-01-01",
            quantity=10,
        ),
        NullAsset(
            ticker="AAPL",
            price=0,
            date="",
            quantity=None,
        ),
    ]

    portfolio._assets = assets
    assert portfolio.check_null_assets() == 0


def get_portfolio_total_value(portfolio):
    assets = [
        Stock(
            ticker="",
            price=10,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=30,
            date="2023-01-01",
            quantity=1,
        ),
        NullAsset(
            ticker="",
            price=10,
            date="",
            quantity=None,
        ),
    ]
    portfolio._assets = assets
    assert isinstance(portfolio.get_total_value(), float)


def get_total_investment_by_asset_type(portfolio):
    assets = [
        Stock(
            ticker="",
            price=10,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=30,
            date="2023-01-01",
            quantity=1,
        ),
        NullAsset(
            ticker="",
            price=10,
            date="",
            quantity=None,
        ),
        Stock(
            ticker="",
            price=50,
            date="2023-01-01",
            quantity=1,
        ),
        Stock(
            ticker="",
            price=0.1,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=800,
            date="2023-01-01",
            quantity=1,
        ),
    ]
    res = portfolio.get_total_investment_by_asset_type()
    assert res == {"ETF": 830.0, "Stock": 60.1}


def get_total_investment_by_asset_type_with_zero_assets(portfolio):
    res = portfolio.get_total_investment_by_asset_type()
    assert res == {}


def get_portfolio_positions_by_type(portfolio):
    assets = [
        Stock(
            ticker="",
            price=10,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=30,
            date="2023-01-01",
            quantity=1,
        ),
        NullAsset(
            ticker="",
            price=10,
            date="",
            quantity=None,
        ),
        Bond(
            ticker="",
            price=50,
            date="2023-01-01",
            quantity=1,
        ),
        Stock(
            ticker="",
            price=0.1,
            date="2023-01-01",
            quantity=1,
        ),
        ETF(
            ticker="",
            price=800,
            date="2023-01-01",
            quantity=1,
        ),
    ]
    res = portfolio.get_portfolio_positions_by_type()
    assert res == {"ETF": 1, "Stock": 10.1, "Bond": 1}
