import pymysql
import numpy as np
import pandas as pd
import peewee
import pickle
from textblob import TextBlob

def calc_model_variables(tweetsRows):
    """
    :param tweets: list of tweet objects collected. Each Tweet is an object with 
        the attributes as class variables. 
    :return: dataframe of the tweet variables aggregated by minute
    :return: whatever variables we need to pass to the determine_purchase function
    """
    tweets = pd.DataFrame(list(tweetsRows),columns=["tablekey","id","text","date","favorites","retweets"])
    tweets['date'] = pd.to_datetime(tweets['date'],unit = 's')
    tweets['count'] = 1
    
    ## sentiment analysis
    sents = [TextBlob(tw).sentiment.polarity for tw in tweets['text']]
    tweets = pd.concat([tweets,pd.DataFrame(sents,columns=['sentiment'])],axis = 1)

    ## get dataframe of number of tweets, number of favorites
    ag1 = tweets[['date','count','favorites','retweets']].groupby('date').sum()
    ag2 = tweets[['date','sentiment']].groupby('date').mean()
    ag = pd.concat([ag1,ag2],axis = 1)
    ## convert index to a datetime variable
    ag['datetime'] = pd.to_datetime(ag.index)
    ag = ag.reset_index(drop = True)
    return ag

def merge_data(bitcoinData,tweetData):
    """
    :param bitcoinData: dataframe of the aggregated bitcoinData with the variables necessary
    :param tweetData: dataframe of the aggregated data for the tweets
    """
    allData = bitcoinData.merge(tweetData,on = 'datetime')
    return allData

def load_model(model_name):
    """
    :param model_name: string of the file that the model is saved in
        ("model.sav")
    :return: the model to pass to determine_purchase
    """
    return pickle.load(open(model_name, 'rb'))

def determine_expected_price(data, model):
    """
    :param data: input array of the x variables (one row of a dataframe)
    :parma model: used for determining predicted prices change
    :return: expected price change
    
    will look like:
    >>> determine_expected_price(data, load_model("model.sav"))
    """
    ## initialize the x variables (hard coded)
    x_vars = ['count','favorites','retweets','avg_sentiment',
          'sum1440_count','sum1440_favorites','sum1440_retweets','sum1440_avg_sentiment',
          'sum2880_count','sum2880_favorites','sum2880_retweets','sum2880_avg_sentiment',
          'sum4320_count','sum4320_favorites','sum4320_retweets','sum4320_avg_sentiment',
          'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    
    return model.predict(data[x_vars])[0]