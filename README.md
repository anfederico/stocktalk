## Stock Talk Documentation
* StockTalk.py
   * Extracts sentiment values from Twitter, Stock Twits, and Google News simultaneously 
   * Pulls from three main functions defined in DataExtractors.py
   * Records data in a log called SocialSentimentLog.txt

* StockHistoricals.py
   * Pulls stock historical values from Yahoo Finance
   * Calculates momentum indicators based on past 14 trading periods, including:
     * Slow Stochastic Oscillator (SSO)
     * Relative Strength Index (RSI)
    * Also records Daily Percent Change (DPC) and Daily Trading Volume (DTV)  

### Purpose

The purpose of this repository is to provide two resources for predicting stock movement.

1. Calculating established momentum indicators with stock historical data.
2. Scraping social media websites and analzying social sentiment for a particular stock.

Combinations of these tools can lead to substancial data that can be fed to machine learning classification algorithms.
