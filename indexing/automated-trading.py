from binance.client import Client

from binance.enums import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd 

from index import get_indexed_df
import math
import time

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")
trading_fee = 0.001

client = Client(binance_api_key, binance_api_secret)
fixes = [{'coinmarketcap':'MIOTA', 'binance': 'IOTA'},{'coinmarketcap':'BCH', 'binance': 'BCC'}]

def main():
	balances = pd.DataFrame(client.get_account()['balances'])
	df = get_indexed_df()
	balances['symbol'] = balances['asset']
	df['symbol'] = df['symbol'].apply(lambda x: fix_name(x))
	merged_df = pd.merge(balances, df, on='symbol')

	merged_df['free']= pd.to_numeric(merged_df['free'], errors='coerce')
	merged_df['price_usd']= pd.to_numeric(merged_df['price_usd'], errors='coerce')
	merged_df['percentage_market_cap']= pd.to_numeric(merged_df['percentage_market_cap'], errors='coerce')
	merged_df['price_usd']= pd.to_numeric(merged_df['price_usd'], errors='coerce')
	merged_df['free']= pd.to_numeric(merged_df['free'], errors='coerce')

	total_value = get_account_value(merged_df)
	projection = project_coins(merged_df, total_value)

	reallocate_coins(projection)


def fix_name(name):
	for fix in fixes:
		if fix['coinmarketcap'] == name:
			name = fix['binance']
	return name

# Calculates the total value of the account in usd
def get_account_value(df):
	account_value = 0.0
	for i, row in df.iterrows():
		account_value += row['price_usd'] * row['free']
	return account_value
	
	
#  projects how many dollars and how many coins should be allocated based off of market cap and price
def project_coins(df, account_value):
	df['dollar_allocation'] = df['percentage_market_cap'] * account_value
	df['coin_allocation'] = df['dollar_allocation'] / df['price_usd']
	df['allocation_diff'] =  df['coin_allocation'] - df['free']
	df['allocation_diff'] = df['allocation_diff'] * (1-trading_fee)
	return df


# preforms reallocation and bakes in trading fee
def reallocate_coins(df):

	# go through and sell off all coins that we have too much have
	for i, row in df.iterrows():
		if row['symbol'] != 'BTC':
			if row['allocation_diff'] <= 0:
				sell_coins(row['symbol'], math.fabs(row['allocation_diff']))
				time.sleep(2)

	# now that excess coins have been sold off and we have some BTC available for reallocation, go through and purchase coins
	for i, row in df.iterrows():
		if row['symbol'] != 'BTC':
			if row['allocation_diff'] >= 0:
				buy_coins(row['symbol'], math.fabs(row['allocation_diff']))
				time.sleep(2)

# Sells off coins
def sell_coins(symbol, quantity):
	quantity = round(quantity, 2)
	if quantity > 0.0:
		print("attempting to sell ", symbol, quantity)
		try:
			order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
			print("success selling! ", order )
		except Exception as e:
			print("failed with initial quantity", e )
			try:
				quantity = round(quantity, 1)
				order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
				print("success selling! ", order )
			except Exception as e:
				print("failed with second quantity", e )
				quantity = int(round(quantity, 0))
				try:
					order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
					print("success selling! ", order )
				except:
					print("not going to work with this quantity", symbol, quantity)



def buy_coins(symbol, quantity):
	
	quantity = round(quantity, 2)
	if quantity > 0.0:
		print("attempting to buy ", symbol, quantity)
		try:
			order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
			print("success buying! ", order )
		except Exception as e:
			print("failed with initial quantity", e )
			try:
				quantity = round(quantity, 1)
				order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
				print("success buying! ", order )
			except Exception as e:
				print("failed with second quantity", e )
				quantity = int(round(quantity, 0))
				try:
					order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
					print("success buying! ", order )
				except:
					print("not going to work with this quantity", symbol, quantity)








if __name__ == "__main__":
	# run = input("Type in yes to run and re-allocate binance coins \n")
	# if run == "yes":
	main()