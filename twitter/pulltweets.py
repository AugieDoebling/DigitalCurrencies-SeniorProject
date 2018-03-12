import got
from datetime import datetime, timedelta
import peewee
import requests
import sys
import traceback
from dateutil.relativedelta import relativedelta

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

def send_email(subject, message):
   recipient = "Augie Doebling <augustdoebling@gmail.com>"
   return requests.post(
      "https://api.mailgun.net/v3/sandbox1901f3bfd2e64cb9b1e4a3ea2525a8e2.mailgun.org/messages",
      auth=("api", EMAIL_PASSWORD),
      data={"from": "Mailgun Sandbox <postmaster@sandbox1901f3bfd2e64cb9b1e4a3ea2525a8e2.mailgun.org>",
            "to": recipient,
            "subject": subject,
            "text": message})

def day_of_data(date):
   since = date.strftime("%Y-%m-%d")
   until = (date + timedelta(days=1)).strftime("%Y-%m-%d")
   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#bitcoin -giveaway -#freebitcoin').setSince(since).setUntil(until)

   res = ""
   result_count = 0

   try:
      result_count = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer=send_to_aws, bufferLength=BUFFER_LENGTH)
      res = "SUCCESS"
   except Exception as e:
      res = "FAULURE: \n Error occured at {}\n".format(datetime.now())
      print res
      tb = sys.exc_info()[2]
      traceback.print_tb(tb)

   return (res, result_count)

def main():
   if DB_USERNAME == "" or DB_PASSWORD == "" or EMAIL_PASSWORD == "":
      print "PASSWORDS NOT INCLUDED"

   start_month = datetime.strptime(raw_input("Start Month (format 2018-06): "), "%Y-%m")
   month_count = int(raw_input("Number of Months to Collect: "))

   end_month = start_month + relativedelta(months=month_count-1)
   cur_day = start_month

   body = "Starting tweet download.\nRange {} -> {}\nStartTime = {}\n\n".format(start_month.strftime("%Y-%m"), 
      end_month.strftime("%Y-%m"), datetime.now())
   print body
   start = datetime.now()
   lap_time = start

   # while we're still in the same month
   while cur_day.month <= end_month.month:
      day_res = day_of_data(cur_day)

      day_msg = "Date : {} Status : {}\n    Records Collected : {} Time : {}\n".format(cur_day.strftime("%Y-%m-%d"),
         day_res[0], day_res[1], datetime.now()-lap_time)
      print day_msg
      body += day_msg

      cur_day = cur_day + timedelta(days=1)
      lap_time = datetime.now()

   end = datetime.now()
   myDB.close()

   fin_msg = "\nFinished in {}".format(end-start)
   print fin_msg
   body += fin_msg

   send_email("Twitter SeniorProject v2", body)

if __name__ == '__main__':
   main()