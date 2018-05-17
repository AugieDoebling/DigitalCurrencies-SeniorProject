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
    return pickle.load(model_name)

def determine_expected_price(data, model):
    """
    :param data: input array of the x variables (one row of a dataframe)
    :parma model: used for determining predicted prices change
    :return: expected price change
    """
    return model.predict([data])[0]