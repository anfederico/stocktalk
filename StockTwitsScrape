from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib2 import urlopen
import json
import time
import re

'''
Args:
    1. Ticker(str): You are searching twits referencing this ticker
    2. Iterations(int): Number of times you want to request twits from Stock Twits
        Default = 1
    3. Rest(int): Number of seconds you want to wait between each iteration
        Default = 0
        
Assumptions:
    Each iteration will request the last 30 twits

Returns:
    (int) Sentiment score based on tweets
'''

def ST_Scrape(Ticker, Iterations = 1, Rest = 0):
    
    # Request twits
    def StockTwitsStream(Ticker, Twits = []):
        Response = urlopen('https://api.stocktwits.com/api/2/streams/symbol/%s.json' % Ticker)
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
    
    # Filters spam and meaningless data
    def StockTwits_Filter(text):
        text = re.sub("$[^\s]+", "", text)
        text = text.lower()
        text = re.sub("[0-9]+", "number", text)
        text = text.replace('$', '@')
        text = re.sub("@[^\s]+", "", text)
        text = re.sub("(http|https)://[^\s]*", "", text)
        text = re.sub("[^\s]+@[^\s]+", "", text)
        return text
        
    # Analyze twits with NLTK Sentiment Analzyer
    def StockTwitsSentiment(Twits):
        SentimentScores = []
        for Twit in Twits:
            Support = Twit['Support']
            if Twit['Sentiment'] != 'None':
                if Twit['Sentiment'] == 'Bullish':
                    SentimentScores += [1]*Support
                elif Twit['Sentiment'] == 'Bearish':
                    SentimentScores += [-1]*Support
            else:
                Twit = StockTwits_Filter(Twit['Text'])
                Score = SentimentIntensityAnalyzer().polarity_scores(Twit)['compound']
                if Score != 0:
                    for i in range(0, Support+1):
                        SentimentScores.append(Score)
        return round(sum(SentimentScores)/len(SentimentScores),3)
    
    # Main    
    Twits = []
    while Iterations > 0:
        Twits += StockTwitsStream(Ticker)
        time.sleep(Rest)
        Iterations -= 1
    return StockTwitsSentiment(Twits)
