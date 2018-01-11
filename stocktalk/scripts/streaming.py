import re
import sys
import time
import copy
import threading
import codecs
import tweepy
from   tweepy.api import API

# Special Exceptions
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError

# Local Files
sys.path.append("..")
from scripts import mongio

def get_tracker(queries):
    return {query: {'volume': 0, 'scores': []} for query in queries}

def get_reverse(queries):
    reverse = {}
    for query in queries:
        for keyword in queries[query]:
            reverse[keyword] = query
    return reverse

def elapsed_time(start):
    return (time.time()-start)

def process(text):
    text = re.sub("[0-9]+", "number", text)
    text = re.sub("#", "", text)
    text = re.sub("\n", "", text)
    text = re.sub("$[^\s]+", "", text)
    text = re.sub("@[^\s]+", "", text)
    text = re.sub("(http|https)://[^\s]*", "", text)
    text = re.sub("[^\s]+@[^\s]+", "", text)
    text = re.sub('[^a-z A-Z]+', '', text)
    return text

class Listener(tweepy.StreamListener):

    def __init__(self, auth, queries, refresh, sentiment=False, debug=False):
        self.api         = tweepy.API(auth)
        self.queries     = queries.keys()
        self.refresh     = refresh      
        self.sentiment   = sentiment
        self.processing  = False
        self.timer       = time.time()
        self.debug       = debug
        self.reverse     = get_reverse(queries)
        self.tracker     = get_tracker(self.queries)

    def process(self):
        # Reset timer
        self.timer = time.time()
        
        # Copy tracking data to temporary tracker
        previous_tracker = copy.deepcopy(self.tracker)
        self.tracker = get_tracker(self.queries)

        # Update database
        for query in previous_tracker:
            
            if self.sentiment:
                scores = previous_tracker[query]['scores']
                try: 
                    sentiment = round(sum(scores)/len(scores) ,2)
                except ZeroDivisionError: 
                    sentiment = 0
            else:
                sentiment = 0
            
            volume = previous_tracker[query]['volume']
            timestamp = time.strftime('%m/%d/%Y %H:%M:%S')

            mongio.push(query, 'logs', {'timestamp' : timestamp,
                                        'volume'    : volume,
                                        'sentiment' : sentiment})

            if self.debug:
                print('Query', query)
                print('Timestamp', timestamp)
                print('Volume', volume)
                print('Sentiment', sentiment)
                print('-------\n')

        self.processing = False

    def on_status(self, status):
        original_tweet = status.text 

        # For every incoming tweet...
        for query in self.queries:
            if query.lower() in original_tweet.lower():
                
                # Categorize tweet
                lookup = self.reverse[query]
    
                # Increment count
                self.tracker[lookup]['volume'] += 1

                # Sentiment analysis
                if self.sentiment:
                    processed_tweet = process(original_tweet.lower())
                    score = SentimentIntensityAnalyzer().polarity_scores(processed_tweet)['compound']
                    self.tracker[lookup]['scores'].append(score)

                # Check refresh
                if elapsed_time(self.timer) >= self.refresh:
                    if not self.processing:
                        self.processing = True
                        processing_thread = threading.Thread(target=self.process)
                        processing_thread.start()
        return True
 
    def on_error(self, status_code):
        print("{0} Error: {1}\n".format(time.strftime('%m/%d/%Y %H:%M:%S'), status_code)) 
        if status_code == 413 or status_code == 420 or status_code == 503:
            return False
        return True # To continue listening
 
    def on_timeout(self):
        print("Timeout...")
        return True # To continue listening
 
# Streaming --------------------------------------------------

def streamer(credentials, queries, refresh, sentiment=False, debug=False):
    keywords = [i for j in queries.values() for i in j]

    # User Error Checks
    if len(queries)  <= 0:  print("Error: You must include at least one query."); return
    if len(queries)  >= 10: print("Warning: Fewer than ten query recommended.")
    if len(keywords) <= 0:  print("Error: You must include at least one keyword."); return
    if len(keywords) >= 20: print("Warning: Fewer than twenty keywords recommended.")
    if refresh       <= 0:  print("Error: Refresh rate must be greater than 0"); return

    auth = tweepy.OAuthHandler(credentials[0], credentials[1])
    auth.set_access_token(credentials[2], credentials[3])

    if sentiment:
        global SentimentIntensityAnalyzer
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

    while True:

        # Start streaming -----------------------------
        try:
            print("Streaming Now...")
            listener = Listener(auth, queries, refresh, sentiment, debug)
            stream = tweepy.Stream(auth, listener)
            stream.filter(track=keywords)

        except (Timeout, ConnectionError, ReadTimeoutError):
            print("{0} Error: Connection Dropped\n".format(time.strftime('%m/%d/%Y %H:%M:%S')))
            print("Re-establishing Connection...")

        time.sleep((15*60)+1) # Wait at least 15 minutes before restarting listener

        # ---------------------------------------------
