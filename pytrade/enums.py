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
    MONTH = "1mo"
    MONTH_3 = "3mo"


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


class WilliamsType(Enum):
    SHORT = "williams_short"
    MEDIUM = "williams_medium"
    LONG = "williams_long"