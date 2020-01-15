import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Generate archive page URL from year and month
def genURL(y, m):
	y = str(y)
	m = str(m)
	if(len(m) == 1):
		m = "0"+m
	return "https://digiteye.in/"+y+"/"+m+"/"

# Fetch relevant information about story via the article URL
def fetchArticle(url):
	html = requests.get(url).content
	article = dict()
	soup = BeautifulSoup(html, 'html5lib')
	articleDiv = soup.find('article')
	article['title'] = soup.find('span', attrs = {'itemprop':'name'}).text
	article['date'] = soup.find('span', attrs = {'class':'tie-date'}).text
	article['author'] = dict()
	article['author']['name'] = soup.find('span', attrs = {'class':'post-meta-author'}).find('a').text
	article['author']['link'] = soup.find('span', attrs = {'class':'post-meta-author'}).find('a')['href']
	article['domain'] = 'digiteye.in'
	article['url'] = url
	article['photos'] = []
	article['lang'] = 'english'
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
	for row in soup.findAll('a', attrs = {'class':'more-link'}): 
	    url = row['href']
	    article = fetchArticle(url)
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

file = open('posts.json', 'w+')
file.write(json.dumps(data))
file.close()