import pytest
from domain.entities.bonds import Bond, BondFactory, NullBond


def test_create_bond():
    bond = BondFactory.create_bond(
        ticker="BOND123",
        quantity=100,
        value=1000,
        coupon=0.01,
        maturity="2023-06-30",
    )
    assert bond.ticker == "BOND123"
    assert bond.quantity == 100
    assert bond.value == 1000
    assert bond.coupon == 0.01
    assert bond.maturity == "2023-06-30"
