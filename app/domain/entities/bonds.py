from dataclasses import dataclass
from enum import Enum
import re
from datetime import datetime
from shared.portfolio_logger import print_log
import pandas as pd


class BondType(Enum):
    CORPORATE = "Corporate"
    GOVERNMENT = "Government"


class Bond:
    def __init__(
        self,
        wkn,
        isin,
        name,
        bond_type,
        date,
        maturity,
        currency,
        face_value,
        invested,
        coupon_redemption,
    ):
        self.wkn = wkn
        self.isin = isin
        self.name = name
        self.bond_type = bond_type
        self.date = date
        self.maturity = maturity
        self.currency = currency
        self.face_value = face_value
        self.invested = invested
        self.coupon_redemption = coupon_redemption


class NullBond:
    def __init__(self):
        self.wkn = ""
        self.isin = ""
        self.name = ""
        self.bond_type = BondType.GOVERNMENT.value
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.maturity = datetime.now().strftime("%Y-%m-%d")
        self.currency = "EUR"
        self.face_value = "0"
        self.invested = "0"
        self.coupon_redemption = "0"


# @dataclass
# class Bond:
#     wkn: str
#     isin: str
#     name: str = None
#     bond_type: BondType
#     maturity: str
#     currency: str = "EUR"
#     face_value: float
#     invested: float
#     coupon_redemption: float

#     # def __post_init__(self):
#     #     assert re.match("^\d{4}-\d{2}-\d{2}$", self.maturity)


# @dataclass
# class NullBond:
#     wkn: str = ""
#     isin: str = ""
#     name: str = ""
#     bond_type: BondType = BondType.GOVERNMENT.value
#     maturity: str = datetime.now().strftime("%Y-%m-%d")
#     currency: str = "EUR"
#     face_value: float = "0"
#     invested: float = "0"
#     coupon_redemption: float = "0"


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

    @staticmethod
    def create_bonds_from_df(df: pd.DataFrame) -> list[Bond]:
        df.columns = [col.lower().replace(" ", "_").strip() for col in df.columns]
        return [BondFactory.create_bond(**row) for _, row in df.iterrows()]


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
