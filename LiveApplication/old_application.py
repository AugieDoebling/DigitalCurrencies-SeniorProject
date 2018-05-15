# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from utilities import *
import time
import pause

usd_account = 1000.0
btc_account = 0.0

def buy(btc_price, purch_amount):
   global usd_account
   global btc_account
   # remove from usd account
   usd_account -= purch_amount

   # amount of btc to buy
   btc_purchase = purch_amount / btc_price
   # add to bitcoin account
   btc_account += btc_purchase

   print "Purchase:\n   ${:.4f} USD on BTC at price ${:.2f}".format(purch_amount, btc_price)

def sell(btc_price):
   global usd_account
   global btc_account
   # price sold for in usd
   sell_amount = btc_account * btc_price
   # add to usd account
   usd_account += sell_amount

   # remove from btc account
   btc_account = 0.0

   print "Sale:\n   ${:.4f} worth of BTC at price ${:.2f}".format(sell_amount, btc_price)

def invest(btc_price, tweets, purch_amount):
   should_buy = True
   # sell_time = datetime.now() + relativedelta(minutes=1)
   sell_time = datetime.now() + relativedelta(seconds=10)

   if should_buy:
      buy(btc_price, purch_amount)

   return (should_buy, sell_time)

def main():
   # currently holding bitcoin
   holding = False
   # price at purchase
   purchase_price = None
   # time at which we should sell
   sell_time = None
   # how much of the account we should spend
   purch_amount = 100.0

   while True:
      # get the recent tweets
      status, tweets = get_recent_tweets('bitcoin', 100)
      if status and not holding:
         purchase_price = get_currency_price('BTC')
         holding, sell_time = invest(purchase_price, tweets, purch_amount)

      # if currently holding bitcoin
      if holding:
         pause.until(sell_time)

         cur_price = get_currency_price('BTC')

         sell(get_currency_price('BTC'))
         holding = False
      # if not holding bitcoin
      else:
         # pause.minutes(1)
         time.sleep(10)

      print "Account Status:\n   USD ) $ {:.4f}      BTC ) ₿ {:.10f}".format(usd_account, btc_account)

      if btc_account == 0.0 and usd_account < purch_amount:
         print "Ran out of money"
         break;


if __name__ == '__main__':
   main()