import pymysql
import numpy as np
import pandas as pd
import peewee
from textblob import TextBlob

def calc_model_variables(tweets):
    """
    :param tweets: list of tweet objects collected. Each Tweet is an object with 
        the attributes as class variables. 
    :return: whatever variables we need to pass to the determine_purchase function
    """
    raise NotImplementedError()

def load_model():
    """
    :param ?: whatever parameters we need
    :return: the model to pass to determine_purchase
    """
    raise NotImplementedError()

def determine_expected_price(data, model):
    """
    :param data: input array of the x variables (one row of a dataframe)
    :parma model: used for determining predicted prices change
    :return: expected price change
    """
    return model.predict([data])[0]