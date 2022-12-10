from flask import Flask, render_template, request
app = Flask(__name__)

from pytrade.enums import DataInterval, WilliamsType 
from pytrade.model import WilliamsParams
from pytrade.trader import Trader


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/current")
def current():
    return render_template("current.html", intervals=DataInterval.as_selected_list())


@app.route("/historical")
def historical():
    return render_template("historical.html", intervals=DataInterval.as_list())


@app.route("/trade", methods=["POST"])
def trade():
    williams_params= [
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
    Trader(
        app,
        tickers=None,
        hull_ma_period=int(request.form["hull_ma_period"]),
        hull_ma_limit=float(request.form["hull_ma_limit"]),
        intervals=request.form.getlist("intervals"),
        williams_params=williams_params,
        google_tickers_worksheet_title=request.form["google_tickers_worksheet_title"],
        google_out_worksheet_title=request.form["google_out_worksheet_title"]
    ).trade()
    return "Processing done!"


if __name__ == '__main__':
   app.run()    