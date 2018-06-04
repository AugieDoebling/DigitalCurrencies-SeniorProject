from datetime import datetime, timedelta
import got
import requests
import sys
import traceback
import pandas as pd

def tweet_array_to_df(tweet_array):
   d = {'id' : [], 'text' : [], 'date' : [], 'favorites' : [], 'retweets' : [], 'Monday' : [],
      'Tuesday' : [], 'Wednesday' : [], 'Thursday' : [], 'Friday' : [], 'Saturday' : [], 'Sunday' : []}
   for t in tweet_array:
      d['id'].append(t.id)
      d['text'].append(t.text)
      d['date'].append(t.date)
      d['favorites'].append(t.favorites)
      d['retweets'].append(t.retweets)
      d['Monday'].append(1 if t.date.weekday() == 0 else 0)
      d['Tuesday'].append(1 if t.date.weekday() == 1 else 0)
      d['Wednesday'].append(1 if t.date.weekday() == 2 else 0)
      d['Thursday'].append(1 if t.date.weekday() == 3 else 0)
      d['Friday'].append(1 if t.date.weekday() == 4 else 0)
      d['Saturday'].append(1 if t.date.weekday() == 5 else 0)
      d['Sunday'].append(1 if t.date.weekday() == 6 else 0)

   return pd.DataFrame(data=d)

def get_currency_price(currency_code):
   # request prices from Coinbase API
   request = requests.get("https://api.coinbase.com/v2/exchange-rates?currency="+currency_code)
   # parse from json
   prices = request.json()
   # return the price in US dollars
   return float(prices['data']['rates']['USD'])

def send_email(subject, message, email_password):
   recipient = "Augie Doebling <augustdoebling@gmail.com>, Hans <hansschumann24@gmail.com>"
   return requests.post(
      "https://api.mailgun.net/v3/sandbox1901f3bfd2e64cb9b1e4a3ea2525a8e2.mailgun.org/messages",
      auth=("api", email_password),
      data={"from": "Mailgun Sandbox <postmaster@sandbox1901f3bfd2e64cb9b1e4a3ea2525a8e2.mailgun.org>",
            "to": recipient,
            "subject": subject,
            "text": message})

def notification_email(sell_prices, expected_change, purchased_price, did_buy, email_password):
   message = ""
   if sell_prices:
      message += "SOLD\n"
   for s in sell_prices:
      message += "   sold ${0} worth of BTC\n".format(s)
   message += "\nEXPECTED CHANGE\n   {0}".format(expected_change)
   if did_buy:
      message += "\n\nPURCHASES\n   purchased $100 worth of BTC at {0}\n".format(purchased_price)
   else:
      message += "\n\nNO PURCHASES\n   did not buy any bitcoin. Price at {0}\n".format(purchased_price)

   subject = "Live BTC App Notification - {0}".format(datetime.now().strftime("%m/%d/%Y"))

   send_email(subject, message, email_password)

def get_recent_tweets(search_terms, tweet_count=1000):
   # collect tweets from today until tomorrow.
   today = datetime.now().strftime("%Y-%m-%d")
   tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
   # collect tweets starting with the most recent
   tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_terms).setSince(today).setUntil(tomorrow).setMaxTweets(tweet_count)

   status = False
   result = []

   try:
      # collect tweets in chunks of 100
      result = got.manager.TweetManager.getTweets(tweetCriteria, bufferLength=100)
      # mark as successful
      status = True
   except Exception as e:
      # print the error and the traceback
      print "FAULURE: \n Error occured at {}\n".format(datetime.now())
      tb = sys.exc_info()[2]
      traceback.print_tb(tb)

   # return if collection was a success and the result
   return (status, result)