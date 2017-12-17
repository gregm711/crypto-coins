import requests
import pandas as pd 

api_url = "https://api.coinmarketcap.com/v1/"

def main():
	tickers = requests.get(api_url + "ticker/")
	df = pd.DataFrame(tickers.json())
	index(df)



def index(df):
	print(df.head(20))




if __name__ == "__main__":
	main()