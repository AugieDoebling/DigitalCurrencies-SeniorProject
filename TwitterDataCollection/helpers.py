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

