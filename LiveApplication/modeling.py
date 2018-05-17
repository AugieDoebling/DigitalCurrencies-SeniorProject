import pymysql
import numpy as np
import pandas as pd
import peewee
import pickle
from textblob import TextBlob

def tweet_to_dict(tweet):
    weekday = tweet.date.weekday()
    return {
        'id': tweet.id,
        'text': tweet.text,
        'date': tweet.date,
        'favorites': tweet.favorites,
        'retweets': tweet.retweets,
        'Sunday'   :1 if weekday == 6 else 0,
        'Monday'   :1 if weekday == 0 else 0,
        'Tuesday'  :1 if weekday == 1 else 0,
        'Wednesday':1 if weekday == 2 else 0,
        'Thursday' :1 if weekday == 3 else 0,
        'Friday'   :1 if weekday == 4 else 0,
        'Saturday' :1 if weekday == 5 else 0,
      }

def tweet_array_to_df(tweet_array):
    """
    :param tweet_array: list of tweet objects collected. Each Tweet is an object with 
        the attributes as class variables. 
    :return: pandas df version of data
    """
    return pd.DataFrame.from_records([tweet_to_dict(t) for t in one_t], 
        columns=['id', 'text', 'date', 'favorites','retweets', 'Sunday', 'Monday', 'Tuesday', 
        'Wednesday', 'Thursday', 'Friday', 'Saturday'])


def calc_model_variables(tweets):
    """
    :param tweets: list of tweet objects collected. Each Tweet is an object with 
        the attributes as class variables. 
    :return: whatever variables we need to pass to the determine_purchase function
    """
    raise NotImplementedError()

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
    """
    return model.predict([data])[0]