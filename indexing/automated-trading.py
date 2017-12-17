from binance.client import Client


import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")


client = Client(binance_api_key, binance_api_secret)

# # get market depth
# depth = client.get_order_book(symbol='BNBBTC')

# # place market buy order
# order = client.create_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)

# # get all symbol prices
# prices = client.get_all_tickers()

# # start trade websocket
# def process_message(msg):
#     print("message type: {}".format(msg['e']))
#     print(msg)
#     # do something

# from binance.websockets import BinanceSocketManager
# bm = BinanceSocketManager(client)
# bm.start_aggtrade_socket(symbol='BNBBTC')
# bm.start()

from binance.enums import *
order = client.create_test_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')

print(order)