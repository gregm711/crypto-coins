import requests
import pandas as pd 
import os 
api_url = "https://api.coinmarketcap.com/v1/"




def get_indexed_df():
	tickers = requests.get(api_url + "ticker/")
	df = pd.DataFrame(tickers.json())
	df = index(df)
	return df



def index(df):
	df = df.head(10)
	df['market_cap_usd']= pd.to_numeric(df['market_cap_usd'], errors='coerce')
	df['percent_change_24h']= pd.to_numeric(df['percent_change_24h'], errors='coerce')
	df['percentage_market_cap'] = (df['market_cap_usd'] / df['market_cap_usd'].sum())
	total_day_change =((df['percent_change_24h'] * df['percentage_market_cap']).sum())/(len(df.index))

	return df





if __name__ == "__main__":
	get_indexed_df()