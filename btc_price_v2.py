import websocket
import json
import threading
import time

class Trading():

   def calc_price_est(self, binancemsg):

      binance_best_ask = float(binancemsg['data']['a'])
      binance_best_ask_vol = float(binancemsg['data']['A'])
      binance_best_bid = float(binancemsg['data']['b'])
      binance_best_bid_vol = float(binancemsg['data']['B'])

      # Calculate the estimated price for binance
      latest_spot_est_price = (binance_best_ask + binance_best_bid)/2
      return latest_spot_est_price

   # ***************************************************************
   def on_message_binance(self, ws, message):

      mystream = ws.url
      binancemsg = json.loads(message)
      estprice = self.calc_price_est(self, binancemsg)
      self.coindata['BTC'] = estprice

   def printer(self, greeting):
      while True:
         time.sleep(0.05)
         print('BTC est Price: ' + str(self.coindata['BTC']))

# ****************************************************************************
   def start(self):

      self.coindata = dict()
      self.coindata['BTC'] = dict()
      self.coindata['BTC']['estPrice'] = float('nan')

      # ************************************************************
      # Start recording from binance. Make lots of threads to manage that
      binance_stream = dict()
      binance_stream['BTC'] = 'wss://stream.binance.com:9443/stream?streams=btcusdt@bookTicker'

      mywebsockets = dict()
      mythread = dict()

      mythread['BTC'] = threading.Thread(target=self.printer, args = (self, 'hi'), name='BTC')
      mythread['BTC'].daemon = True
      mythread['BTC'].start()

      # Launch the thread
      mywebsockets['BTC'] = websocket.WebSocketApp(binance_stream['BTC'], on_message=lambda ws, msg: self.on_message_binance(
         self, ws, msg))
      mywebsockets['BTC'].run_forever()

      # mythread['BTC'] = threading.Thread(target=mywebsockets['BTC'].run_forever, name='BTC')
      # mythread['BTC'].daemon = True
      # mythread['BTC'].start()

# ******************************************************************
if __name__ == '__main__':

    # Start trading!
    x = Trading
    x.start(x)