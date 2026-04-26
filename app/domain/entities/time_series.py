import pandas as pd


class TimeSeries:
    """time series object to store the historical and expected performance of an asset"""

    def __init__(
        self,
        ticker: str,
        data: pd.DataFrame,
        quantity: float = 1,
        expected_performance: float = 0.06,
    ):
        """Intialize a new time series and evaluate automatically the expected performance

        Args:
            ticker (str): YFinance ticker
            data (pd.DataFrame): dataframe with the historical data
            quantity (float, optional): number of shares owned. Defaults to 1.
            _expected_performance (float, optional): expected performance of the asset. Defaults to 0.06.
        """
        self.ticker = ticker
        self.start_date = data.index[0]
        self._data = data
        self._quantity = quantity
        self._expected_performance = expected_performance

        self.calculate_asset_performance()
        self.calculate_expected_value()

    @property
    def data(self):
        return self._data * self._quantity

    def calculate_asset_performance(self):
        self._data["ActualPerformance"] = (
            self._data["Close"] / self._data["Close"].iloc[0]
        ) - 1

    def calculate_expected_value(self, expected_performance: float = None):
        if expected_performance is None:
            expected_performance = self._expected_performance
        data = self._data.copy()
        data.index = pd.to_datetime(data.index)
        t0 = data.index[0]

        days_elapsed = (data.index - t0).days
        self._data["ExpectedDevFactor"] = (1 + expected_performance) ** (
            days_elapsed / 365
        )
        self._data["ExpectedValue"] = (
            self._data["Close"].iloc[0] * self._data["ExpectedDevFactor"]
        )
        pass


class TimeSeriesFabric:
    @staticmethod
    def create_time_series(ticker: str, start_date: str, end_date: str = ""):
        return TimeSeries(ticker=ticker)


class TimeSeriesHandler:
    def __init__(self):
        self.time_series: list[TimeSeries] = {}
