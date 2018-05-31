# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from utilities import *
from modeling import *
import peewee
import sys
import traceback
import pandas as pd

# get sql credentials from creds.txt
with open("creds.txt", "r") as creds:
   DB_USERNAME = creds.readline()[:-1]
   DB_PASSWORD = creds.readline()[:-1]
   EMAIL_PASSWORD = creds.readline()[:-1]

# PeeWee classes for interacting with the database
myDB = peewee.MySQLDatabase("seniorproject", host="seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com", 
   port=3306, user=DB_USERNAME, passwd=DB_PASSWORD)
class Live_buy(peewee.Model):
   id = peewee.BigIntegerField()
   time = peewee.DateTimeField()
   threshold = peewee.DoubleField()
   expected_change = peewee.DoubleField()
   purchased_btc = peewee.DoubleField()
   class Meta:
      database = myDB
class Live_sell(peewee.Model):
   id = peewee.BigIntegerField()
   time = peewee.DateTimeField()
   threshold = peewee.DoubleField()
   sell_price = peewee.DoubleField()
   class Meta:
      database = myDB

def sell():
   # collect the purchases from the last 24hrs
   purchases = Live_buy.select().where(Live_buy.time > datetime.utcnow() - timedelta(hours=36))
   # grab selling price
   cur_price = get_currency_price('BTC')
   # sell prices 
   sold = []
   # 'sell' every purchase from the last 24hrs and record the change
   for purch in purchases:
      sell_p = cur_price * purch.purchased_btc
      sold.append(sell_p)
      Live_sell.create(
         threshold=purch.threshold,
         sell_price=sell_p)

   return sold

def print_tweets(tweets):
   timestamp = '?'
   if len(tweets) > 0 :
      timestamp = tweets[0].date

   print "Tweets: {} CurTime: {} timestamp: {}".format(100, datetime.now(), timestamp)

def collect_tweets():
   since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
   until = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#bitcoin').setSince(since).setUntil(until).setMaxTweets(100)

   results = []

   try:
      results = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer=print_tweets)
      print "SUCCESS"
      print len(results)
   except Exception as e:
      print "FAULURE: \n Error occured at {}\n".format(datetime.now())
      traceback.print_tb(sys.exc_info()[2])

   return results

def buy(exp_price, thresholds, amount):
   # BTC price
   btc_price = get_currency_price('BTC')
   # did buy
   did_buy = False
   # usd amount to btc
   purch = amount / btc_price
   # for every threshold value
   for th in thresholds:
      # if we should buy at this threshold
      if exp_price >= th:
         did_buy = True
         # save a record of a 'purchase'
         Live_buy.create(
            threshold=th,
            expected_change=exp_price,
            purchased_btc=purch)
   return (btc_price, did_buy)

def main():
   # PARAMETERS
   # amount in USD to buy
   amount_usd = 100.0
   # different thresholds to purchase at
   thresholds = [0.0, 100.0, 300.0]

   print "going to sell btc..."

   # sell btc purchased 
   sell_prices = sell()

   print "sold btc"
   print "going to collect tweets..."
   
   # collect_tweets
   tweet_array = collect_tweets()
   # save for backup
   with open("tweet_backup.txt", 'w+') as f:
      for t in tweet_array:
         f.write("{0},{1},{2},{3},{4}\n".format(t.id,
         ''.join([i if ord(i) < 128 else ' ' for i in t.text]),
         t.date,
         t.favorites, 
         t.retweets))

   tweet_df = tweet_array_to_df(tweet_array)

   print "collected tweets"
   print "calculating variables..."
   
   # calculate needed variables
   model_variables = calc_model_variables(tweet_df)

   print "calculated variables"
   print "calculating expected change..."

   # load model
   saved_model = load_model('model_python27.sav')

   # run variables through model
   expected_change = determine_expected_price(model_variables, saved_model)

   print "expected change done"
   print "buying..."

   # 'buy' bitcoin according to different price thresholds
   purchased_price, did_buy = buy(expected_change, thresholds, amount_usd)

   print "bought"
   print "sending email..."

   # notify augie via email
   notification_email(sell_prices, expected_change, purchased_price, did_buy, EMAIL_PASSWORD)

   print "finished"

if __name__ == '__main__':
   main()