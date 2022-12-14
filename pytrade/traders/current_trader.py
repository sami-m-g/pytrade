from logging import Logger

import pandas as pd

from pytrade.enums import SignalStatus, DataInterval
from pytrade.helpers.google_sheets_helper import GoogleSheetsHelper
from pytrade.loaders.yahoo_finance_loader import YahooFinanceLoader
from pytrade.model import WilliamsParams
from pytrade.signals.hull_ma_signal import HullMASignal
from pytrade.signals.williams_signal import WilliamsSignal


class CurrentTrader:
    DEFAULT_TICKERS = [
        "STX40.JO", "STXDIV.JO", "STXFIN.JO", "STXIND.JO", "STXRAF.JO", "STXSWX.JO", "STXRES.JO", "STXQUA.JO", "STXMMT.JO",
        "STXWDM.JO", "STXEMG.JO", "STX500.JO", "STXNDQ.JO", "STXILB.JO", "STXPRO.JO", "ETFGGB.JO", "ETFGRE.JO", "ETFWLD.JO",
        "ETF500.JO", "ETF5IT.JO", "ETFBND.JO", "ETFSAP.JO", "ETFSWX.JO", "ETFT40.JO", "ETFGLD.JO", "ETFPLD.JO", "ETFPLT.JO",
        "ETFRHO.JO", "DIVTRX.JO", "PREFTX.JO", "GLPROP.JO", "CSP500.JO", "SMART.JO", "CSPROP.JO", "CTOP50.JO", "NFEMOM.JO",
        "NFEVOL.JO", "MAPPSG.JO", "GIVISA.JO", "NFSH40.JO", "NFTRCI.JO", "NFEDEF.JO", "NFEHGE.JO", "NFEMOD.JO", "GLD.JO",
        "NGPLD.JO", "NGPLT.JO", "SYG4IR.JO", "SYGEU.JO", "SYGUK.JO", "SYGP.JO", "SYGEMF.JO", "SYGJP.JO", "SYGUS.JO",
        "SYGWD.JO", "SYG500.JO", "SYGSW4.JO", "SYGT40.JO", "EURUSD=X", "ZARUSD=X", "ZAR=X", "GC=F", "SI=F", "BZ=F", "CL=F",
        "SBPP.JO", "BTC-USD", "ETH-USD", "ADA-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOT-USD", "DOGE-USD", "LUNA1-USD",
        "AVAX-USD", "ABG.JO", "ARI.JO", "AMS.JO", "AGL.JO", "ANG.JO", "ANH.JO", "APN.JO", "BID.JO", "BVT.JO", "BTI.JO",
        "CPI.JO", "CLS.JO", "CFR.JO", "DSY.JO", "EXX.JO", "FSR.JO", "GLN.JO", "GFI.JO", "IMP.JO", "KIO.JO", "MNP.JO",
        "MRP.JO", "MTN.JO", "NPN.JO", "NED.JO", "NRP.JO", "PPH.JO", "PRX.JO", "REM.JO", "SLM.JO", "SOL.JO", "SHP.JO",
        "SSW.JO", "S32.JO", "SBK.JO", "VOD.JO", "WHL.JO"
    ]
    DEFAULT_INTERVALS = DataInterval.defaults()

    def __init__(
        self, logger: Logger, williams_params: list[WilliamsParams], hull_ma_period: int, hull_ma_limit: float,
        tickers: list[str] = DEFAULT_TICKERS, intervals: list[str] = DEFAULT_INTERVALS, period: str = "7y",
        google_spreadsheet_title: str = "StartInvesting", google_out_worksheet_title: str = "CURENT_SIGNALS",
        google_tickers_worksheet_title: str = "Tickers"
    ) -> "CurrentTrader":
        if tickers is None:
            self.tickers = GoogleSheetsHelper.read_tickers(google_spreadsheet_title, google_tickers_worksheet_title)
        else:
            self.tickers = tickers

        self.logger = logger
        self.williams_params = williams_params
        self.hull_ma_period = hull_ma_period
        self.hull_ma_limit = hull_ma_limit
        self.intervals = intervals
        self.period = period
        self.google_spreadsheet_title = google_spreadsheet_title
        self.google_out_worksheet_title = google_out_worksheet_title
        self.loader = YahooFinanceLoader()

    @staticmethod
    def add_williams_buy_sell(data: pd.DataFrame, williams_buy_sells: list[SignalStatus]) -> None:
        if williams_buy_sells.count(williams_buy_sells[0]) == len(williams_buy_sells):
            buy_sell = williams_buy_sells[0].name
        else:
            buy_sell = SignalStatus.GRAY.name
        data.at[data.shape[0] - 1, "buy/sell"] = buy_sell

    def trade(self) -> str:
        output_fields = ["ticker", "interval", "last_interval", "signal", "reading", "status", "buy/sell", "position", "movements"]
        output_df = pd.DataFrame([], columns=output_fields)

        for ticker in self.tickers:
            self.logger.debug(f"Processing: {ticker}...")
            for interval in self.intervals:
                data = self.loader.get_ticker_data(ticker, self.period, interval)
                williams_buy_sells: list[SignalStatus] = []
                for williams_param in self.williams_params:
                    williams = WilliamsSignal(data, williams_param)
                    william_data = [ticker, interval]
                    william_data.extend(williams.to_list())
                    output_df = pd.concat([output_df, pd.DataFrame([william_data], columns=output_fields)], ignore_index=True)
                    williams_buy_sells.append(williams.get_buy_sell())
                CurrentTrader.add_williams_buy_sell(output_df, williams_buy_sells)
                hull_ma = HullMASignal(data, self.hull_ma_period, self.hull_ma_limit)
                hull_ma_data = [ticker, interval]
                hull_ma_data.extend(hull_ma.to_list())
                output_df = pd.concat([output_df, pd.DataFrame([hull_ma_data], columns=output_fields)], ignore_index=True)
        GoogleSheetsHelper.write_data(output_df, self.google_spreadsheet_title, self.google_out_worksheet_title)
        return GoogleSheetsHelper.get_sheet_url(self.google_spreadsheet_title, self.google_out_worksheet_title)
