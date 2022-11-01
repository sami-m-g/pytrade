import gspread
import gspread_dataframe
import pandas as pd

from pytrade.utils.secrets import ClientSecret


class GoogleSheetsWriter:
    DEFAULT_SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    @staticmethod
    def get_service_account(scopes: list[str] = DEFAULT_SCOPES) -> gspread.client.Client:
        return gspread.service_account_from_dict(ClientSecret.to_json(), scopes=scopes)

    @staticmethod
    def write_data(data: pd.DataFrame, spreadsheet_title: str, worksheet_title: str) -> None:
        client = GoogleSheetsWriter.get_service_account()
        spreadsheet = client.open(spreadsheet_title)
        worksheet = spreadsheet.worksheet(worksheet_title)
        gspread_dataframe.set_with_dataframe(worksheet, data, include_column_header=True, resize=True)