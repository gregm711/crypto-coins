import pandas as pd
import math

import matplotlib.pyplot as plt


def main():
	df = pd.read_csv("gas-btc.csv")
	df['ratio-binance-poloniex'] = df.apply(ratio, one="binance_price", two="poloniex_price", axis=1)
	df['ratio-binance-kucoin'] = df.apply(ratio, one="binance_price", two="kucoin_price", axis=1)
	df['ratio-kucoin-poloniex'] = df.apply(ratio, one="kucoin_price", two="poloniex_price", axis=1)

	plt.scatter(df['time'].values, df['poloniex_price'].values)
	plt.scatter(df['time'].values, df['binance_price'].values)
	plt.scatter(df['time'].values, df['kucoin_price'].values)
	plt.ylim(0.0021, 0.0028)
	plt.legend(['poloniex', 'binance', 'kucion'], loc='upper left')
	plt.show()


	break_even = [0.003] * len(df['time'].values)
	plt.scatter(df['time'].values, df['ratio-binance-poloniex'].values)
	plt.scatter(df['time'].values, df['ratio-binance-kucoin'].values)
	plt.scatter(df['time'].values, df['ratio-kucoin-poloniex'].values)
	plt.scatter(df['time'].values, break_even)	
	plt.legend(['binance/poloniex', 'binance/kucoin', 'kucoin/poloniex', 'break_even'], loc='upper left')
	plt.show()



def ratio(row, one, two):
	price_one = row[one]
	price_two = row[two]
	if price_one > price_two:
		return (price_one / price_two) - 1
	else:
		return (price_two / price_one) - 1 



def percentage_difference(row, one, two):
	price_one = row[one]
	price_two = row[two]
	result =  (math.fabs(price_one - price_two) / ((price_one + price_two) / 2)) 
	return result






if __name__ == "__main__":
	main()