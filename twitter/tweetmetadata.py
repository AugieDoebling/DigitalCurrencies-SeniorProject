import got
from datetime import datetime

time_dic = {}

def main():
   tweetCriteria = got.manager.TweetCriteria().setQuerySearch('bitcoin').setSince("2018-01-01").setUntil("2018-01-02").setMaxTweets(10)
   
   start = datetime.now()

   tweets = got.manager.TweetManager.getTweets(tweetCriteria)

   end = datetime.now()

   print "recieved in {}, calculating".format(end - start)

   for t in tweets:
      time = t.date.replace(second=0)
      if time in time_dic:
         time_dic[time] += 1
      else:
         time_dic[time] = 1

   print list(time_dic.keys())


if __name__ == '__main__':
   main()