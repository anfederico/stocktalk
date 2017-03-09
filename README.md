<p align="center"><img src="https://raw.githubusercontent.com/Crypto-AI/Stocktalk/master/media/Design.png" width=60%></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![PyPI version](https://badge.fury.io/py/stocktalk.svg)](https://badge.fury.io/py/stocktalk)
[![Build Status](https://travis-ci.org/Crypto-AI/Stocktalk.svg?branch=master)](https://travis-ci.org/Crypto-AI/Stocktalk)
![Python](https://img.shields.io/badge/python-v2.7%20%2F%20v3.6-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/Crypto-AI/Stocktalk.svg)](https://github.com/Crypto-AI/stocktalk/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Quickstart
#### Track tweet volume and sentiment in realtime
```python
from stocktalk import streaming, visualize

streaming(credentials, 'TSLA', ['TSLA', 'Tesla'], 30, path, realtime=True, logSentiment=True)
visualize('TSLA', 30, path)
```

<img src="https://raw.githubusercontent.com/Crypto-AI/Stocktalk/master/media/Demo.gif" width=50%>

## Content
- [Install](#install)
- [Download Corpus](#download-corpus)
- [Code Examples](#code-examples)
	* [Twitter Streaming](#twitter-streaming)
	* [Realtime Visualization](#realtime-visualization)
- [Major Features](#major-features)
	* [Debugging Mode](#debugging-mode)
	* [Tracker Log Format](#tracker-log-format)
	* [Tweets Log Format](#tweets-log-format)
- [Underlying Features](#underlying-features)
	* [Text Processing](#text-processing)
	* [Sentiment Analysis](#sentiment-analysis)

## Install
```python
pip install stocktalk
```

## Download Corpus
```python
stocktalk-corpus
or
python -m nltk.downloader vader_lexicon
```

## Code Examples
#### Twitter Streaming
```python
from stocktalk import streaming

# Credentials to access Twitter API 
API_KEY = 'XXXXXXXXXX'
API_SECRET = 'XXXXXXXXXX'
ACCESS_TOKEN = 'XXXXXXXXXX'
ACCESS_TOKEN_SECRET = 'XXXXXXXXXX'
credentials = [API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]

# First element must be ticker/name, proceeding elements are extra queries
TSLA = ['TSLA', 'Tesla']
SNAP = ['SNAP', 'Snapchat']
AAPL = ['AAPL', 'Apple']
AMZN = ['AMZN', 'Amazon']

# Variables
tickers = [TSLA,SNAP,AAPL,AMZN]  # Used for identification purposes
queries =  TSLA+SNAP+AAPL+AMZN   # Filters tweets containing one or more query 
refresh = 30                     # Process and log data every 30 seconds

# Create a folder to collect logs and temporary files
path = "/Users/Anthony/Desktop/Data/"

streaming(credentials, tickers, queries, refresh, path, \
realtime=True, logTracker=True, logTweets=True, logSentiment=True, debug=True)
```

#### Realtime Visualization
```python
from stocktalk import visualize

# Make sure these variables are consistent with streaming.py
tickers = ['TSLA','SNAP','AAPL','AMZN']
refresh = 30
path = "/Users/Anthony/Desktop/Data/"

visualize(tickers, refresh, path)

'''
Steps to run local bokeh server
1. Make sure streaming.py is running...
2. Traverse in console to the directory containing visualize.py
3. python -m bokeh serve --show visualize.py
'''

# Note: Volume is the thick blue line while sentiment is the thin white line
```

<p align="center"><img src="https://raw.githubusercontent.com/Crypto-AI/Stocktalk/master/media/Demo.png"></p>

## Major Features
##### Debugging Mode
```text
Streaming Now...

---10:00:00---
TSLA Volume: 25
TSLA Sentiment: 0.29
SNAP Volume: 218
SNAP Sentiment: 0.03
AAPL Volume: 63
AAPL Sentiment: 0.14
AMZN Volume: 64
AMZN Sentiment: 0.34

---10:00:30---
TSLA Volume: 23
TSLA Sentiment: -0.05
SNAP Volume: 298
SNAP Sentiment: 0.02
AAPL Volume: 112
AAPL Sentiment: 0.01
AMZN Volume: 150
AMZN Sentiment: 0.11
```

##### Tracker Log Format
```text
TSLA_Tracker.txt
datetime,volume,sentiment,duration
03/01/2017 10:30:00,22,0.26,30
03/01/2017 10:30:30,27,0.33,30
03/01/2017 10:31:00,24,0.23,30
03/01/2017 10:31:30,23,0.25,30
03/01/2017 10:32:00,25,0.18,30
```

##### Tweets Log Format
```text
TSLA_Tweets.txt
datetime,tweet,sentiment
03/01/2017 10:30:02,#Tesla zeroing in market with strong relations,0.54
03/01/2017 10:30:03,$TSLA needs 8 Billion for Supercharger network,0.0
03/01/2017 10:30:03,#Tesla grossing high yet still losing money,-0.32
03/01/2017 10:30:03,Tesla's soon to be as affordable as gas-powered cars,0.11 
03/01/2017 10:30:05,The technical reason why Tesla shares could soon rise,0.42 
```

## Underlying Features
##### Text Processing
```python
textOne = "@TeslaMotors shares jump as shipments more than double! #winning"
print(process(textOne))

textTwo = "Tesla announces its best sales quarter: http://trib.al/RbTxvSu $TSLA" 
print(process(textTwo))

textThree = "Tesla $TSLA reports deliveries of 24500, above most views."
print(process(textThree))
```

```text
shares jump as shipments more than double winning
tesla announces its best sales quarter
tesla reports deliveries of number above most views
```

##### Sentiment Analysis
```python
textOne = "shares jump as shipments more than double winning"
print(sentiment(textOne))

textTwo = "tesla reports deliveries of number above most views"
print(sentiment(textTwo))

textThree = "not looking good for tesla competition on the rise"
print(sentiment(textThree))
```

```text
0.706
0.077
-0.341
```
