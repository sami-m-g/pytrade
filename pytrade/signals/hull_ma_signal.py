import numpy as np
import pandas as pd

from pytrade.enums import SignalPosition, SignalStatus
from pytrade.signals.signal import Signal


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
            HullMASignal.claculate_wma(close, period // 2)
            .multiply(2)
            .sub(HullMASignal.claculate_wma(close, period)), int(np.sqrt(period))
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
