import pandas as pd

from pytrade.loader import YahooFinanceLoader
from pytrade.williams import Williams, WilliamsParams
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
        self, williams_params: list[WilliamsParams], tickers: list[str] = DEFAULT_TICKERS, intervals: list[str] = DEFAULT_INTERVALS,
        period: str = "7y", google_spreadsheet_title: str = "StartInvesting", google_out_worksheet_title: str = "SIGNALS",
        google_tickers_worksheet_title: str = "Tickers"
    ) -> "Trader":
        if tickers is None:
            self.tickers = GoogleSheetsHelper.read_tickers(google_spreadsheet_title, google_tickers_worksheet_title)
        else:
            self.tickers = tickers

        self.williams_params = williams_params
        self.intervals = intervals
        self.period = period
        self.google_spreadsheet_title = google_spreadsheet_title
        self.google_out_worksheet_title = google_out_worksheet_title

    def trade(self) -> None:
        output_fields = ["ticker", "interval", "last_interval", "signal", "status", "position", "movements"]
        output_df = pd.DataFrame([], columns=output_fields)

        for ticker in self.tickers:
            for interval in self.intervals:
                data = YahooFinanceLoader.get_historical_data(ticker, self.period, interval)
                for williams_param in self.williams_params:
                    william_data = [ticker, interval]
                    william_data.extend(Williams(data, williams_param).to_list())
                    output_df = pd.concat([output_df, pd.DataFrame([william_data], columns=output_fields)]) 
        GoogleSheetsHelper.write_data(output_df, self.google_spreadsheet_title, self.google_out_worksheet_title)