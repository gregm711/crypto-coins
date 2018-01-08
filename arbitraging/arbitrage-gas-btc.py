from binance.client import Client as BinanceClient
import numpy
from binance.enums import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd 
from scipy.optimize import fsolve
import numpy as np
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


kucoin_gas_add = "AQujqWhn4UsEcRYGP7F3KkVYfHDBNfqT3D"
poloniex_gas_add = "AX8UxpFQcp3LYEEk9j4K8CPbZTWwyjHJdT"

binance_gas_add = "AexzA2PoEytX3nKwTpx4fgXovFPhUzydxb"
poloniex_btc_add = "1KGFzwUrLtQc8GfmWT8NRV4XfikbYKFqZh"
kucion_btc_add = "14eg4a5q1tucRcBipC8aD5tS4a5i9gb5hv"
binance_btc_add = "14eg4a5q1tucRcBipC8aD5tS4a5i9gb5hv"


poloniex_bitcoin_withdrawl_fee = 0.0005
binance_bitcoin_withdrawl_fee = 0.001
kucoin_bitcoin_withdrawl_fee = 0.0005

binance_trading_fee = 0.001
kucoin_trading_fee = 0.001
poloniex_trading_fee = 0.0015

binance_client = BinanceClient(binance_api_key, binance_api_secret)
poloniex_client = poloniex.Poloniex(poloniex_api_key,poloniex_api_secret)
kucion_client = KucoinClient(kucoin_api_key, kucoin_api_secret)


fixes = [{'coinmarketcap':'MIOTA', 'binance': 'IOTA'},{'coinmarketcap':'BCH', 'binance': 'BCC'}]

max_principal_btc = 0.1

def main():
	while True:
		df = pd.read_csv("gas-btc.csv")
		now = time.time()
		lastTime = df['time'].values[-1]
		if math.fabs(now - lastTime) > 60:
			
			df['ratio-binance-poloniex'] = df.apply(ratio, one="binance_price", two="poloniex_price", axis=1)
			df['ratio-binance-kucoin'] = df.apply(ratio, one="binance_price", two="kucoin_price", axis=1)
			df['ratio-kucoin-poloniex'] = df.apply(ratio, one="kucoin_price", two="poloniex_price", axis=1)
			ratios_df = df[['ratio-binance-poloniex', 'ratio-binance-kucoin', 'ratio-kucoin-poloniex']].tail(5)
			binance_btc = get_account_btc("binance")
			latest_ratios = ratios_df.tail(1).values
			index_min = np.argmin(latest_ratios)
			print(index_min)


			
			time.sleep(200)
		else:
			print("not running logger!")
			break

		



def send_to_account(account_one, account_two, symbol, amount):
	symbol = 'GAS'
	try:
		result = binance_client.withdraw(asset=symbol,address=account_two,amount=38, name='greg-kucoin')
	except Exception  as e:
		print(e)
	except BinanceWithdrawException as e:
		print(e)
	else:
		print("Success", result)

def get_account_btc(account):
	if account == "binance":
		balances = pd.DataFrame(binance_client.get_account()['balances'])
		balances = balances[balances['asset'] == 'BTC']
		balances['free']= pd.to_numeric(balances['free'], errors='coerce')
		balance = balances['free'].values[0]
		return balance
	if account == "kucoin":
		return binance_client.get_asset_balance(asset='BTC')
	if account == "poloniex":
		return binance_client.get_asset_balance(asset='BTC')


def ratio(row, one, two):
	price_one = row[one]
	price_two = row[two]
	if price_one > price_two:
		return (price_one / price_two) - 1
	else:
		return (price_two / price_one) - 1 


def calculate_return(principal_btc, ratio,tf1,tf2,withdraw_fee2):
	return_btc = principal_btc * (1-tf1) * (1-tf2) * ratio - withdraw_fee2 
	return return_btc, (return_btc - principal_btc)



# given principal amount of btc, gives ratio that will be needed to break even
def break_even(principal_btc, tf1,tf2,withdraw_fee2):
	break_even_ratio = 1.0
	return_btc = principal_btc * (1-tf1) * (1-tf2) * break_even_ratio - withdraw_fee2 
	while True:
		break_even_ratio = break_even_ratio + 0.00001
		return_btc = principal_btc * (1-tf1) * (1-tf2) * break_even_ratio - withdraw_fee2 
		if return_btc >= principal_btc:
			break
	return break_even_ratio
	
	

def percentage_difference(row):
	price_one = row['poloniex_price']
	price_two = row['price']
	result =  (math.fabs(price_one - price_two) / ((price_one + price_two) / 2)) * 100
	return result


def clean_poloniex_name(name):
	tmpNames = name.split("_")
	tmp = tmpNames[-1] + tmpNames[0]
	name = ''.join(tmp)
	return name







if __name__ == "__main__":
	# main()
	balances = kucion_client.get_all_balances()
	print(balances)
	# ratio = 0.00253498/.00252000
	# print(ratio)
	# break_even_ratio = break_even(0.1,binance_trading_fee, poloniex_trading_fee, poloniex_bitcoin_withdrawl_fee)

	# print(calculate_return(0.1, ratio,binance_trading_fee, poloniex_trading_fee, poloniex_bitcoin_withdrawl_fee))
	# needed_price = break_even_ratio * 0.00252000
	# print("NEED THIS PRICE" , needed_price)