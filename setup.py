import os
from setuptools import setup

from pytrade import __version__


setup(
    name = "pytrade",
    version = __version__,
    author = "Mina Sami",
    author_email = "sami.mg@outlook.com",
    license = "MIT",
    packages=["pytrade",],
    install_requires=[
        "gspread==5.6.2",
        "gspread_dataframe==3.3.0",
        "loadenv==0.1.1",
        "pandas==1.5.0",
        "typing_extensions==4.4.0",
        "yfinance==0.1.84"
    ],
)