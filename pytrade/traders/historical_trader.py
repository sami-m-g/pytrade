from datetime import date, timedelta

import pandas as pd

from pytrade.enums import WilliamsType
from pytrade.helpers.google_sheets_helper import GoogleSheetsHelper
from pytrade.loaders.yahoo_finance_loader import YahooFinanceLoader
from pytrade.model import WilliamsParams
from pytrade.signals.hull_ma_signal import HullMASignal
from pytrade.signals.williams_signal import WilliamsSignal


class HistoricalTrader:
    def __init__(
        self, last_date: str, ticker: str, interval: str, number_of_intervals: int = 3, hull_ma_period: int = 21,
        hull_ma_limit: float = 1, williams_params: WilliamsParams = WilliamsParams(75, -20, -80, WilliamsType.MEDIUM, -16, -92),
        period: str = "7y", google_spreadsheet_title: str = "StartInvesting", google_out_worksheet_title: str = "HISTORICAL_SIGNAL",
    ) -> "HistoricalTrader":
        self.last_date = last_date
        self.ticker = ticker
        self.interval = interval
        self.number_of_intervals = number_of_intervals
        self.hull_ma_period = hull_ma_period
        self.hull_ma_limit = hull_ma_limit
        self.williams_params = williams_params
        self.period = period
        self.google_spreadsheet_title = google_spreadsheet_title
        self.google_out_worksheet_title = google_out_worksheet_title
        self.loader = YahooFinanceLoader()
        self.get_parsed_date()
        self.get_next_date_generator()

    def get_parsed_date(self) -> None:
        date_list = list(map(int, self.last_date.split("-")))
        year, day, month = date_list[0], date_list[1], date_list[2]
        self.parsed_date = date(year, month, day)

    def get_next_date_generator(self) -> None:
        step = int(self.interval[0])
        period_str = self.interval[1:]
        if period_str == "m":
            self.time_delta = timedelta(minutes=step)
        elif period_str == "h":
            self.time_delta = timedelta(hours=step)
        elif period_str == "d":
            self.time_delta = timedelta(days=step)
        elif period_str == "wk":
            self.time_delta = timedelta(weeks=step)
        elif period_str == "mo":
            self.time_delta = timedelta(weeks=step*4)
        else:
            raise NotImplementedError(period_str)

    def trade(self) -> str:
        output_fields = ["Period", "Hull Status", "Hull Reading", "Hull Position", "Williams Movement"]
        data = self.loader.get_ticker_data(self.ticker, self.period, self.interval)
        output_df = pd.DataFrame([], columns=output_fields)
        for i in range(1, self.number_of_intervals + 1):
            current_date = self.parsed_date - i * self.time_delta
            current_data = data[data.index < current_date]
            hull_ma = HullMASignal(current_data, self.hull_ma_period, self.hull_ma_limit)
            williams = WilliamsSignal(current_data, self.williams_params)
            output_data = [
                current_date,
                hull_ma.get_status().name, hull_ma.get_reading(), hull_ma.get_position().name,
                "".join([movement.value for movement in williams.get_movements()])
            ]
            output_df = pd.concat([output_df, pd.DataFrame([output_data], columns=output_fields)], ignore_index=True)
        GoogleSheetsHelper.write_data(output_df, self.google_spreadsheet_title, self.google_out_worksheet_title)
        return GoogleSheetsHelper.get_sheet_url(self.google_spreadsheet_title, self.google_out_worksheet_title)