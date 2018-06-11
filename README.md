# DigitalCurrencies-SeniorProject
Cal Poly Senior Project Winter/Spring 2018

Authors:
* [Augie Doebling](https://github.com/AugieDoebling)
* [Hans Schumann](https://github.com/HSchumann)

Collected Data:
* [Bitcoin Data from Twitter](https://kaggle.com/augiedoebling/bitcoin-tweets)

## Objective
Using social network data, news articles and search trends, we would like to
model an optimal time to buy and sell digital currencies in short-term time
periods. We believe the recent excitement around digital currencies gives their
value a strong connection to public perception.

To do so, we will collect data using APIs about both the prevalence of
conversation about digital currencies and the prices of digital currencies in
those same cross-sections of time.  Using this, we could ideally find a way to
predict the market behavior and develop a bot to buy and sell digital
currencies in a more efficient way than humans could.  This would result in
profits (or marginal gains) that could be measured in a small experiment.

## What's in This Repository
**Report** Final report on our projects. Findings and reflections reported.

**Twitter** - Code used to call Twitter API to collect data. After collection, we have about 6 million data rows. We have [published this data to Kaggle.](https://kaggle.com/augiedoebling/bitcoin-tweets)

**DataCleaning** - Scripts used to create a data file necessary for statistical
 learning analyses.  dataSetup.py is the main script to run and will create a
 csv file containing currency prices by minute along with information about
 tweets regarding the currency (sentiment, favorites, etc)

**LiveApplication** - Application using models and data from database to
predict best time to purchase and sell Bitcoin. Currently the application only
simulates the buying/selling of Bitcoin and keeps track of how much money it
would have.

## Libraries Used
 [**GetOldTweets-python**](https://github.com/Jefferson-Henrique/GetOldTweets-python), **Pandas**, **Numpy**, **TextBlob**, **PeeWee**
