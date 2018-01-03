import pandas as pd


import matplotlib.pyplot as plt


def main():
	df = pd.read_csv("gas-btc.csv")

	plt.scatter(df['time'].values, df['poloniex_price'].values)
	plt.scatter(df['time'].values, df['binance_price'].values)
	plt.scatter(df['time'].values, df['kucoin_price'].values)
	plt.ylim(0.0021, 0.0028)
	plt.legend(['poloniex', 'binance', 'kucion'], loc='upper left')
	plt.show()
	





if __name__ == "__main__":
	main()