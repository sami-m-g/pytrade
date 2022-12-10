from enum import Enum


class DataInterval(Enum):
    MINUTE_1 = "1m"
    MINUTE_2 = "2m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    MINUTE_90 = "90m"
    HOUR_1 = "1h"
    DAY_1 = "1d"
    DAY_5 = "5d"
    WEEK_1 = "1wk"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"

    @staticmethod
    def defaults() -> list[str]:
        return [DataInterval.MONTH_1.value, DataInterval.WEEK_1.value, DataInterval.DAY_1.value]

    @staticmethod
    def as_selected_list() -> list[tuple[str, bool]]:
        defaults = DataInterval.defaults()
        return [(interval.value, interval.value in defaults) for interval in DataInterval]
    
    @staticmethod
    def as_list() -> list[str]:
        return [interval.value for interval in DataInterval]


class SignalStatus(Enum):
    SELL = -1
    BUY = 1
    GRAY = 0
    HOLD = -2
    STAY_OUT = 2
    EMPTY = 999


class SignalPosition(Enum):
    OVERSOLD = 1
    OVERBOUGHT = -1
    MIDDLE = 0
    SIDEWAYS = 10
    SIDEWAYS_UP = 11
    SIDEWAYS_DOWN = -11
    TRENDING_UP = 12
    TRENDING_DOWN = -12
    EMPTY = 999


class SignalMovement(Enum):
    UP = "U"
    DOWN = "D"


class WilliamsType(Enum):
    SHORT = "williams_short"
    MEDIUM = "williams_medium"
    LONG = "williams_long"