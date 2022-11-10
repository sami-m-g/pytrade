from dataclasses import dataclass

from pytrade.enums import WilliamsType


@dataclass
class WilliamsParams:
    lookback: int
    overbought: int
    oversold: int
    type: WilliamsType
    movements: int = 4