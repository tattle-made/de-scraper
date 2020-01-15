import requests
from bs4 import BeautifulSoup
import json

# Generate archive page URL from year and month
def genURL(y, m):
	y = str(y)
	m = str(m)
	if(len(m) == 1):
		m = "0"+m
	return "https://digiteye.in/kannada/"+y+"/"+m+"/"

# Fetch relevant information about story via the article URL
def fetchArticle(url):
	html = requests.get(url).content
	article = dict()
	soup = BeautifulSoup(html, 'html5lib')
	articleDiv = soup.find('article')
	article['title'] = soup.find('span', attrs = {'itemprop':'name'}).text
	#article['date'] = soup.find('span', attrs = {'class':'tie-date'}).text
	article['author'] = dict()
	article['author']['name'] = soup.find('section', attrs = {'id':'author-box'}).find('div', attrs={'class':'block-head'}).text
	article['domain'] = 'digiteye.in'
	article['url'] = url
	article['lang'] = 'kannada'
	article['photos'] = []
	for row in articleDiv.findAll('img'):
		article['photos'].append(row['src'])

	article['text'] = []

	firstP = True
	for row in articleDiv.findAll('p'):
		# Skip first <p>, as it contains meta-data
		if firstP == True:
			firstP = False
			continue
		article['text'].append(row.text)

	return article;

# Fetch relevant information about stories via the archive URL
def fetchArticles(url):
	html = requests.get(url).content
	soup = BeautifulSoup(html, 'html5lib') 
	articles = []
	for row in soup.findAll('article', attrs = {'class':'item-list'}): 
	    url = row.find('a', attrs= {'class':'more-link'})['href']
	    article = fetchArticle(url)
	    article['date'] = soup.find('span', attrs={'class':'tie-date'}).text
	    articles.append(article);
	return articles

# Stores scraped information
data = []

for year in range(datetime.now().year, 2016, -1):
	for month in range(12, 0, -1):
		url = genURL(year, month)
		articles = fetchArticles(url)
		data = data+articles
		print(str(len(articles))+" article(s) from "+str(year)+"/"+str(month)+" fetched.")

file = open('outputKa.json', 'w+')
file.write(json.dumps(data))
file.close()
