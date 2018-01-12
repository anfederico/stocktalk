<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Stocktalk/master/media/Design.png" width=60%></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v2.7%20%2F%20v3.6-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/Stocktalk.svg)](https://github.com/anfederico/stocktalk/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Purpose
*Stocktalk is a visualization tool that tracks tweet volume and sentiment on Twitter, given a series of queries.*

*It does this by opening a local websocket with Twitter and pulling tweets that contain user-specified keywords. For example, I can tell Stocktalk to grab all tweets that mention Ethereum and periodically tally volume and measure average sentiment every 15 minutes.*

*It will then record this data continuously and update an online database that can be used to visualize the timeseries data via an interactive Flask-based web application.*

## Demo
[https://anfederico.github.io/Stocktalk/](https://anfederico.github.io/Stocktalk/)

# Prerequisites
> Stocktalk requires API credentials with Twitter and Mlab

#### Twitter Steps (Creating an application)
1. Sign into Twitter at [apps.twitter.com](apps.twitter.com)
2. Create a new application and fill out details
3. Generate an access token
4. Save the following information
	- Consumer Key
	- Consumer Secret
	- Access Token
	- Access Token Secret

#### Mlab Steps (Setting up an online database)
1. Make an account at [https://mlab.com](https://mlab.com)
2. Create a new deployment in sandbox mode
3. Add a database user to your deployment
4. Save the following information
	- Mongo deployment server
	- Mongo deployment id
	- Mongo deployment client
	- Deployment user
	- Deployment pass

## Download
```bash
# Clone repository and install dependencies
$ git clone https://github.com/anfederico/Stocktalk
$ pip install -r Stocktalk/requirements.txt

# Install natural language toolkit sentiment corpus
$ python -m nltk.downloader vader_lexicon
```

## Edit Settings
```
/stocktalk
└── /scripts
    └── settings.py
```
```python
# Mongo
mongo_server = 'ds254236.mlab.com'
mongo_id     =  54236
mongo_client = 'stocktalk'
mongo_user   = 'username'
mongo_pass   = 'password'

# Twitter
api_key             = ''
api_secret          = ''
access_token        = ''
access_token_secret = ''
credentials = [api_key, api_secret, access_token, access_token_secret]
```

## Code Examples
#### Twitter Streaming
> This file opens the websocket and writes to the online databse until manually interrupted
```
/stocktalk
└── listen.py

$ python listen.py
```
```python
from scripts import settings

# Each key or category corresponds to an array of keywords used to pull tweets
queries = {'ETH': ['ETH', 'Ethereum'],
           'LTC': ['LTC', 'Litecoin'],
           'BTC': ['BTC', 'Bitcoin'],
           'XRP': ['XRP', 'Ripple'],
           'XLM': ['XLM', 'Stellar']}

# Aggregate volume and sentiment every 15 minutes
refresh = 15*60

streaming.streamer(settings.credentials, 
                   queries, 
                   refresh, 
                   sentiment=True, 
                   debug=True)
```

#### Realtime Visualization
> This file initiates a local web-application which pulls data from the online database
```
/stocktalk
└── app.py

$ python app.py
```

## Underlying Features
##### Text Processing
```python
t1 = "@TeslaMotors shares jump as shipments more than double! #winning"
print(process(t1))

t2 = "Tesla announces its best sales quarter: http://trib.al/RbTxvSu $TSLA" 
print(process(t2))

t3 = "Tesla $TSLA reports deliveries of 24500, above most views."
print(process(t3))
```

```text
shares jump as shipments more than double winning
tesla announces its best sales quarter
tesla reports deliveries of number above most views
```

##### Sentiment Analysis
```python
t1 = "shares jump as shipments more than double winning"
print(sentiment(t1))

t2 = "tesla reports deliveries of number above most views"
print(sentiment(t2))

t3 = "not looking good for tesla competition on the rise"
print(sentiment(t3))
```

```text
0.706
0.077
-0.341
```
