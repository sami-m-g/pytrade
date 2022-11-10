from flask import Flask, render_template, request
app = Flask(__name__)

from pytrade.enums import DataInterval, WilliamsType 
from pytrade.model import WilliamsParams
from pytrade.trader import Trader


@app.route("/")
def index():
    return render_template(
        "index.html",
        intervals=[(interval.value, interval.value in Trader.DEFAULT_INTERVALS) for interval in DataInterval]
    )


@app.route("/trade", methods=["POST"])
def trade():
    williams_params= [
        WilliamsParams(
            int(request.form[f"{type.value}_lookback"]),
            int(request.form[f"{type.value}_overbought"]),
            int(request.form[f"{type.value}_oversold"]),
            type
        )
        for type in WilliamsType
    ]
    Trader(
        tickers=None,
        intervals=request.form.getlist("intervals"),
        williams_params=williams_params
    ).trade()
    return "Processing done!"


if __name__ == '__main__':
   app.run()    