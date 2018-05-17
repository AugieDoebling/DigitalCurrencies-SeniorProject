import pymysql
import numpy as np
import pandas as pd
import peewee
import pickle
from textblob import TextBlob

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
    ## initialize the x variables (hard coded)
    x_vars = ['count','favorites','retweets','avg_sentiment',
          'sum1440_count','sum1440_favorites','sum1440_retweets','sum1440_avg_sentiment',
          'sum2880_count','sum2880_favorites','sum2880_retweets','sum2880_avg_sentiment',
          'sum4320_count','sum4320_favorites','sum4320_retweets','sum4320_avg_sentiment',
          'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    return model.predict([data[x_vars]])[0]