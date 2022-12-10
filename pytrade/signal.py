from datetime import date

import numpy as np
import pandas as pd

from pytrade.enums import SignalMovement, SignalPosition, SignalStatus
from pytrade.model import WilliamsParams


class Signal:
    def get_last_interval(self) -> date:
        return self.data.index[-1]

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_reading(self) -> float:
        return self.signal[-1]

    def get_status(self) -> SignalStatus:
        return SignalStatus.EMPTY

    def get_buy_sell(self) -> SignalStatus:
        return SignalStatus.EMPTY

    def get_position(self) -> SignalPosition:
        return SignalPosition.EMPTY

    def get_movements(self) -> list[SignalMovement]:
        return []

    def to_list(self) -> list[any]:
        status = self.get_status()
        buy_sell = self.get_buy_sell()
        position = self.get_position()

        return [
            self.get_last_interval(),
            self.get_name(),
            self.get_reading(),
            status.name if status is not SignalStatus.EMPTY else "",
            buy_sell.name if buy_sell is not SignalStatus.EMPTY else "",
            position.name if position is not SignalPosition.EMPTY else "",
            "".join([movement.value for movement in self.get_movements()])
        ]


class HullMASignal(Signal):
    def __init__(self, data: pd.DataFrame, period: int, limit: float) -> None:
        self.data = data
        self.period = period
        self.limit = limit

        self.calculate()

    @staticmethod
    def claculate_wma(close: pd.Series, period: int) -> pd.Series:
        return close.rolling(period).apply(
            lambda x: ((np.arange(period) + 1) * x).sum() / (np.arange(period) + 1).sum(), raw=True
        )

    @staticmethod
    def calculate_hma(close: pd.Series, period: int) -> pd.Series:
        return HullMASignal.claculate_wma(
            HullMASignal.claculate_wma(close, period // 2).multiply(2).sub(
                HullMASignal.claculate_wma(close, period)), int(np.sqrt(period)
            )
        )

    def calculate(self) -> None:
        self.signal = HullMASignal.calculate_hma(self.data.Close, self.period)

    def get_status(self) -> SignalStatus:
        hma = self.get_reading()
        open, close = self.data.Open[-1], self.data.Close[-1]
        if close > hma and open > hma:
            return SignalStatus.HOLD
        if close < hma < open:
            return SignalStatus.SELL
        if close > hma > open:
            return SignalStatus.BUY
        return SignalStatus.STAY_OUT

    def get_buy_sell(self) -> SignalStatus:
        last_close = self.data.Close[-1]
        hma = self.get_reading()
        if last_close > hma:
            return SignalStatus.BUY
        if last_close < hma:
            return SignalStatus.SELL
        return SignalStatus.GRAY

    def get_position(self) -> SignalPosition:
        current_hma = self.signal[-1]
        previous_hma = self.signal[-2]
        change = (previous_hma - current_hma) / previous_hma * 100
        if change == 0:
            return SignalPosition.SIDEWAYS
        if 0 < change < self.limit: 
            return SignalPosition.SIDEWAYS_UP
        if -self.limit < change < 0:
            return SignalPosition.SIDEWAYS_DOWN
        if change <= self.limit:
            return SignalPosition.TRENDING_UP
        return SignalPosition.TRENDING_DOWN


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
        return  [SignalMovement.UP if wr[-i] > wr[-i-1] else SignalMovement.DOWN for i in range(self.movements, 0, -1)]