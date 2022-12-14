from dataclasses import dataclass

from pytrade.enums import WilliamsType


@dataclass
class WilliamsParams:
    lookback: int
    overbought: int
    oversold: int
    type: WilliamsType
    buy_threshold: float
    sell_threshold: float
    movements: int = 4
