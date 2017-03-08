import re
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

def getTracker(coins):
	tracker = {'Volume':{},'Sentiment':{},'Seconds':0}
	for coin in coins:
		tracker['Volume'][coin[0]] = 0
		tracker['Sentiment'][coin[0]] = {}
		tracker['Sentiment'][coin[0]]['all'] = []
		tracker['Sentiment'][coin[0]]['avg'] = 'N/A'
	return tracker

def getReversal(coins):
	reversal = {}
	for coin in coins:
		for term in coin:
			reversal[term] = coin[0]
	return reversal

def writeUpdates(filename, coins, tracker):
	with open(filename, 'w') as outfile:
		for coin in coins:
			outfile.write("%s,%d,%s\n" % (coin[0], tracker['Volume'][coin[0]], tracker['Sentiment'][coin[0]]['avg']))
			outfile.flush()

def elapsedTime(start):
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

class CoinListener(tweepy.StreamListener):

	def __init__(self, auth, coins, queries, refresh, path, realtime=False, logTracker=True, logTweets=True, logSentiment=False, debug=True): 
		
		self.api          = tweepy.API(auth)
		self.coins        = coins
		self.queries      = queries
		self.refresh      = refresh
		self.path         = path
		self.realtime     = realtime
		self.logTracker   = logTracker
		self.logTweets    = logTweets		
		self.logSentiment = logSentiment
		self.debug        = debug
		self.processing   = False
		self.timer        = time.time()
		self.reversal     = getReversal(coins)
		self.tracker      = getTracker(coins)

		# Initiate file for visualization
		if self.realtime:
			writeUpdates(('%supdates.txt' % self.path), self.coins, self.tracker)

	def process(self):
		# Record timer and reset
		self.tracker['Seconds'] += elapsedTime(self.timer)
		self.timer = time.time()
		
		# Copy tracking data to temporary tracker
		tempTracker = copy.deepcopy(self.tracker)
		self.tracker = getTracker(self.coins)

		# Calculate average sentiment
		if self.logSentiment:
			for coin in self.coins:
				try: tempTracker['Sentiment'][coin[0]]['avg'] = round(sum(tempTracker['Sentiment'][coin[0]]['all'])/len(tempTracker['Sentiment'][coin[0]]['all']),2)
				except ZeroDivisionError: tempTracker['Sentiment'][coin[0]]['avg'] = 'N/A'

		# Data logging
		if self.logTracker:
			for coin in self.coins:
				with open("%s%s_Tracker.txt" % (self.path, coin[0]), "a") as outfile:
					outfile.write("%s,%d,%s,%d\n" % (time.strftime('%m/%d/%Y %H:%M:%S'), tempTracker['Volume'][coin[0]], tempTracker['Sentiment'][coin[0]]['avg'], tempTracker['Seconds']))

		# Data visualization
		if self.realtime:
			writeUpdates(('%supdates.txt' % self.path), self.coins, tempTracker)

		# Print to console
		if self.debug:
			print("---%s---" % time.strftime('%H:%M:%S'))
			for coin in self.coins:
				print("%s Volume: %s" % (coin[0], tempTracker['Volume'][coin[0]]))
				print("%s Sentiment: %s" % (coin[0], tempTracker['Sentiment'][coin[0]]['avg']))
			print('\n')

		self.processing = False

	def on_status(self, status):
		tweetOrgnl = status.text 
		tweetLower = tweetOrgnl.lower()

		# For every incoming tweet...
		for query in self.queries:
			if query.lower() in tweetLower:
				
				# Categorize tweet
				lookup = self.reversal[query]

				# Increment count
				self.tracker['Volume'][lookup] += 1
				
				# Sentiment analysis
				if self.logSentiment:
					tweetPrcsd = process(tweetLower)
					tweetScore = SentimentIntensityAnalyzer().polarity_scores(tweetPrcsd)["compound"]
					self.tracker['Sentiment'][lookup]['all'].append(tweetScore)
				else: tweetScore = 'N/A'

				# Log tweet
				if self.logTweets:
					with codecs.open("%s%s_Tweets.txt" % (self.path, lookup), "a", encoding='utf8') as outfile:
						outfile.write("%s,%s,%s\n" % (time.strftime('%m/%d/%Y %H:%M:%S'), tweetOrgnl, tweetScore))

				# Check refresh
				if elapsedTime(self.timer) >= self.refresh:
					if not self.processing:
						self.processing = True
						processingThread = threading.Thread(target=self.process)
						processingThread.start()
		return True
 
	def on_error(self, status_code):
		if status_code == 413 or status_code == 420 or status_code == 503:
			print("Got an error with status code: %d" % status_code)
			with open("%sError_Log.txt" % self.path, "a") as outfile:
				outfile.write("%s Error: %d\n" % (time.strftime('%m/%d/%Y %H:%M'), status_code))	
			return False
		print('Got an error with status code: %d' % status_code)
		return True # To continue listening
 
	def on_timeout(self):
		print("Timeout...")
		return True # To continue listening
 

 
# Streaming --------------------------------------------------

def streaming(credentials, coins, queries, refresh, path, realtime=False, logTracker=True, logTweets=True, logSentiment=False, debug=True):

	# User Error Checks
	if len(coins)   <= 0:  print("Error: You must include at least one coin."); return
	if len(coins)   >= 10: print("Warning: Fewer than ten coins recommended.")
	if len(queries) <= 0:  print("Error: You must include at least one query."); return
	if len(queries) >= 20: print("Warning: Fewer than twenty queries recommended.")
	if refresh      <= 0:  print("Error: Refresh rate must be greater than 0"); return

	auth = tweepy.OAuthHandler(credentials[0], credentials[1])
	auth.set_access_token(credentials[2], credentials[3])

	if logSentiment:
		global SentimentIntensityAnalyzer
		from nltk.sentiment.vader import SentimentIntensityAnalyzer

	while True:

		# Start streaming -----------------------------
		try:
			print("Streaming Now...")
			listener = CoinListener(auth, coins, queries, refresh, path, realtime, logTracker, logTweets, logSentiment, debug)
			stream = tweepy.Stream(auth, listener)
			stream.filter(track=queries)

		except (Timeout, ConnectionError, ReadTimeoutError):
			print("Reestablishing Connection...")
			with open("%sError_Log.txt" % path, "a") as outfile:
				outfile.write("%s Error: Connection Dropped\n" % time.strftime('%m/%d/%Y %H:%M'))

		time.sleep((15*60)+1) # Wait at least 15 minutes before restarting listener

		# ---------------------------------------------