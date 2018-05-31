## import necessary packages
import pymysql
import numpy as np
import pandas as pd
import helpers
import pickle
from sklearn.neighbors import KNeighborsRegressor

## create credentials
DB_USERNAME = ""
DB_PASSWORD = ""
with open("creds.txt", "r") as creds:
    DB_USERNAME = creds.readline()[:-1]
    DB_PASSWORD = creds.readline()[:-1]

connection = pymysql.connect(host='seniorproject.cxbqypcd9gwp.us-east-2.rds.amazonaws.com',
                             user=DB_USERNAME,
                             password=DB_PASSWORD,
                             db='seniorproject')
## get all the rows from the sql database
cursor = connection.cursor()
sentimentQuery = "SELECT * FROM sentiment"
cursor.execute(sentimentQuery)
sentimentRows = cursor.fetchall()
## put all the rows in a dataframe
sentiment = pd.DataFrame(list(sentimentRows),
                         columns = ['key','id','datetime','currency','price','logprice',
                                    'times','count','favorites','retweets','avg_sentiment'])

## add day of the week variable
sentiment['datetime'] = pd.to_datetime(sentiment['datetime'])
sentiment['day_of_week'] = sentiment['datetime'].dt.weekday_name
sentiment = pd.concat([sentiment,pd.get_dummies(sentiment['day_of_week'])],axis = 1)

## convert necessary columns to numeric
sentiment['price'] = pd.to_numeric(sentiment['price'])
sentiment['logprice'] = pd.to_numeric(sentiment['logprice'])
sentiment['times'] = pd.to_numeric(sentiment['times'])
sentiment['count'] = pd.to_numeric(sentiment['count'])
sentiment['favorites'] = pd.to_numeric(sentiment['favorites'])
sentiment['retweets'] = pd.to_numeric(sentiment['retweets'])
sentiment['avg_sentiment'] = pd.to_numeric(sentiment['avg_sentiment'])

dummy_df = helpers.create_rolling_sums(sentiment,[1440,2880,4320])

dummy_df['price_change_1day'] = (dummy_df['price'].shift(-1440) - dummy_df['price']).fillna(method = 'ffill')
dummy_df['price_change_2days'] = (dummy_df['price'].shift(-2880) - dummy_df['price']).fillna(method = 'ffill')
dummy_df['price_change_3days'] = (dummy_df['price'].shift(-4320) - dummy_df['price']).fillna(method = 'ffill')

## divide into the training and testing set
x_vars = ['count','favorites','retweets','avg_sentiment',
          'sum1440_count','sum1440_favorites','sum1440_retweets','sum1440_avg_sentiment',
          'sum2880_count','sum2880_favorites','sum2880_retweets','sum2880_avg_sentiment',
          'sum4320_count','sum4320_favorites','sum4320_retweets','sum4320_avg_sentiment',
          'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
y_var = 'price_change_1day'

dummy_df = dummy_df.sample(frac = 1)
n = int(0.75 * len(dummy_df))
train = dummy_df[:n]
test = dummy_df[n:]

x_train = train[x_vars]
x_test = test[x_vars]

y_train = train[y_var]
y_test = test[y_var]

knn_reg = KNeighborsRegressor(n_neighbors = 101)
knn_reg.fit(x_train,y_train)

pickle.dump(knn_reg, open('model.sav', 'wb'))

