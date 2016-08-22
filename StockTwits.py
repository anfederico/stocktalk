import urllib2
import json
import time
import re

def Stream(Ticker, Twits = []):
    response = urllib2.urlopen('https://api.stocktwits.com/api/2/streams/symbol/%s.json' % Ticker)
    data = response.read()
    data = json.loads(data)
    
    for message in data['messages']:
        
        # Body of twit
        Text =  message['body']
        
        # Bearish/Unknown/Bullish
        if message['entities']['sentiment'] == None:
            Sentiment = 'Unknown'
        else:
            Sentiment = message['entities']['sentiment']['basic'] 
        
        # Likes/Reshares
        try:
            Likes = message['likes']['total']
            Reshares = message['reshares']['reshared_count']
        except KeyError:
            Likes = 0
            Reshares = message['reshares']['reshared_count']
    
        Twit = {'Text': Text, 'Sentiment': Sentiment, 'Likes': Likes, 'Reshares': Reshares}
        Twits.append(Twit)
    
    return Twits

#Strips away irrelevant information
def PreprocessText(text):
    #Handle cash tags
    text = re.sub("$[^\s]+", "", text)
    #Lower case
    text = text.lower()
    #Handle numbers
    text = re.sub("[0-9]+", "number", text)
    #Handle replies/mentions/cashtags
    text = text.replace('$', '@')
    text = re.sub("@[^\s]+", "", text)
    #Handle URLs
    text = re.sub("(http|https)://[^\s]*", "", text)
    #Handle email addresses
    text = re.sub("[^\s]+@[^\s]+", "", text)
    return text
    
def Stocktwits(Ticker, Iterations = 1, Rest = 0):
    Twits = []
    while Iterations > 0:
        Twits += Stream(Ticker)
        time.sleep(Rest)
        Iterations -= 1
    return Twits

for tweet in Stocktwits('TSLA', 1): # Max 30 tweets per iteration
    twit = PreprocessText(tweet['Text'])
    print twit
