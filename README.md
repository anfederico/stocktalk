## Stock Talk Documentation
* StockTalk.py
   * Extract sentiment values from Twitter, StockTwits, and Google News simultaneously 
   * Pulls from three main functions defined in DataExtractors.py
   * Records data in a log called SocialSentimentLog.txt

* StockHistoricals.py
   * Pulls stock historical values from Yahoo Finance
   * Calculates momentum indicators based on past 14 trading peroids, including:
     * Slow Stochastic Oscillator (SSO)
     * Relative Strength Index (RSI)
