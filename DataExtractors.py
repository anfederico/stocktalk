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
        
    # Stream Twits    
    Twits = []
    while Iterations > 0:
        Twits += StockTwits_Stream(Ticker)
        time.sleep(Rest)
        Iterations -= 1
    
    # Calculate sentiment scores
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
