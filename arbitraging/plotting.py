import pandas as pd
import math
import time
# import matplotlib.pyplot as plt


def main():
	df_gas = pd.read_csv("gas-btc.csv")
	df_neo = pd.read_csv("neo-btc.csv")
	now = time.time()
	lastTime = df_gas['time'].values[-1]
	if math.fabs(now - lastTime) < 60:

		df_gas['ratio-binance-poloniex-gas'] = df_gas.apply(ratio, one="binance_price", two="poloniex_price", axis=1)
		df_gas['ratio-binance-kucoin-gas'] = df_gas.apply(ratio, one="binance_price", two="kucoin_price", axis=1)
		df_gas['ratio-kucoin-poloniex-gas'] = df_gas.apply(ratio, one="kucoin_price", two="poloniex_price", axis=1)
		df_gas = df_gas[['ratio-binance-poloniex-gas', 'ratio-binance-kucoin-gas', 'ratio-kucoin-poloniex-gas']]
		print(df_gas.tail(2))

		print("******")
		df_neo['ratio-binance-kucoin-neo'] = df_neo.apply(ratio, one="binance_price", two="kucoin_price", axis=1)
		df_neo = df_neo[['ratio-binance-kucoin-neo']]
		print(df_neo.tail(2))
		
		# df = df_gas


		# plt.scatter(df['time'].values, df['poloniex_price'].values)
		# plt.scatter(df['time'].values, df['binance_price'].values)
		# plt.scatter(df['time'].values, df['kucoin_price'].values)
		# plt.ylim(0.002, 0.0035)
		# plt.legend(['poloniex', 'binance', 'kucion'], loc='upper left')
		# plt.show()


		# break_even = [0.003] * len(df['time'].values)
		# plt.scatter(df['time'].values, df['ratio-binance-poloniex-gas'].values)
		# plt.scatter(df['time'].values, df['ratio-binance-kucoin-gas'].values)
		# plt.scatter(df['time'].values, df['ratio-kucoin-poloniex-gas'].values)
		# plt.scatter(df['time'].values, break_even)	
		# plt.legend(['binance/poloniex', 'binance/kucoin', 'kucoin/poloniex', 'break_even'], loc='upper left')
		# plt.show()
		
	else:
		print("logger not running!")



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