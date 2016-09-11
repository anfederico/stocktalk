import time
import sys
sys.path.insert(0, '/Scrapers')
from TwitterScrape    import TW_Scrape
from StockTwitsScrape import ST_Scrape
from GoogleNewsScrape import GN_Scrape

# Request 100 (max) tweets from Twitter each iteration
# Input rest (sec) between each iteration
# Credentials not shown, see TwitterScrape.py for setup example

TW_Sentiment = TW_Scrape(Credentials, Query = '$TSLA', Iterations = 1, Rest = 0)

# Request 30 (max) twits from Stock Twits each iteration
# Input rest (sec) between each iteration

ST_Sentiment = ST_Scrape(Ticker = 'TSLA', Iterations = 1, Rest = 0)

# Request pages of news headlines from Google News
# Input rest (sec) between each page

GN_Sentiment = GN_Scrape('Tesla Motors', Pages = 1, Rest = 0)

outfile = open('SocialSentimentLog.txt', 'a')
outfile.write(time.strftime("%m/%d/%Y %H:%M ")+
              'Twitter: '   +str(TW_Sentiment)+' '
              'StockTwits: '+str(ST_Sentiment)+' '
              'GoogleNews: '+str(GN_Sentiment)+'\n') 
outfile.flush()
