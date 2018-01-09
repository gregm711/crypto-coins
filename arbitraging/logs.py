

from binance.client import Client as BinanceClient
from binance.enums import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import time
import math
import csv
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


binance_client = BinanceClient(binance_api_key, binance_api_secret)

kucion_client = KucoinClient(kucoin_api_key, kucoin_api_secret)
poloniex_client = poloniex.Poloniex(poloniex_api_key,poloniex_api_secret)

def main():
	while True:
		try:
			binance_price =  binance_client.get_ticker(symbol='GASBTC')['lastPrice']
			poloniex_price = poloniex_client('returnTicker')['BTC_GAS']['last']
			kucoin_price = kucion_client.get_tick('GAS-BTC')['lastDealPrice']
			save_to_csv([poloniex_price, binance_price, kucoin_price])
			print(poloniex_price, binance_price, kucoin_price)

			binance_price =  binance_client.get_ticker(symbol='NEOBTC')['lastPrice']
			kucoin_price = kucion_client.get_tick('NEO-BTC')['lastDealPrice']
			save_neo_to_csv([binance_price, kucoin_price])
			
		except Exception as e:
			print("errored: ", e)
		time.sleep(30)


def save_to_csv(prices):
	now = time.time()
	with open('gas-btc.csv', 'a') as csvfile:
	    fieldnames = ['poloniex_price', 'binance_price', 'kucoin_price', 'time']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writerow({'poloniex_price': prices[0], 'binance_price': prices[1], 'kucoin_price': prices[2], 'time':now})


def save_neo_to_csv(prices):
	now = time.time()
	with open('neo-btc.csv', 'a') as csvfile:
	    fieldnames = ['binance_price', 'kucoin_price', 'time']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writerow({'binance_price': prices[0], 'kucoin_price': prices[1], 'time':now})




def clean_poloniex_name(name):
	tmpNames = name.split("_")
	tmp = tmpNames[-1] + tmpNames[0]
	name = ''.join(tmp)
	return name







if __name__ == "__main__":
	# run = input("Type in yes to run and re-allocate binance coins \n")
	# if run == "yes":
	main()
