####################################
#             Twitter              #
####################################

from twitter import Twitter as TWTR, OAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import re
import time

# Credentials to access Twitter API 
# ACCESS_TOKEN    = 'XXXXXXXXXXXXXXXXXXXXXXX'
# ACCESS_SECRET   = 'XXXXXXXXXXXXXXXXXXXXXXX'
# CONSUMER_KEY    = 'XXXXXXXXXXXXXXXXXXXXXXX'
# CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'

# Initiate the connection to Twitter Streaming API
# auth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
# Credentials = TWTR(auth=auth)

def Twitter(Credentials, Query, Amount, Iterations = 1, Rest = 0): # Max 30 tweets per iteration, rest between each iteration

    def Twitter_Stream(Query, Amount, Storage):
        Iterator = Credentials.search.tweets(q=Query, result_type='recent', lang='en', count=Amount)
        for Tweet in Iterator["statuses"]:
            Storage[json.dumps(Tweet['text'])] = None
    
    def Twitter_Filter(text):
        text = text.lower()
        text = re.sub("[0-9]+", "number", text)
        text = re.sub("rt", "", text)
        text = text.replace('$', '@')
        text = text.replace('\n', '@')
        text = re.sub("@[^\s]+", "", text)
        text = re.sub("(http|https)://[^\s]*", "", text)
        text = re.sub("[^\s]+@[^\s]+", "", text)
        return text
    
    def Twitter_Sentiment(Tweets):
        SentimentScores = []
        for Tweet in Tweets:
            Tweet = Twitter_Filter(Tweet)
            print Tweet
            Score = SentimentIntensityAnalyzer().polarity_scores(Tweet)['compound']
            if Score != 0:
                SentimentScores.append(Score)
        return round(sum(SentimentScores)/len(SentimentScores),3)
    
    Tweets = {}
    Loops = 1
    while Loops > 0:
        Twitter_Stream(Query, Amount, Tweets)
        time.sleep(0)
        Loops -= 1
    return Twitter_Sentiment(Tweets)

####################################
#           StockTwits             #
####################################

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import urllib2
import json
import time
import re

def StockTwits(Ticker, Iterations = 1, Rest = 0): # Max 30 tweets per iteration, rest between each iteration
    
    def StockTwits_Stream(Ticker, Twits = []):
        Response = urllib2.urlopen('https://api.stocktwits.com/api/2/streams/symbol/%s.json' % Ticker)
        Data = Response.read()
        Data = json.loads(Data)
        for Message in Data['messages']:
            Text =  Message['body']
            if Message['entities']['sentiment'] != None:
                Sentiment = Message['entities']['sentiment']['basic'] 
            else:
                Sentiment = 'None'
            try:
                Likes = Message['likes']['total']
                Reshares = Message['reshares']['reshared_count']
            except KeyError:
                Likes = 0
                Reshares = Message['reshares']['reshared_count']
            Twit = {'Text': Text, 'Sentiment': Sentiment, 'Support': Likes+Reshares}
            Twits.append(Twit)
        return Twits    
    
    def StockTwits_Filter(text):
        text = re.sub("$[^\s]+", "", text)
        text = text.lower()
        text = re.sub("[0-9]+", "number", text)
        text = text.replace('$', '@')
        text = re.sub("@[^\s]+", "", text)
        text = re.sub("(http|https)://[^\s]*", "", text)
        text = re.sub("[^\s]+@[^\s]+", "", text)
        return text
        
    Twits = []
    while Iterations > 0:
        Twits += StockTwits_Stream(Ticker)
        time.sleep(Rest)
        Iterations -= 1
    
    SentimentScores = []
    for Twit in Twits:
        Support = Twit['Support']
        if Twit['Sentiment'] != 'None':
            if Twit['Sentiment'] == 'Bullish':
                for i in range(0, Support+1):
                    SentimentScores.append(1)
            elif Twit['Sentiment'] == 'Bearish':
                for i in range(0, Support+1):
                    SentimentScores.append(-1)
        else:
            Twit = StockTwits_Filter(Twit['Text'])
            Score = SentimentIntensityAnalyzer().polarity_scores(Twit)['compound']
            if Score != 0:
                for i in range(0, Support+1):
                    SentimentScores.append(Score)
    return round(sum(SentimentScores)/len(SentimentScores),3)
