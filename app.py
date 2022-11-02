from flask import Flask, render_template, request
app = Flask(__name__)

from pytrade.trader import Trader


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/trade", methods=["POST"])
def trade():
    Trader(
        tickers=None,
        williams_short_lookback=int(request.form["williams_short_lookback"]),
        williams_short_overbought=int(request.form["williams_short_overbought"]),
        williams_short_oversold=int(request.form["williams_short_oversold"]),
        williams_long_lookback=int(request.form["williams_long_lookback"]),
        williams_long_overbought=int(request.form["williams_long_overbought"]),
        williams_long_oversold=int(request.form["williams_long_oversold"])
    ).trade()
    return "Processing done!"


if __name__ == '__main__':
   app.run()