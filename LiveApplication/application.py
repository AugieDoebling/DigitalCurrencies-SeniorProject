# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from utilities import *
import peewee

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
   price_at_purchase = peewee.DoubleField()
   class Meta:
      database = myDB
class Live_sell(peewee.Model):
   id = peewee.BigIntegerField()
   time = peewee.DateTimeField()
   threshold = peewee.DoubleField()
   change = peewee.DoubleField()
   class Meta:
      database = myDB

def sell():
   # collect the purchases from the last 24hrs
   purchases = Live_buy.select().where(Live_buy.time > datetime.utcnow() - timedelta(days=1))
   # grab selling price
   cur_price = get_currency_price('BTC')
   # 'sell' every purchase from the last 24hrs and record the change
   for purch in purchases:
      Live_sell.create(
         threshold=purch.threshold,
         change=cur_price-purch.price_at_purchase)

def collect_tweets():
   return "tweets here"

def buy(exp_price, thresholds):
   # for every threshold value
   for th in thresholds:
      # if we should buy at this threshold
      if exp_price >= th:
         # save a record of a 'purchase'
         Live_buy.create(
            threshold=th,
            expected_change=exp_price,
            price_at_purchase=get_currency_price('BTC'))