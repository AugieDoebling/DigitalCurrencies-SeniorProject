## HANS SCHUMANN
## VERSION 1
## 4.April 2018

"""
This script is full of helper functions that can be used to create
and manipulate data for future use (in the dataSetup.py file)
"""


## a function to create a lag of k
def createLag(k,allData):
    temp = allData.copy()[['id','price','count','favorites','retweets']]
    temp['id'] = temp['id'] + k
    temp.columns = ['id','lag_price','lag_count','lag_favorites','lag_retweets']
    lagData = allData.merge(temp,on = 'id')
    lagData['priceChange'] = lagData['price'] - lagData['lag_price']
    return lagData

def create_rolling_sums(df,times):
    """
    Creates the training and testing sets with sums of the tweet variables
    for given time periods as specified
    :param df: the dataframe to use
    :param times: an array of the times wanted 
    :return dataframe with the created variables
    """
    for i in range(len(times)):
        df[('sum' + str(times[i]) + '_count')] = df['count'].rolling(times[i]-1).sum().fillna(method = 'bfill')
        df[('sum' + str(times[i]) + '_favorites')] = df['favorites'].rolling(times[i]-1).sum().fillna(method = 'bfill')
        df[('sum' + str(times[i]) + '_retweets')] = df['retweets'].rolling(times[i]-1).sum().fillna(method = 'bfill')
        df[('sum' + str(times[i]) + '_avg_sentiment')] = df['avg_sentiment'].rolling(times[i]-1).sum().fillna(method = 'bfill')
        # subtract all but the time period of interest
        if (i > 1):
            df[('sum' + str(times[i]) + '_count')] = df[('sum' + str(times[i]) + '_count')] - df['count'].rolling(times[i-1]-1).sum().fillna(method = 'bfill')
            df[('sum' + str(times[i]) + '_favorites')] = df[('sum' + str(times[i]) + '_favorites')] - df['favorites'].rolling(times[i-1]-1).sum().fillna(method = 'bfill')
            df[('sum' + str(times[i]) + '_retweets')] = df[('sum' + str(times[i]) + '_retweets')] - df['retweets'].rolling(times[i-1]-1).sum().fillna(method = 'bfill')
            df[('sum' + str(times[i]) + '_avg_sentiment')] = df[('sum' + str(times[i]) + '_avg_sentiment')] -df['avg_sentiment'].rolling(times[i-1]-1).sum().fillna(method = 'bfill')
    return df

def determine_purchase(data, model, threshold = 0):
    """
    :param data: input array of the x variables (one row of a dataframe)
    :parma model: used for determining predicted prices change
    :return: true or false based on if we should buy
    """
    if model.predict([data])[0] > threshold:
        return True
    else:
        return False
    