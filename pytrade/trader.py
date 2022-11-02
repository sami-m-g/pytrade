import pandas as pd

from pytrade.loader import YahooFinanceLoader
from pytrade.williams import Williams
from pytrade.helpers import GoogleSheetsHelper


class Trader:
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
    DEFAULT_INTERVALS = ["1mo", "1wk", "1d"]

    def __init__(
        self, tickers: list[str] = DEFAULT_TICKERS, intervals: list[str] = DEFAULT_INTERVALS, period: str = "7y",
        williams_short_lookback: int = 20, williams_short_overbought: int = -20, williams_short_oversold: int = -80,
        williams_long_lookback: int = 50, williams_long_overbought: int = -20, williams_long_oversold: int = -80,
        williams_nmovements: int = 4, google_spreadsheet_title: str = "StartInvesting", google_out_worksheet_title: str = "SIGNALS",
        google_tickers_worksheet_title: str = "Tickers"
    ) -> "Trader":
        if tickers is None:
            self.tickers = GoogleSheetsHelper.read_tickers(google_spreadsheet_title, google_tickers_worksheet_title)
        else:
            self.tickers = tickers

        self.intervals = intervals
        self.period = period
        self.williams_short_lookback = williams_short_lookback
        self.williams_short_overbought = williams_short_overbought
        self.williams_short_oversold = williams_short_oversold
        self.williams_long_lookback = williams_long_lookback
        self.williams_long_overbought = williams_long_overbought
        self.williams_long_oversold = williams_long_oversold
        self.williams_nmovements = williams_nmovements
        self.google_spreadsheet_title = google_spreadsheet_title
        self.google_out_worksheet_title = google_out_worksheet_title
    
    def get_short_williams(self, data: pd.DataFrame, ticker: str, interval: str) -> list[list[any]]:
        williams = Williams(
            data, self.williams_short_lookback, self.williams_short_overbought, self.williams_short_oversold, self.williams_nmovements
        )
        name = f"short_williams_{self.williams_short_lookback}_{self.williams_short_overbought}_{self.williams_short_oversold}"
        return [[ticker, interval, williams.get_last_interval(), name, williams.get_status(), williams.get_position(), williams.get_movements()]]

    def get_long_williams(self, data: pd.DataFrame, ticker: str, interval: str) -> list[list[any]]:
        williams = Williams(
            data, self.williams_long_lookback, self.williams_long_overbought, self.williams_long_oversold, self.williams_nmovements
        )
        name = f"long_williams_{self.williams_long_lookback}_{self.williams_long_overbought}_{self.williams_long_oversold}"
        return [[ticker, interval, williams.get_last_interval(), name, williams.get_status(), williams.get_position(), williams.get_movements()]]

    def trade(self) -> None:
        output_fields = ["ticker", "interval", "last_interval", "signal", "status", "position", "movements"]
        output_df = pd.DataFrame([], columns=output_fields)

        for ticker in self.tickers:
            for interval in self.intervals:
                data = YahooFinanceLoader.get_historical_data(ticker, self.period, interval)
                short_williams_data = self.get_short_williams(data, ticker, interval)
                long_williams_data = self.get_long_williams(data, ticker, interval)
                output_df = pd.concat([
                    output_df,
                    pd.DataFrame(short_williams_data, columns=output_fields),
                    pd.DataFrame(long_williams_data, columns=output_fields)
                ]) 

        GoogleSheetsHelper.write_data(output_df, self.google_spreadsheet_title, self.google_out_worksheet_title)