from binance.client import Client
import numpy
from binance.enums import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd 
from scipy.optimize import fsolve

import math
import time

import poloniex

from kucoin.client import Client as KucoinClient
import kucoin




dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)
binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")


greg_binance_client = Client(binance_api_key, binance_api_secret)

greg_kucoin_gas_add = "AQujqWhn4UsEcRYGP7F3KkVYfHDBNfqT3D"
greg_poloniex_gas_add = "AX8UxpFQcp3LYEEk9j4K8CPbZTWwyjHJdT"
greg_binance_gas_add = "AexzA2PoEytX3nKwTpx4fgXovFPhUzydxb"


ian_poloniex_btc_add = "1FfEnWV67M8MsBpVfNgAdh5HF1ZZW4HnF"

greg_poloniex_btc_add = "1KGFzwUrLtQc8GfmWT8NRV4XfikbYKFqZh"
greg_kucion_btc_add = "14eg4a5q1tucRcBipC8aD5tS4a5i9gb5hv"
greg_binance_btc_add = "1ARieYKr49eFAR4fFw1EoRDwykFzNae7Xj"



binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")
poloniex_api_key = os.environ.get("POLONIEX_API_KEY")
poloniex_api_secret = os.environ.get("POLONIEX_API_SECRET")
kucoin_api_key = os.environ.get("KUCOIN_API_KEY")
kucoin_api_secret = os.environ.get("KUCOIN_API_SECRET")

poloniex_bitcoin_withdrawl_fee = 0.0005
binance_bitcoin_withdrawl_fee = 0.001
kucoin_bitcoin_withdrawl_fee = 0.0005

binance_trading_fee = 0.001
kucoin_trading_fee = 0.001
poloniex_trading_fee = 0.0015

DM = 0.005      # Desired Profit Margin
SS = 4          # Signal Strength, consecutive periods req. for trade signal

# binance_client = BinanceClient(binance_api_key, binance_api_secret)
# poloniex_client = poloniex.Poloniex(poloniex_api_key,poloniex_api_secret)
# kucoin_client = KucoinClient(kucoin_api_key, kucoin_api_secret)



# result = kucoin_client.create_withdrawal('GAS', 29.4170997, greg_poloniex_gas_add)
# print(result)

amount = 40.5348
try:
    result = greg_binance_client.withdraw(asset='GAS',address=greg_kucoin_gas_add,amount=amount, name='greg-kucoin')
except Exception  as e:
    print(e)
except BinanceWithdrawException as e:
    print(e)
else:
    print("Success", result)
