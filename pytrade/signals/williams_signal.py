import pandas as pd

from pytrade.enums import SignalMovement, SignalPosition, SignalStatus
from pytrade.model import WilliamsParams
from pytrade.signals.signal import Signal


class WilliamsSignal(Signal):
    def __init__(
        self, data: pd.DataFrame, williams_params: WilliamsParams
    ) -> "WilliamsSignal":
        self.data = data
        self.lookback = williams_params.lookback
        self.overbought = williams_params.overbought
        self.oversold = williams_params.oversold
        self.movements = williams_params.movements
        self.type = williams_params.type
        self.buy_threshold = williams_params.buy_threshold
        self.sell_threshold = williams_params.sell_threshold

        self.calculate()

    def get_name(self) -> str:
        return f"{self.type.value}_{self.lookback}_{self.overbought}_{self.oversold}"

    def calculate(self) -> None:
        high = self.data.High.rolling(self.lookback).max()
        low = self.data.Low.rolling(self.lookback).min()
        close = self.data.Close
        self.data["WR"] = -100 * ((high - close) / (high - low))
        self.signal = self.data.WR

    def get_buy_sell(self) -> SignalStatus:
        current_wr = self.data.WR[-1]
        previous_wr = self.data.WR[-2]
        if previous_wr > self.overbought and current_wr < self.overbought:
            return SignalStatus.SELL
        if previous_wr < self.oversold and current_wr > self.oversold:
            return SignalStatus.BUY
        return SignalStatus.GRAY

    def get_position(self) -> SignalPosition:
        wr = self.data.WR[-1]
        if wr > self.overbought:
            return SignalPosition.OVERBOUGHT
        if wr < self.oversold:
            return SignalPosition.OVERSOLD
        return SignalPosition.MIDDLE

    def get_movements(self) -> list[SignalMovement]:
        wr = self.data.WR
        return [SignalMovement.UP if wr[-(i+1)] <= wr[-i] else SignalMovement.DOWN for i in range(self.movements, 0, -1)]
