import unittest

import pandas as pd

from pytrade.enums import SignalPosition, SignalStatus, WilliamsType
from pytrade.model import WilliamsParams
from pytrade.signal import Signal, WilliamsSignal


class TestWilliamsSignal(unittest.TestCase):
    def get_data(self, rows: list[list[any]]) -> pd.DataFrame:
        data_columns = ["High", "Low", "Close"]
        index = pd.Index(rows, name="Date")
        return pd.DataFrame(rows, columns=data_columns, index=index)
    
    def test_get_status_sell(self) -> None:
        rows = [[2, 1, 1.9], [2, 1, 1.7]]
        data = self.get_data(rows)
        williams = WilliamsSignal(data, WilliamsParams(1, -20, -80, WilliamsType.SHORT, 0, 0))
        self.assertEqual(SignalStatus.SELL, williams.get_status())
    
    def test_get_status_buy(self) -> None:
        rows = [[2, 1, 1.1], [2, 1, 1.5]]
        data = self.get_data(rows)
        williams = WilliamsSignal(data, WilliamsParams(1, -20, -80, WilliamsType.SHORT, 0, 0))
        self.assertEqual(SignalStatus.BUY, williams.get_status())

    def test_get_status_gray(self) -> None:
        rows = [[2, 1, 1.3], [2, 1, 1.5]]
        data = self.get_data(rows)
        williams = WilliamsSignal(data, WilliamsParams(1, -20, -80, WilliamsType.SHORT, 0, 0))
        self.assertEqual(SignalStatus.GRAY, williams.get_status())

    def test_get_position_overbought(self) -> None:
        rows = [[2, 1, 1.9]]
        data = self.get_data(rows)
        williams = WilliamsSignal(data, WilliamsParams(1, -20, -80, WilliamsType.SHORT, 0, 0))
        self.assertEqual(SignalPosition.OVERBOUGHT, williams.get_position())

    def test_get_position_oversold(self) -> None:
        rows = [[2, 1, 1.1]]
        data = self.get_data(rows)
        williams = WilliamsSignal(data, WilliamsParams(1, -20, -80, WilliamsType.SHORT, 0, 0))
        self.assertEqual(SignalPosition.OVERSOLD, williams.get_position())

    def test_get_position_middle(self) -> None:
        rows = [[2, 1, 1.5]]
        data = self.get_data(rows)
        williams = WilliamsSignal(data, WilliamsParams(1, -20, -80, WilliamsType.SHORT, 0, 0))
        self.assertEqual(SignalPosition.MIDDLE, williams.get_position())


if __name__ == '__main__':
    unittest.main()