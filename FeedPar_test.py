import feedparser
import re
import os
import time 


def parseRSS( rss_url ):
    d = feedparser.parse( rss_url )
    return d
def getHeadlines( rss_url ):
    headlines = []
    
    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
	headlines.append("###############")
	headlines.append(newsitem['id'])
        headlines.append(newsitem['published'])
        headlines.append(newsitem['title'])
	newsitem['description'] = re.sub('<.*?>',' ', newsitem['description'])
	headlines.append(newsitem['description'])
 
        
    return headlines
    
allheadlines = []

newsurls = {
	#UK Sources
    'bbc':'http://feeds.bbci.co.uk/news/politics/rss.xml',
    'guardian':'https://www.theguardian.com/politics/rss',

	#US Sources
    'ABC':'http://feeds.abcnews.com/abcnews/politicsheadlines',
    'CBS':'http://www.cbsnews.com/latest/rss/politics',
    'CBS':'http://www.nbcnewyork.com/news/politics/?rss=y',
    'AP':'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa',

}
for key,url in newsurls.items():
    allheadlines.extend( getHeadlines( url ) )

f = open('NewsData/NewsList.txt', 'w')

for hl in allheadlines:
    f.write(hl.encode("utf-8") + '\n')
f.close()

