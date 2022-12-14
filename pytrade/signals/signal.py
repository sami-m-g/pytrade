from datetime import date

from pytrade.enums import SignalMovement, SignalPosition, SignalStatus


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
