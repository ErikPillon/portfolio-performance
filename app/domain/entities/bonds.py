from dataclasses import dataclass
import re
from datetime import datetime
from app.shared.portfolio_logger import print_log


@dataclass
class Bond:
    ticker: str
    quantity: int
    value: float
    coupon: float
    maturity: str

    def __post_init__(self):
        assert re.match("^\d{4}-\d{2}-\d{2}$", self.maturity)


@dataclass
class NullBond:
    ticker: str = ""
    quantity: int = 0
    value: float = 0
    coupon: float = 0
    maturity: str = datetime.now().strftime("%Y-%m-%d")


class BondFactory:
    @staticmethod
    def create_bond(**kwargs):
        try:
            bond = Bond(**kwargs)
            print_log(f"Created bond with kwargs {kwargs}", type="SUCCESS")
        except Exception as e:
            print_log(f"Error creating bond with kwargs {kwargs}: {e}", type="WARNING")
            bond = NullBond()
        return bond


if __name__ == "__main__":
    bond1 = BondFactory.create_bond(
        ticker="BOND123",
        quantity=100,
        value=1000,
        coupon=0.01,
        maturity="2023-06-30",
    )
    print(bond1)

    null_bond = BondFactory.create_bond()
    print(null_bond)
