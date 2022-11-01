import unittest

import pandas as pd

from pytrade.williams import Williams, WilliamsPosition, WilliamsStatus


class TestWilliams(unittest.TestCase):
    def get_data(self, rows: list[list[any]]) -> pd.DataFrame:
        data_columns = ["High", "Low", "Close"]
        index = pd.Index(rows, name="Date")
        return pd.DataFrame(rows, columns=data_columns, index=index)
    
    def test_get_status_buy(self) -> None:
        rows = [[2, 1, 1.7], [2, 1, 1.9]]
        data = self.get_data(rows)
        williams = Williams(data=data, lookback=1, overbought=-20, oversold=-80, movements=0)
        self.assertEqual(WilliamsStatus.BUY.name, williams.get_status())
    
    def test_get_status_sell(self) -> None:
        rows = [[2, 1, 1.5], [2, 1, 1.1]]
        data = self.get_data(rows)
        williams = Williams(data=data, lookback=1, overbought=-20, oversold=-80, movements=0)
        self.assertEqual(WilliamsStatus.SELL.name, williams.get_status())

    def test_get_status_gray(self) -> None:
        rows = [[2, 1, 1.3], [2, 1, 1.5]]
        data = self.get_data(rows)
        williams = Williams(data=data, lookback=1, overbought=-20, oversold=-80, movements=0)
        self.assertEqual(WilliamsStatus.GRAY.name, williams.get_status())

    def test_get_position_overbought(self) -> None:
        rows = [[2, 1, 1.9]]
        data = self.get_data(rows)
        williams = Williams(data=data, lookback=1, overbought=-20, oversold=-80, movements=0)
        self.assertEqual(WilliamsPosition.OVERBOUGHT.name, williams.get_position())

    def test_get_position_oversold(self) -> None:
        rows = [[2, 1, 1.1]]
        data = self.get_data(rows)
        williams = Williams(data=data, lookback=1, overbought=-20, oversold=-80, movements=0)
        self.assertEqual(WilliamsPosition.OVERSOLD.name, williams.get_position())

    def test_get_position_middle(self) -> None:
        rows = [[2, 1, 1.5]]
        data = self.get_data(rows)
        williams = Williams(data=data, lookback=1, overbought=-20, oversold=-80, movements=0)
        self.assertEqual(WilliamsPosition.MIDDLE.name, williams.get_position())


if __name__ == '__main__':
    unittest.main()