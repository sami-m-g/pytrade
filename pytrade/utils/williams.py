from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class WilliamsStatus(Enum):
    SELL = -1
    BUY = 1
    GRAY = 0


class WilliamsPosition(Enum):
    OVERSOLD = 1
    OVERBOUGHT = -1
    MIDDLE = 0


class WilliamsMovement(Enum):
    UP = "U"
    DOWN = "D"


class Williams:
    def __init__(
        self, data: pd.DataFrame, lookback: int, overbought: int, oversold: int, movements: int, 
    ) -> "Williams":
        self.data = data
        self.lookback = lookback
        self.movements = movements
        self.overbought = overbought
        self.oversold = oversold

        self.get_wr()

    def get_wr(self) -> None:
        high = self.data["High"].rolling(self.lookback).max() 
        low = self.data["Low"].rolling(self.lookback).min()
        close = self.data["Close"]
        self.data["WR"] = -100 * ((high - close) / (high - low))

    def get_last_interval(self) -> str:
        return self.data.index[-1]

    def get_status(self) -> WilliamsStatus:
        current_wr = self.data["WR"][-1]
        previous_wr = self.data["WR"][-2]
        if previous_wr < self.overbought and current_wr > self.overbought:
            return WilliamsStatus.BUY.name
        if previous_wr > self.oversold and current_wr < self.oversold:
            return WilliamsStatus.SELL.name
        return WilliamsStatus.GRAY.name

    def get_position(self) -> WilliamsPosition:
        wr = self.data["WR"][-1]
        if wr > self.overbought:
            return WilliamsPosition.OVERBOUGHT.name
        if wr < self.oversold:
            return WilliamsPosition.OVERSOLD.name
        return WilliamsPosition.MIDDLE.name

    def get_movements(self) -> str:
        wr = self.data["WR"]
        return "".join(
            [WilliamsMovement.UP.value if wr[-i] > wr[-i-1] else WilliamsMovement.DOWN.value for i in range(self.movements, 0, -1)]
        )