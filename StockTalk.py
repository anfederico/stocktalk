import time
from Twitter import Twitter
from DataExtractors StockTwits, GoogleNews

# Request 100 (max) tweets from Twitter each iteration
# Input rest (sec) between each iteration
# Edit API credentials in Twitter.py
TW_Sentiment = Twitter(Credentials, Query = '$TSLA', Iterations = 5, Rest = 60)

# Request 30 (max) twits from StockTwiters each iteration
# Input rest (sec) between each iteration
ST_Sentiment = StockTwits(Ticker = 'TSLA', Iterations = 1, Rest = 0)

# Request 10 (limit) pages of news headlines from Google News
# Input rest (sec) between each page
GN_Sentiment = GoogleNews('Tesla Motors', Pages = 5, Rest = 10)

outfile = open('SocialSentimentLog.txt', 'a')
outfile.write(time.strftime("%m/%d/%Y %H:%M ")+
              'Twitter: '   +str(TW_Sentiment)+' '
              'StockTwits: '+str(ST_Sentiment)+' '
              'GoogleNews: '+str(GN_Sentiment)+'\n') 
outfile.flush()
