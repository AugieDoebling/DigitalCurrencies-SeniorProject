import got
from datetime import datetime
import peewee
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

BUFFER_LENGTH = 100
SINCE = "2018-01-01"
UNTIL = "2018-01-02"
MAX_TWEETS = None

DB_USERNAME = ""
DB_PASSWORD = ""
EMAIL_PASSWORD = ""


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
   # global test
   for t in tweet_array:
      # id, text, date, favorites, retweets
      # t.id, t.text.encode('utf-8')[:140], t.date.replace(second=0), t.favorites, t.retweets
      stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
      pw_tweet = Tweet.create(id=t.id, text=stripped(t.text)[:140], date=t.date.replace(second=0),
         favorites=t.favorites, retweets=t.retweets)
      pw_tweet.save()

   print "Tweets: {} CurTime: {}\n    DateTime:{}".format(BUFFER_LENGTH, datetime.now(), tweet_array[BUFFER_LENGTH-1].date)

def get_params():
   max_n = raw_input("Max Tweets: ")
   if max_n.isdigit():
      MAX_TWEETS = int(max_n)

   SINCE = raw_input("Since: (format 2018-07-10): ")
   UNTIL = raw_input("Until: (format 2018-07-10): ")

def main():
   if DB_USERNAME == "" or DB_PASSWORD == "" or EMAIL_PASSWORD == "":
      print "PASSWORDS NOT INCLUDED"

   get_params()

   fromaddr = "augiesjunk263@gmail.com"
   toaddr = "augustdoebling@gmail.com"
   msg = MIMEMultipart()
   msg['From'] = fromaddr
   msg['To'] = toaddr
   msg['Subject'] = "Digital Currencies: PASSED"
   body = ""

   start_msg = "Starting tweet download.\nBufferSize = {}\nStartTime = {}\n".format(BUFFER_LENGTH, datetime.now())
   print start_msg
   body += start_msg

   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#bitcoin -giveaway -#freebitcoin').setSince(SINCE).setUntil(UNTIL)
   # if(MAX_TWEETS):
      # tweetCriteria = tweetCriteria.setMaxTweets(MAX_TWEETS)
   
   start = datetime.now()
   lap_time = datetime.now()

   try:
      got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer=send_to_aws, bufferLength=BUFFER_LENGTH)
   except Exception as e:
      err_msg = "Error occured at {}\n{}".format(datetime.now(), e.message)
      print err_msg
      msg['Subject'] = "Digital Currencies: ERROR"
      body = err_msg
      
   end = datetime.now()
   myDB.close()

   fin_msg = "\nFinished. Recieved tweets in {}".format(end-start)
   print fin_msg
   body += fin_msg

   msg.attach(MIMEText(body, 'plain'))
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login(fromaddr, EMAIL_PASSWORD)
   text = msg.as_string()
   server.sendmail(fromaddr, toaddr, text)
   server.quit()


if __name__ == '__main__':
   main()