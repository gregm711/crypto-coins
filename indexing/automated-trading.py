from binance.client import Client

from binance.enums import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd 

from index import get_indexed_df

import time
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")


client = Client(binance_api_key, binance_api_secret)

def main():
	balances = pd.DataFrame(client.get_account()['balances'])
	df = get_indexed_df()
	balances['symbol'] = balances['asset']

	merged_df = pd.merge(balances, df, on='symbol')
	merged_df['free']= pd.to_numeric(merged_df['free'], errors='coerce')
	merged_df['price_usd']= pd.to_numeric(merged_df['price_usd'], errors='coerce')
	merged_df['percentage_market_cap']= pd.to_numeric(merged_df['percentage_market_cap'], errors='coerce')
	merged_df['price_usd']= pd.to_numeric(merged_df['price_usd'], errors='coerce')
	merged_df['free']= pd.to_numeric(merged_df['free'], errors='coerce')

	total_value = get_account_value(merged_df)


	projection = project_coins(merged_df, total_value)
	reallocate_coins(projection)




def get_account_value(df):
	account_value = 0.0
	for i, row in df.iterrows():
		account_value += row['price_usd'] * row['free']
	return account_value
	
	

def project_coins(df, account_value):
	df['dollar_allocation'] = df['percentage_market_cap'] * account_value
	df['coin_allocation'] = df['dollar_allocation'] / df['price_usd']
	return df



def reallocate_coins(df):
	df['allocation_diff'] =  df['coin_allocation'] - df['free']
	for i, row in df.iterrows():
		print(row['symbol'], row['allocation_diff'])
		if row['allocation_diff'] <= 0:
			sell_coins(row['symbol'], row['allocation_diff'])
		elif row['allocation_diff'] >= 0:
			buy_coins(row['symbol'], row['allocation_diff'])
		time.sleep(10)
	
def sell_coins(symbol, quantity):
	order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
	print("sold coins! ",order)

def buy_coins(symbol, quantity):
	order = client.create_order(symbol= symbol + 'BTC',side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
	print("bought coins! ",order)








if __name__ == "__main__":
	main()