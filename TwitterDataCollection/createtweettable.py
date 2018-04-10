import got
from datetime import datetime
import peewee

myDB = peewee.MySQLDatabase("seniorproject", host="seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com", 
   port=3306, user="", passwd="")

class Tweet(peewee.Model):
   id = peewee.IntegerField()
   text = peewee.CharField()
   date = peewee.TimestampField()
   favorites = peewee.IntegerField()
   retweets = peewee.IntegerField()

   class Meta:
      database = myDB

Tweet.create_table()