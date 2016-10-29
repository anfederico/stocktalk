<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Stocktalk/master/media/Stocktalk.png" width=60%></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![PyPI version](https://badge.fury.io/py/stocktalk.svg)](https://badge.fury.io/py/stocktalk)
[![Build Status](https://travis-ci.org/anfederico/Stocktalk.svg?branch=master)](https://travis-ci.org/anfederico/Stocktalk)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/Stocktalk.svg)](https://github.com/anfederico/stocktalk/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)

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

#### Mining Twitter

```python
from stocktalk import TwitterAxe

# Credentials to access Twitter API 
ACCESS_TOKEN    = 'XXXXXXXXXX'
ACCESS_SECRET   = 'XXXXXXXXXX'
CONSUMER_KEY    = 'XXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXX'
Credentials = [ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET] 

# Create an instance of the TwitterAxe class
axe = TwitterAxe(Credentials)

minePeriod        = 60*5     # Mine Twitter for 5 minutes
requestFrequency  = 30*1     # Request tweets every 30 seconds
analyzeFrequency  = 60*1     # Analyze tweets every 1 minute
requestAmount     = 100      # With each request pull 100 tweets (max = 100)
similarityCutoff  = 90       # Filter out tweets with 90% similarity (default = 90)

# Start mining
axe.mine("Apple", minePeriod, requestFrequency, analyzeFrequency, requestAmount, similarityCutoff)
```

```text
Mine complete from
[2016/10/14 02:37:16 PM] - [2016/10/14 02:42:26 PM]
```
#### Explore Collected Data

```python
axe.showInventory()
axe.showUniqueTweets()
axe.showFilteredTweets()
axe.showTimeSeries()
```

```text
Inventory
Unique Tweets: 128
Filtered Tweets: 6

Unique Tweets                                            
0   Apple needs to release new Macbooks soon or i ...
1   Apple Sony to Release Five Smartphone Games T ...
2   Apple unveils tree-filled Regent Street store ...
...
125 Apple in talks with Australian company to bri ...
126 Anyone else holding out on updating their App ...
127 The Washington Post goes interactive on Apple ...

Filtered Tweets                                      
0   Apple Sony to Release Five Smartphone Games T ...
1   Apple Sony to Release Five Smartphone Games T ...
2   Apple Sony to Release Five Smartphone Games T ...
3   The Washington Post goes interactive on Apple ...
4   The Washington Post goes interactive on Apple ...
5   The Washington Post goes interactive on Apple ...

Time Series
       time        sentiment  tweets
0   01:40:15 PM      0.204     193
1   01:50:15 PM      0.164     232
2   02:00:15 PM      0.004     221
3   02:10:15 PM     -0.234     255
4   02:20:41 PM     -0.354     244
5   02:30:58 PM     -0.430     242
...
26  06:10:56 PM     -0.055     342
27  06:20:02 PM     -0.134     352
28  06:30:13 PM     -0.125     361
29  06:40:26 PM     -0.045     351
30  06:50:49 PM     -0.032     357
31  07:00:53 PM     -0.011     330
```
#### Visualize Sentiment Analysis

```python
axe.showPlot()
```
<img src="https://github.com/anfederico/Stocktalk/blob/master/media/Plot.png"  width=60%>

## Underlying Features

#### Spam Filtering
```python
stringOne = "Lawsuits are piling up against Tesla Motors (TSLA) over the Solar City (SCTY) merger"
stringTwo = "Lawsuits piling up against Tesla Motors (TSLA) with the Solar City (SCTY) merger"
print similarityScore(stringOne, stringTwo)
# 95.12%

stringTwo   = "Lawsuits piling up against Tesla Motors (TSLA) with the Solar City (SCTY) merger"
stringThree = "Bad news for Tesla Motors (TSLA) over the Solar City (SCTY) merger"
print similarityScore(stringTwo, stringThree)
# 82.19%

stringThree = "Bad news for Tesla Motors (TSLA) over the Solar City (SCTY) merger"
stringFour  = "Tesla Motors (TSLA) will not need to raise equity or debt before the end of the year"
print similarityScore(stringThree, stringFour)
# 59.33%
```

#### Text Processing
```python
textOne = "@TeslaMotors shares jump as shipments more than double! #winning"
print filter(textOne)
# shares jump as shipments more than double winning

textTwo = "Tesla announces its best sales quarter: http://trib.al/RbTxvSu $TSLA" 
print filter(textTwo)
# tesla announces its best sales quarter

textThree = "Tesla $TSLA reports deliveries of 24500, above most views."
print filter(textThree)
# tesla reports deliveries of number above most views
```

#### Sentiment Analysis
```python
textOne = "shares jump as shipments more than double winning"
print sentimentScore(textOne)
# 0.706

textTwo = "tesla reports deliveries of number above most views"
print sentimentScore(textTwo)
# 0.077

textThree = "not looking good for tesla competition on the rise"
print sentimentScore(textThree)
# -0.341
```
