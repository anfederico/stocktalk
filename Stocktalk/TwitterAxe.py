import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from twitter import Twitter, OAuth
from datetime import datetime
from matplotlib.dates import DateFormatter
from csv import DictWriter
from re import sub
from pandas import DataFrame
from time import time, gmtime, localtime, strftime, sleep
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import schedule

def filter(text):
    text = text.lower()
    text = sub("[0-9]+", "number", text)
    text = sub("#", "", text)
    text = sub("\n", "", text)
    text = text.replace('$', '@')
    text = sub("@[^\s]+", "", text)
    text = sub("(http|https)://[^\s]*", "", text)
    text = sub("[^\s]+@[^\s]+", "", text)
    text = sub('[^a-z A-Z]+', '', text)
    return text

def similarityScore(s1, s2):
    if len(s1) == 0: return len(s2)
    elif len(s2) == 0: return len(s1)
    v0 = [None]*(len(s2) + 1)
    v1 = [None]*(len(s2) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s1)):
        v1[0] = i + 1
        for j in range(len(s2)):
            cost = 0 if s1[i] == s2[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return 100-((float(v1[len(s2)])/(len(s1)+len(s2)))*100)

def sentimentScore(texts):
    scores = []
    for text in texts:
        score = SentimentIntensityAnalyzer().polarity_scores(text)["compound"]
        if score != 0: scores.append(score)
    try: return round(sum(scores)/len(scores),3)
    except ZeroDivisionError: return 0
     
class TwitterAxe:
    
    def __init__(self, userCredentials):
        self.credentials = Twitter(auth=OAuth(userCredentials[0], userCredentials[1], userCredentials[2], userCredentials[3]))
        self.query            = ""
        self.amount           = 50
        self.cutoff           = 90
        self.filteredOutCount = 0
        self.filteredInCount  = 0
        self.filteredIn       = []
        self.filteredOut      = []
        self.binnedTweets     = []
        self.groupedTweets    = []
        self.timeSeries       = []
    
    def requestTweets(self):
        tweets = self.credentials.search.tweets(q=self.query, count=self.amount, result_type='recent', lang='en')['statuses']
        
        for tweet in tweets:
            tweet = tweet['text']
            t1 = filter(tweet)
            highScore = 0
            for t2 in self.binnedTweets:
                score = similarityScore(t1, t2)
                if score > highScore: highScore = score
            
            if highScore < self.cutoff:
                self.filteredInCount += 1
                if len(self.binnedTweets) >= 50: 
                    self.binnedTweets.pop()
                self.binnedTweets.insert(0, t1)
                self.groupedTweets.append(t1)
                self.filteredIn.append(tweet)
            else: 
                self.filteredOutCount += 1
                self.filteredOut.append(tweet)
    
    def analyzeGroup(self):
        self.timeSeries.append({ "time"      : strftime("%I:%M:%S %p", localtime()),
                                 "sentiment" : sentimentScore(self.groupedTweets), 
                                 "tweets"    : len(self.groupedTweets)})             
        self.groupedTweets = []

    def mine(self, query, minePeriod, requestFrequency, analyzeFrequency, requestAmount = 50, similarityCutoff = 90):
        self.query = query
        self.cutoff = similarityCutoff
        self.amount = requestAmount
        
        startStr = strftime("[%Y/%m/%d %I:%M:%S %p]", localtime())
        schedule.every(requestFrequency).seconds.do(self.requestTweets)
        schedule.every(analyzeFrequency).seconds.do(self.analyzeGroup)
        
        end = time()+minePeriod
        while time() <= end:
            schedule.run_pending()
            
        endStr = strftime("[%Y/%m/%d %I:%M:%S %p]", localtime())
        print "Mine complete from\n" + startStr +" - " + endStr +"\n"
    
    def showInventory(self):
        print "\033[1m"+"Inventory"+"\033[0m"
        print "Unique Tweets: "+str(self.filteredInCount)
        print "Filtered Tweets: "+str(self.filteredOutCount)
        print 
        
    def showUniqueTweets(self):
        print "\033[1m"+"Unique Tweets"+"\033[0m"
        print DataFrame(self.filteredIn) 
        
    def exportUniqueTweets(self):
        outfile = open("UniqueTweets.txt", 'w')
        for tweet in self.filteredIn:
            try: outfile.write(tweet+'\n') 
            except: pass
        outfile.close()    
   
    def showFilteredTweets(self):
        print "\033[1m"+"Filtered Tweets"+"\033[0m"      
        print DataFrame(self.filteredOut) 
        print
        
    def exportFilteredTweets(self):
        outfile = open("FilteredTweets.txt", 'w')
        for tweet in self.filteredOut:
            try: outfile.write(tweet+'\n') 
            except: pass
        outfile.close()      
    
    def showTimeSeries(self):
        print "\033[1m"+"Time Series"+"\033[0m"
        columns = ["time", "sentiment", "tweets"]
        print DataFrame(self.timeSeries, columns=columns)
        print
    
    def exportTimeSeries(self):
        with open("Sentiment.txt", 'w') as outfile:
            writer = DictWriter(outfile, fieldnames=['time', 'sentiment', 'tweets'])
            writer.writeheader()
            for datapoint in self.timeSeries:
                writer.writerow({ "time"      : datapoint["time"],
                                  "sentiment" : datapoint["sentiment"],
                                  "tweets"    : datapoint["tweets"]})
     
    def savePlot(self, name, width = 6, height = 4.5):
        timestamps = []
        sentiment = []
        tweets = []
        for time in self.timeSeries:
            timestamps.append(datetime.strptime(time["time"], '%I:%M:%S %p'))
            sentiment.append(time["sentiment"])
            tweets.append(time["tweets"])

        # Plot setup
        ax1 = plt.figure(figsize=(width, height)).add_subplot(111)  
        ax1.spines["top"].set_visible(False)   
        ax1.get_xaxis().tick_bottom()  
        ax1.get_yaxis().tick_left()   
        ax1.xaxis.set_major_formatter(DateFormatter('%I:%M %p')) 
        lns1 = ax1.plot(timestamps, sentiment, color="dimgrey", lw=0.75, label="Sentiment")
        plt.yticks(fontsize=8)
        plt.ylim(ymin=-1, ymax=1)
        plt.xticks(rotation=50, fontsize=8) 
        ax2 = ax1.twinx()
        lns2 = ax2.plot(timestamps, tweets, color="dodgerblue", lw=0.5, label="Tweets")
        ax2.margins(0.05)
        plt.yticks(fontsize=8)  
        
        # Labeling
        ax1.legend(lns1+lns2, ['Sentiment', 'Tweets'], loc=0, frameon=False, fontsize=6)
        ax1.set_ylabel("Sentiment", weight="light", rotation=90, fontsize=9, labelpad=1)
        ax2.set_ylabel("Tweets", weight="light", rotation=-90, fontsize=9, labelpad=15)
        plt.title("Tweet Sentiment", weight ="light", fontsize=12, y=1.08)  
        plt.ylim(ymin=0)
        plt.tight_layout()
        plt.savefig(name+".png")

    def showPlot(self):
        timestamps = []
        sentiment = []
        tweets = []
        for time in self.timeSeries:
            timestamps.append(datetime.strptime(time["time"], '%I:%M:%S %p'))
            sentiment.append(time["sentiment"])
            tweets.append(time["tweets"])

        # Plot setup
        ax1 = plt.figure(figsize=(6, 4.5)).add_subplot(111)  
        ax1.spines["top"].set_visible(False)   
        ax1.get_xaxis().tick_bottom()  
        ax1.get_yaxis().tick_left()   
        ax1.xaxis.set_major_formatter(DateFormatter('%I:%M %p')) 
        lns1 = ax1.plot(timestamps, sentiment, color="dimgrey", lw=0.75, label="Sentiment")
        plt.yticks(fontsize=8)
        plt.ylim(ymin=-1, ymax=1)
        plt.xticks(rotation=50, fontsize=8) 
        ax2 = ax1.twinx()
        lns2 = ax2.plot(timestamps, tweets, color="dodgerblue", lw=0.5, label="Tweets")
        ax2.margins(0.05)
        plt.yticks(fontsize=8)  
        
        # Labeling
        ax1.legend(lns1+lns2, ['Sentiment', 'Tweets'], loc=0, frameon=False, fontsize=6)
        ax1.set_ylabel("Sentiment", weight="light", rotation=90, fontsize=9, labelpad=1)
        ax2.set_ylabel("Tweets", weight="light", rotation=-90, fontsize=9, labelpad=15)
        plt.title("Tweet Sentiment", weight ="light", fontsize=12, y=1.08)  
        plt.ylim(ymin=0)
        plt.tight_layout()
        plt.show()
