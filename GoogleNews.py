from bs4 import BeautifulSoup
import requests
import time
import random

# There are three parts to the URL when you search google news by recent 
# 1. Query / 2. Query / 3. Page number (0, 10, 20, 30,...)
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
    
def GoogleNews(Query, Pages):
    # Create URLs
    URLs = CreateURLs(Query, Pages)
    # Pretend to be a web broswer
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # Extract titles and links
    Titles = []
    Links = []
    for url in URLs:
        # Request response / HTML parser
        Response = requests.get(url, headers=headers)
        Soup = BeautifulSoup(Response.text, "html.parser")
        
        # Scrape article titles
        Title  = [a.get_text() for a in Soup.find_all("a", class_="_HId")]
        Title += [a.get_text() for a in Soup.find_all("a", class_="_sQb")]
        for t in Title:
            Titles.append(t)
        
        # Scrape article links
        Link  = [a["href"] for a in Soup.find_all("a", class_="_HId")]
        Link += [a["href"] for a in Soup.find_all("a", class_="_sQb")]
        for l in Link:
            Links.append(l)
    
        # Look like a user scrolling through links
        time.sleep(random.randint(5, 15))
    
    return Titles, Links
    
Titles, Links = GoogleNews('Barack Obama', 3)

print Titles
print Links

# For extracting article text from the links 
# Needs some refinements: 
# 1. Some links give errors 
# 2. Text is abour 90% pure body
# 3. NLTK has trouble characterizing overall sentiment
'''
from newspaper import Article
for link in links[0]:
    A = Article(link)
    A.download()
    A.parse()
    Paragraphs = (A.text).split('\n')
    for P in Paragraphs:
        if len(P) > 100: #Minimize percentage of non-body text
            print P
    print
'''
