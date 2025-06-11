from shared.portfolio_logger import print_log
from dataclasses import dataclass


@dataclass
class Dividend:
    ticker: str
    date: str
    amount: float


class DividendFactory:
    @staticmethod
    def create_dividend(**kwargs):
        try:
            return Dividend(**kwargs)
        except Exception as e:
            print_log(
                f"Error creating dividend with kwargs {kwargs}: {e}", type="WARNING"
            )
            raise ValueError(f"Failed to create dividend: {kwargs} with error {e}")
