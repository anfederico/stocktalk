import time
from DataExtractors import Twitter, StockTwits, GoogleNews

# Request 100 (max) tweets from Twitter each iteration
# Input rest (sec) between each iteration
# Edit API credentials in DataExtractors.py file

TW_Sentiment = Twitter(Query = '$TSLA', Iterations = 1, Rest = 0)

# Request 30 (max) twits from StockTwiters each iteration
# Input rest (sec) between each iteration

ST_Sentiment = StockTwits(Ticker = 'TSLA', Iterations = 1, Rest = 0)

# Request 10 (limit) pages of news headlines from Google News
# Input rest (sec) between each page

GN_Sentiment = GoogleNews('Tesla Motors', Pages = 1, Rest = 0)


outfile = open('SocialSentimentLog.txt', 'a')
outfile.write(time.strftime("%m/%d/%Y %H:%M ")+
              'Twitter: '   +str(TW_Sentiment)+' '
              'StockTwits: '+str(ST_Sentiment)+' '
              'GoogleNews: '+str(GN_Sentiment)+'\n') 
outfile.flush()
