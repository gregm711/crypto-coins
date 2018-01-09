from poloniex import Poloniex
from binance.client import Client as bina_client
from kucoin.client import Client as kuco_client
# from python_huobi import Client as huobi_client
from pprint import pprint
import pandas as pd
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

F = os.environ.get("BINANCE_API_KEY")
L = os.environ.get("BINANCE_API_SECRET")
I = os.environ.get('POLONIEX_API_KEY')
P = os.environ.get('POLONIEX_API_SECRET')
E = os.environ.get('KUCOIN_API_KEY')
R = os.environ.get('KUCOIN_API_SECRET')

bina = bina_client(F,L)
polo = Poloniex(I,P)
kuco = kuco_client(E,R)
# huobi = huobi_client()

def main():
    bina_df = pd.DataFrame()
    polo_df = pd.DataFrame()
    kuco_df = pd.DataFrame()
    huobi_df = pd.DataFrame()
    kraken_df = pd.DataFrame()


    while True:
        try:
            bina_df = bina_df.append(logBinaPrices(time.time()))
            polo_df = polo_df.append(logPoloPrices(time.time()))
            kuco_df = kuco_df.append(logKucoPrices(time.time()));
            kraken_df = kraken_df.append(logKrakenPrices(time.time()))

            bina_df.to_csv('all_coin_logger_bina.csv')
            polo_df.to_csv('all_coin_logger_polo.csv')
            kuco_df.to_csv('all_coin_logger_kuco.csv')
            kraken_df.to_csv('all_coin_logger_kraken.csv')

            print 'finished loggin cycle'
            time.sleep(3)
        except Exception as e:
            print e

def logKrakenPrices(t):
    df = pd.DataFrame()
    timeNow = t
    pairs = requests.get('https://api.kraken.com/0/public/AssetPairs').json()
    pair_list = ''
    for key, val in pairs['result'].items():
        pair_list = pair_list + ',' + str(key)
    pair_list = pair_list[1:]
    tickers = requests.get('https://api.kraken.com/0/public/Ticker?pair=' + pair_list).json()
    for key, val in tickers['result'].items():
        df[key] = pd.Series([val['c'][0]], index=[timeNow])
    return df

# def logHuobiPrices(t):
#     df = pd.DataFrame()
#     timeNow = t
#     for pair in huobi.get_symbols()['data']:
#         print pair
#         symbol = pair['base-currency'] + pair['quote-currency']
#         result = huobi.get_ticker(symbol)
#         print symbol
#         print result
#         price = result['tick']['data'][0]['price']
#         df[symbol] = pd.Series([price], index=[timeNow])
#     return df

def logKucoPrices(t):
    kucoTickers = pd.DataFrame(kuco.get_trading_symbols())
    df = pd.DataFrame()
    timeNow = t
    for key,value in kucoTickers['symbol'].iteritems():
        df[value] = pd.Series([kucoTickers['lastDealPrice'][key]], index=[timeNow])
    return df

def logBinaPrices(t):
    binaTickers = pd.DataFrame(bina.get_all_tickers())
    df = pd.DataFrame()
    timeNow = t
    for key,value in binaTickers['symbol'].iteritems():
        df[value] = pd.Series([binaTickers['price'][key]], index=[timeNow])
    return df

def logPoloPrices(t):
    poloTickers = polo.returnTicker()
    # pprint(poloTickers)
    df = pd.DataFrame()
    timeNow = t
    for key in poloTickers:
        df[key] = pd.Series([poloTickers[key]['last']], index=[timeNow])
    return df
    # return polTicker['last']


if __name__ == '__main__':
    print 'working!'
    main()

