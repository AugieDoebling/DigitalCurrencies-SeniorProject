import got
from datetime import datetime
import peewee

bufferLength = 5
test = 0

myDB = peewee.MySQLDatabase("seniorproject", host="seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com", port=3306, user="", passwd="")

def send_to_aws(tweet_array):
   global test
   # for tweet in tweet_array:
      # id, text, date, favorites, retweets
      # t.id, t.text.encode('utf-8')[:140], t.date.replace(second=0), t.favorites, t.retweets

   # send this to aws database

   print test


   print "Tweets: {} CurTime: {}".format(bufferLength, datetime.now())


def main():
   # WRITE BEGINNING INFO
   print "Starting tweet download.\nBufferSize = {}\nStartTime = {}\n".format(bufferLength, datetime.now())

   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#bitcoin -giveaway -#freebitcoin :)').setSince("2018-01-01").setUntil("2018-01-02").setMaxTweets(10)
   
   start = datetime.now()
   lap_time = datetime.now()

   try:
      got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer=send_to_aws, bufferLength=bufferLength)
   except Exception as e:
      print "Error occured at {}".format(datetime.now())
      print e.message

   end = datetime.now()

   print "\nFinished. Recieved tweets in {}".format(end-start)


if __name__ == '__main__':
   main()