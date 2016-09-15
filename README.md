# Stock Talk Documentation
<i>Software designed to scrape and analyze social media sentiment about particular stocks</i>

### Python Requirements
    csv
    os
    selenium
    numpy
    matplotlib
    sklearn
    
### Stock Talk Documentation

### StockTalk.py
   * Extracts sentiment values from Twitter, Stock Twits, and Google News simultaneously 
   * Pulls from three main functions in /Scrapers
      * TwitterScrape.py
      * StockTwitsScrape.py
      * GoogleNewsScrape.py
   * Records data in a log called SocialSentimentLog.txt

### Purpose

The purpose of this repository is to provide resources for scraping social media websites and analzying social sentiment for a particular stock. Using these tools can provide substancial raw data that can be fed to clustering algorithms.
