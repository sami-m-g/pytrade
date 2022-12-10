import pandas as pd

from pytrade.helpers.google_sheets_helper import GoogleSheetsHelper
from pytrade.loaders.yahoo_finance_loader import YahooFinanceLoader
from pytrade.signals.hull_ma_signal import HullMASignal


class HistoricalTrader:
    def __init__(
        self, last_date: str, ticker: str, interval: str, number_of_intervals: int = 3, hull_ma_period: int = 21,
        hull_ma_limit: float = 1, period: str = "7y", google_spreadsheet_title: str = "StartInvesting",
        google_out_worksheet_title: str = "HISTORICAL_SIGNAL",
    ) -> "HistoricalTrader":
        self.last_date = last_date
        self.ticker = ticker
        self.interval = interval
        self.number_of_intervals = number_of_intervals
        self.hull_ma_period = hull_ma_period
        self.hull_ma_limit = hull_ma_limit
        self.period = period
        self.google_spreadsheet_title = google_spreadsheet_title
        self.google_out_worksheet_title = google_out_worksheet_title
        self.loader = YahooFinanceLoader()

    def trade(self) -> str:
        output_fields = ["Period", "Hull Status", "Hull Reading", "Hull Position", "Williams Movement"]
        data = self.loader.get_ticker_data(self.ticker, self.period, self.interval)
        output_df = pd.DataFrame([], columns=output_fields)

        GoogleSheetsHelper.write_data(output_df, self.google_spreadsheet_title, self.google_out_worksheet_title)
        return GoogleSheetsHelper.get_sheet_url(self.google_spreadsheet_title, self.google_out_worksheet_title)