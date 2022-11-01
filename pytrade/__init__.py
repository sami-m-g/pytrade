from flask import Flask
app = Flask(__name__)

import pytrade.views

__version__ = "0.1.0"