from flask import Flask, redirect, render_template, request

from pytrade.enums import DataInterval, WilliamsType
from pytrade.model import WilliamsParams
from pytrade.traders.current_trader import CurrentTrader
from pytrade.traders.historical_trader import HistoricalTrader


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/current")
def current():
    return render_template("current.html", intervals=DataInterval.as_selected_list())


@app.route("/historical")
def historical():
    return render_template("historical.html", intervals=DataInterval.as_list())


@app.route("/trade_current", methods=["POST"])
def trade_current():
    williams_params = [
        WilliamsParams(
            int(request.form[f"{type.value}_lookback"]),
            int(request.form[f"{type.value}_overbought"]),
            int(request.form[f"{type.value}_oversold"]),
            type,
            float(request.form[f"{type.value}_buy_threshold"]),
            float(request.form[f"{type.value}_sell_threshold"]),
        )
        for type in WilliamsType
    ]
    sheet_url = CurrentTrader(
        app.logger,
        tickers=None,
        hull_ma_period=int(request.form["hull_ma_period"]),
        hull_ma_limit=float(request.form["hull_ma_limit"]),
        intervals=request.form.getlist("intervals"),
        williams_params=williams_params,
        google_tickers_worksheet_title=request.form["google_tickers_worksheet_title"],
        google_out_worksheet_title=request.form["google_out_worksheet_title"]
    ).trade()
    return redirect(sheet_url, code=302)


@app.route("/trade_historical", methods=["POST"])
def trade_historical():
    sheet_url = HistoricalTrader(
        app.logger,
        last_date=request.form["last_date"],
        ticker=request.form["ticker"],
        interval=request.form["interval"],
        number_of_intervals=int(request.form["number_of_intervals"]),
        google_out_worksheet_title=request.form["google_out_worksheet_title"]
    ).trade()
    return redirect(sheet_url, code=302)


if __name__ == '__main__':
    app.run()
