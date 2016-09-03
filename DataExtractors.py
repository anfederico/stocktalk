####################################
#             Twitter              #
####################################

from twitter import Twitter as TWTR, OAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import re
import time

def Twitter(Query, Amount = 100, Iterations = 1, Rest = 0): # Max 100 tweets per iteration, rest between each iteration

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
            Score = SentimentIntensityAnalyzer().polarity_scores(Tweet)['compound']
            if Score != 0:
                SentimentScores.append(Score)
        return round(sum(SentimentScores)/len(SentimentScores),3)
    
    ACCESS_TOKEN    = '3325237643-7tdg4mD7GLA5ylY2XsZI9h2CRophWJJZHEkyivk'
    ACCESS_SECRET   = 'gb6TwH1STRGNWMxUWSo42q6V6Ed7CaKS9FPQq4TIyRf6Q'
    CONSUMER_KEY    = 'FAu8rlIKWtQ27k0SkeEQx1MWm'
    CONSUMER_SECRET = 'VNHrKtsJWhyAkmFsErHNFanYEXguEz9LSFyTuoEkcyy5LyvCLv'
    auth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    Credentials = TWTR(auth=auth)
    
    Tweets = {}
    while Iterations > 0:
        Twitter_Stream(Query, Amount, Tweets)
        time.sleep(0)
        Iterations -= 1
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

####################################
#           GoogleNews             #
####################################

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import requests
import time
import random

def GoogleNews(Query, Pages = 1, Rest = 0): # Limit to 10 Pages, rest between each page

    def CreateURLs(Query, Pages):
        URLs = []
        for Page in range(0, Pages):
            url = 'https://www.google.com/search?q=%22'
            url += Query.lower().replace(' ','+')                      
            url += '%22&tbm=nws&tbs=qdr:y#q=%22'                                        
            url += Query.lower().replace(' ','+')                                 
            url += '%22&safe=active&tbs=qdr:y,sbd:1&tbm=nws&start='+str(Page*10)
            URLs.append(url)
        return URLs
   
    def GoogleNews_Stream(Query, Pages, Rest = 0):
        URLs = CreateURLs(Query, Pages)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        Titles = []
        Links = []
        for url in URLs:
            Response = requests.get(url, headers=headers)
            Soup = BeautifulSoup(Response.text, "html.parser")
            Title =  [a.get_text() for a in Soup.find_all("a", class_="_HId")]
            Title += [a.get_text() for a in Soup.find_all("a", class_="_sQb")]
            for t in Title:
                Titles.append(t)
            time.sleep(random.randint(Rest/2, Rest))
        return Titles    
    
    Titles = GoogleNews_Stream(Query, Pages, 10)    
    SentimentScores = []
    for Title in Titles:
        Score = SentimentIntensityAnalyzer().polarity_scores(Title)['compound']
        if Score != 0:
            SentimentScores.append(Score) 
    return round(sum(SentimentScores)/len(SentimentScores),3)
