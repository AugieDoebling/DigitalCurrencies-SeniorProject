import got
from datetime import datetime
import peewee
import requests
import sys
import traceback

BUFFER_LENGTH = 100

DB_USERNAME = ""
DB_PASSWORD = ""
EMAIL_PASSWORD = ""

with open("creds.txt", "r") as creds:
   DB_USERNAME = creds.readline()[:-1]
   DB_PASSWORD = creds.readline()[:-1]
   EMAIL_PASSWORD = creds.readline()[:-1]


myDB = peewee.MySQLDatabase("seniorproject", host="seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com", 
   port=3306, user=DB_USERNAME, passwd=DB_PASSWORD)

class Tweet(peewee.Model):
   id = peewee.BigIntegerField()
   text = peewee.CharField()
   date = peewee.TimestampField()
   favorites = peewee.IntegerField()
   retweets = peewee.IntegerField()

   class Meta:
      database = myDB

def send_to_aws(tweet_array):
   send_data = []

   for t in tweet_array:
      stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
      send_data.append({'id':t.id, 'text':stripped(t.text)[:140], 'date':t.date.replace(second=0), 
         'favorites':t.favorites, 'retweets':t.retweets})

   Tweet.insert_many(send_data).execute()

   timestamp = 0
   if len(send_data) > 0 :
      timestamp = send_data[0]['date']

   print "Tweets: {} CurTime: {} timestamp: {}".format(BUFFER_LENGTH, datetime.now(), timestamp)

def get_params():
   max_n = raw_input("Max Tweets: ")
   max_tweets = 0
   if max_n.isdigit():
      max_tweets = int(max_n)

   since = raw_input("Since: (format 2018-07-10): ")
   until = raw_input("Until: (format 2018-07-10): ")

   return (since, until, max_tweets)

def send_email(subject, message):
   recipient = "Augie Doebling <augustdoebling@gmail.com>"
   return requests.post(
      "https://api.mailgun.net/v3/sandbox1901f3bfd2e64cb9b1e4a3ea2525a8e2.mailgun.org/messages",
      auth=("api", EMAIL_PASSWORD),
      data={"from": "Mailgun Sandbox <postmaster@sandbox1901f3bfd2e64cb9b1e4a3ea2525a8e2.mailgun.org>",
            "to": recipient,
            "subject": subject,
            "text": message})

def main():
   if DB_USERNAME == "" or DB_PASSWORD == "" or EMAIL_PASSWORD == "":
      print "PASSWORDS NOT INCLUDED"

   since, until, max_tweets = get_params()

   body = ""
   subject = "Twitter : "

   start_msg = "Starting tweet download.\nBufferSize = {}\nStartTime = {}\n".format(BUFFER_LENGTH, datetime.now())
   print start_msg
   body += start_msg

   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#bitcoin -giveaway -#freebitcoin').setSince(since).setUntil(until)
   if(max_tweets != 0):
      tweetCriteria = tweetCriteria.setMaxTweets(max_tweets)
   
   start = datetime.now()
   lap_time = datetime.now()

   try:
      got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer=send_to_aws, bufferLength=BUFFER_LENGTH)
      subject += "SUCCESS"
   except Exception as e:
      err_msg = "Error occured at {}\n".format(datetime.now())
      print err_msg
      tb = sys.exc_info()[2]
      traceback.print_tb(tb)
      subject += "FAILURE"
      body += err_msg
      
   end = datetime.now()
   myDB.close()

   fin_msg = "\nFinished. Recieved tweets in {}".format(end-start)
   print fin_msg
   body += fin_msg

   send_email(subject, body)


if __name__ == '__main__':
   main()