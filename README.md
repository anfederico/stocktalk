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
