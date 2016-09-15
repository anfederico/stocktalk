# Stock Talk Documentation
<i>Software designed to scrape and analyze social media sentiment about particular stocks</i>

### Python Requirements
    re
    json
    urllib2
    requests
    time
    random
    beautifulsoup
    nltk
    twython
    vader
    scipy
    scikit learn
    numpy
    yahoofinance
    collections
    copy
    csv
    
### StockTalk.py
    Extracts sentiment values from Twitter, Stock Twits, and Google News simultaneously 
    Pulls from three main functions
    TwitterScrape.py
    StockTwitsScrape.py
    GoogleNewsScrape.py
    Records data in a log called SocialSentimentLog.txt

### Purpose
    The purpose of this repository is to provide resources for scraping social media websites and analzying social sentiment for a particular stock. Using these tools can provide substancial raw data that can be fed to clustering algorithms.
