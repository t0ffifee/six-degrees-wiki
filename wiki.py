from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

BASE = 'https://en.wikipedia.org/wiki/'
START = 'https://en.wikipedia.org/wiki/Kevin_Bacon'
END = 'https://en.wikipedia.org/wiki/Sleepers'
MAX_DEPTH = 10
LINKS = 20

def get_hrefs(url):
    html = urlopen(url)
    # bs = BeautifulSoup(html, 'html.parser')
    bs = BeautifulSoup(html, 'lxml')
    article = bs.find(id='mw-content-text')
    links = article.find_all('a', href=True)
    hrefs = [link['href'] for link in links]
    return hrefs

def get_articles(hrefs):
    # have to remove the disambigation articles and List_of articles as well
    link_re = re.compile('/wiki/(?!Wikipedia:|File:|Template(_talk)?:|Help:|Special:|Category:|List_of).+$')
    articles = [h[6:] for h in hrefs if link_re.match(h)]
    return articles[:LINKS]

"""
{
    'article': [article, article, artcicle],
    'article': [article, article, artcicle],
    'article': [article, article, artcicle]
}
"""

# set up
queue = [[START[30:]]]
database = {}
path = []
goal = END[30:]

while queue:
    path = queue.pop(0)
    print(path)
    article = path[-1]
    if article == goal:
        break

    # getting articles in article
    if article in database:
        articles = database[article] # this must be done with try except
    else:
        url = BASE + article
        hrefs = get_hrefs(url)
        articles = get_articles(hrefs)
        database[article] = articles
    
    for article in articles:
        new_path = list(path)
        if article not in path:
            new_path.append(article)
            if len(new_path) != MAX_DEPTH:
                queue.append(new_path)
        

print(path)
