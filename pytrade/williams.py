import pandas as pd

from pytrade.enums import WilliamsMovement, WilliamsPosition, WilliamsStatus
from pytrade.model import WilliamsParams


class Williams:
    def __init__(
        self, data: pd.DataFrame, williams_params: WilliamsParams
    ) -> "Williams":
        self.data = data
        self.lookback = williams_params.lookback
        self.overbought = williams_params.overbought
        self.oversold = williams_params.oversold
        self.movements = williams_params.movements
        self.type = williams_params.type

        self.get_wr()

    def get_name(self) -> str:
        return f"{self.type.value}_{self.lookback}_{self.overbought}_{self.oversold}"

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
        if previous_wr > self.overbought and current_wr < self.overbought:
            return WilliamsStatus.SELL.name
        if previous_wr < self.oversold and current_wr > self.oversold:
            return WilliamsStatus.BUY.name
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
    
    def to_list(self) -> list[any]:
        return [self.get_last_interval(), self.get_name(), self.get_status(), self.get_position(), self.get_movements()]