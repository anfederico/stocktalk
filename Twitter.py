from twitter import Twitter as TWTR, OAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import re
import time

'''
Args:
    1. Credentials(arr): Use OAuth and TWTR (Renamed from Twitter API to avoid conflict)
        Ex. ACCESS_TOKEN    = 'XXXXXXXXXXXXXXX'
            ACCESS_SECRET   = 'XXXXXXXXXXXXXXX'
            CONSUMER_KEY    = 'XXXXXXXXXXXXXXX'
            CONSUMER_SECRET = 'XXXXXXXXXXXXXXX'
            Auth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
            Credentials = TWTR(auth=Auth)
    2. Query(str): You are search tweets based on this keyword(s)
    3. Amount(int): Number of tweets you want to search per iteration
        Default = 100
        Max = 100
    4. Iterations(int): Number of times you want to request the Amount of tweets from Twitter
        Default = 1
    5. Rest(int): Number of seconds you want to wait between each iteration
        Default = 0
        
Assumptions:
    Tweets are sorted by recent and english

Returns:
    int: Sentiment score based on tweets
'''

def Twitter(Credentials, Query, Amount = 100, Iterations = 1, Rest = 0):

    # Connect to twitter with credentials and request tweets
    def TwitterStream(Credentials, Query, Amount, Storage):
        Iterator = Credentials.search.tweets(q=Query, result_type='recent', lang='en', count=Amount)
        for Tweet in Iterator["statuses"]:
            Storage[json.dumps(Tweet['text'])] = None
    
    # Filters spam and meaningless data
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
    
    # Analyze tweets with NLTK Sentiment Analyzer
    def Twitter_Sentiment(Tweets):
        SentimentScores = []
        for Tweet in Tweets:
            Tweet = Twitter_Filter(Tweet)
            Score = SentimentIntensityAnalyzer().polarity_scores(Tweet)['compound']
            if Score != 0:
                SentimentScores.append(Score)
        return round(sum(SentimentScores)/len(SentimentScores),3)
    
    # Main
    Tweets = {}
    while Iterations > 0:
        TwitterStream(Credentials, Query, Amount, Tweets)
        time.sleep(0)
        Iterations -= 1
    return Twitter_Sentiment(Tweets)
