from datetime import datetime, timedelta
import got
import requests
import sys
import traceback

def get_currency_price(currency_code):
   # request prices from Coinbase API
   request = requests.get("https://api.coinbase.com/v2/exchange-rates?currency="+currency_code)
   # parse from json
   prices = request.json()
   # return the price in US dollars
   return prices['data']['rates']['USD']


def get_recent_tweets(search_terms, tweet_count):
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