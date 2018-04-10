## HANS SCHUMANN
## VERSION 1
## 4/04/2018 (Day Not Found)

"""
This file will take data from the SQL database and return dataframes useful for analysis
"""

## import all packages / other files needed
import pymysql
import numpy as np
import pandas as pd
from textblob import TextBlob
import helpers

## create a connection
connection = pymysql.connect(host='seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com',
	                         user='',
	                         password='',
	                         db='')

## get all the rows from the sql database
cursor = connection.cursor()
priceQuery = "SELECT * FROM CurrencyPrice"
cursor.execute(priceQuery)
priceRows = cursor.fetchall()

## put all the rows in a dataframe
bitcoinPrices = pd.DataFrame(list(priceRows), columns=["id","datetime","currency","price"])
bitcoinPrices = bitcoinPrices.drop(bitcoinPrices.index[1189735])  ## drop the bad observation
bitcoinPrices['logprice'] = np.log(bitcoinPrices['price'])  ## log the price
bitcoinPrices['times'] = np.array(range(len(bitcoinPrices)))  ## time integer (may not be useful)

## get the tweet data 
tweetsQuery = "SELECT * FROM tweet"
cursor.execute(tweetsQuery)
tweetsRows = cursor.fetchall()

## clean the variables for later use
tweets = pd.DataFrame(list(tweetsRows),columns=["tablekey","id","text","date","favorites","retweets"])
tweets['date'] = pd.to_datetime(tweets['date'],unit = 's')
tweets['count'] = 1

## sentiment analysis
tw = tweets['text']
sents = [TextBlob(tw).sentiment.polarity for tw in tweets['text']]
tweets = pd.concat([tweets,pd.DataFrame(sents,columns=['sentiment'])],axis = 1)

## get dataframe of number of tweets, number of favorites
ag1 = tweets[['date','count','favorites','retweets']].groupby('date').sum()
ag2 = tweets[['date','sentiment']].groupby('date').mean()
ag = pd.concat([ag1,ag2],axis = 1)
## convert index to a datetime variable
ag['datetime'] = pd.to_datetime(ag.index)
ag = ag.reset_index(drop = True)

allData = bitcoinPrices.merge(ag,on = 'datetime')
lagData = helpers.createLag(2,allData)

allData.to_csv('data.csv')
