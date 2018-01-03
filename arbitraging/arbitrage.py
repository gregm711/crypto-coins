from binance.client import Client
import numpy
from binance.enums import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd 

import math
import time

import poloniex

from kucoin.client import Client as KucoinClient
import kucoin



dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")
poloniex_api_key = os.environ.get("POLONIEX_API_KEY")
poloniex_api_secret = os.environ.get("POLONIEX_API_SECRET")
kucoin_api_key = os.environ.get("KUCOIN_API_KEY")
kucoin_api_secret = os.environ.get("KUCOIN_API_SECRET")

poloniex_bitcoin_withdrawl_fee = 0.0005
binance_bitcoin_withdrawl_fee = 0.001

binance_trading_fee = 0.001
poloniex_trading_fee = 0.0015

client = Client(binance_api_key, binance_api_secret)

kucion_client = KucoinClient(kucoin_api_key, kucoin_api_secret)


# get currencies
currencies = kucion_client.get_currencies()
# print(currencies)


fixes = [{'coinmarketcap':'MIOTA', 'binance': 'IOTA'},{'coinmarketcap':'BCH', 'binance': 'BCC'}]

polo = poloniex.Poloniex(poloniex_api_key,poloniex_api_secret)

def main():
	binance_ticker = pd.DataFrame(client.get_all_tickers())
	poloniex_ticker = pd.DataFrame(polo.returnTicker())
	prices = poloniex_ticker.loc["last"].values
	columns = poloniex_ticker.columns
	poloniex_reset = pd.DataFrame()
	poloniex_reset['poloniex_price'] = prices
	poloniex_reset['symbol'] = columns
	poloniex_reset['symbol'] = poloniex_reset['symbol'].apply(lambda x: clean_poloniex_name(x))
	merged_df = pd.merge(poloniex_reset,binance_ticker, on='symbol')
	merged_df['price']= pd.to_numeric(merged_df['price'], errors='coerce')
	merged_df['poloniex_price']= pd.to_numeric(merged_df['poloniex_price'], errors='coerce')
	merged_df['ratio'] = (merged_df['poloniex_price'] /merged_df['price'])
	merged_df['percentage_difference'] = (merged_df['poloniex_price'] - merged_df['price']) / merged_df['poloniex_price']
	merged_df['abs_diff'] = merged_df['percentage_difference'].apply(lambda x: math.fabs(x))
	merged_df['abs_ratio'] = merged_df['ratio'].apply(lambda x: math.fabs(x))
	df = merged_df.sort_values(by=['abs_ratio'], ascending=False)
	print(df.head(10))






def clean_poloniex_name(name):
	tmpNames = name.split("_")
	tmp = tmpNames[-1] + tmpNames[0]
	name = ''.join(tmp)
	return name







if __name__ == "__main__":
	# run = input("Type in yes to run and re-allocate binance coins \n")
	# if run == "yes":
	main()