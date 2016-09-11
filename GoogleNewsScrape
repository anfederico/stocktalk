from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import requests
import time
import random

'''
Args:
    1. Query: You are searching news stories based on this keyword(s)
    2. Iterations(int): Number of pages of stories you want to request from Google News
        Default = 1
    3. Rest(int): Max number of seconds you want to wait between pages (varies to mimic a user)
        Default = 0
        
Assumptions:
    When requesting multiple pages, set rest at least to 15 seconds

Returns:
    (int) Sentiment score based on tweets
'''

def GN_Scrape(Query, Pages = 1, Rest = 0):

    # Assemble the URL to make news request
    def CreateURLs(Query, Pages):
        URLs = []
        for Page in range(0, Pages):
            url = 'https://www.google.com/search?q=%22'
            url += Query.lower().replace(' ','+')                      
            url += '%22&tbm=nws&tbs=qdr:y#q=%22'                                        
            url += Query.lower().replace(' ','+')                                 
            url += '%22&safe=active&tbs=qdr:y,sbd:1&tbm=nws&start='+str(Page*10)
            URLs.append(url)
        return URLs
   
    # Request URL from Google News   
    def GoogleNewsStream(Query, Pages, Rest = 0):
        URLs = CreateURLs(Query, Pages)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        Titles = []
        Links = []
        for url in URLs:
            Response = requests.get(url, headers=headers)
            Soup = BeautifulSoup(Response.text, "html.parser")
            Title =  [a.get_text() for a in Soup.find_all("a", class_="_HId")]
            Title += [a.get_text() for a in Soup.find_all("a", class_="_sQb")]
            for t in Title:
                Titles.append(t)
            time.sleep(random.randint(Rest/2, Rest))
        return Titles    
    
    # Main
    Titles = GoogleNewsStream(Query, Pages, 10)    
    SentimentScores = []
    for Title in Titles:
        Score = SentimentIntensityAnalyzer().polarity_scores(Title)['compound']
        if Score != 0:
            SentimentScores.append(Score) 
    return round(sum(SentimentScores)/len(SentimentScores),3)
