from datetime import datetime
from logging import Logger

import pandas as pd

from pytrade.enums import WilliamsType
from pytrade.helpers.google_sheets_helper import GoogleSheetsHelper
from pytrade.loaders.yahoo_finance_loader import YahooFinanceLoader
from pytrade.model import WilliamsParams
from pytrade.signals.hull_ma_signal import HullMASignal
from pytrade.signals.williams_signal import WilliamsSignal


class HistoricalTrader:
    SUFFIX_PAGE_NAME = "_HIST"

    FMT_DATETIME = "%Y-%m-%dT%H:%M"

    def __init__(
        self, logger: Logger, last_date: str, ticker: str, interval: str, number_of_intervals: int = 3, hull_ma_period: int = 21,
        hull_ma_limit: float = 1, williams_params: WilliamsParams = WilliamsParams(75, -20, -80, WilliamsType.MEDIUM, -16, -92),
        period: str = "max", google_spreadsheet_title: str = "StartInvesting"
    ) -> "HistoricalTrader":
        self.logger = logger
        self.last_date = datetime.strptime(last_date, self.FMT_DATETIME)
        self.ticker = ticker
        self.interval = interval
        self.number_of_intervals = number_of_intervals
        self.hull_ma_period = hull_ma_period
        self.hull_ma_limit = hull_ma_limit
        self.williams_params = williams_params
        self.period = period
        self.google_spreadsheet_title = google_spreadsheet_title
        self.google_out_worksheet_title = ticker + self.SUFFIX_PAGE_NAME
        self.loader = YahooFinanceLoader()

    def get_close_above_open(self, close: float, open: float) -> str:
        if close > open:
            return "ABOVE"
        if close == open:
            return "EQUAL"
        return "BELOW"

    def trade(self) -> str:
        output_fields = [
            "Period",
            "Hull Status", "Hull Reading", "Hull Position",
            "Williams Reading", "Williams Movement",
            "Close Above Open", "Close", "Open"
        ]
        data = self.loader.get_ticker_data(self.ticker, self.period, self.interval, exclude_current_interval=False)
        data = data[data.index <= self.last_date]
        output_df = pd.DataFrame([], columns=output_fields)
        self.logger.debug(f"Data: {data}...")
        for i in range(0, self.number_of_intervals):
            hull_ma = HullMASignal(data, self.hull_ma_period, self.hull_ma_limit)
            williams = WilliamsSignal(data, self.williams_params)
            close, open = data.Close[-1], data.Open[-1]
            output_data = [
                data.index[-1],
                hull_ma.get_status().name, hull_ma.get_reading(), hull_ma.get_position().name,
                williams.get_reading(), "".join([movement.value for movement in williams.get_movements()]),
                self.get_close_above_open(close, open), data.Close[-1], data.Open[-1]
            ]
            output_df = pd.concat([output_df, pd.DataFrame([output_data], columns=output_fields)], ignore_index=True)
            data = data[:-1]
        GoogleSheetsHelper.write_data(output_df, self.google_spreadsheet_title, self.google_out_worksheet_title)
        return GoogleSheetsHelper.get_sheet_url(self.google_spreadsheet_title, self.google_out_worksheet_title)
