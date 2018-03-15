import sys
import urllib.request
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import multiprocessing
import itertools


headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

def error(message):
	print(json.dumps({
		"status": "error",
		"message": message
		}))

def debug(*args):
	pass
	# print(*args)

def label(obj):
	return "{:s}—{:s}".format(obj['song_name'], obj['artist_name'])

STATE_REQUEST_SUCCESS = 'success'
STATE_REQUEST_404 = 'HTTP Error 404: Not Found'
STATE_REQUEST_503 = 'HTTP Error 503: Service Unavailable'

def search_page_n(query, page):
	debug("search_page")
	max_repetitions = 10
	for _ in range(max_repetitions):
		(status, items) = search_page(query, page)
		debug("search_page status:", status)
		if status == STATE_REQUEST_SUCCESS:
			debug("success")
			return items
		elif status == STATE_REQUEST_503:
			debug("503")
			continue # try again
		elif status == STATE_REQUEST_404:
			debug("404")
			return [] # there is no such page. Don't try again.
	# After max_repetitions 503-errors, give up.
	return []

def search_page(query, page):
	debug("search_page", query, page)
	url = "https://www.ultimate-guitar.com/search.php?search_type=title&value={:s}&page={:d}"
	url = url.format(urllib.parse.quote_plus(query), page)
	r = urllib.request.Request(url, headers=headers)
	try:
		page = urllib.request.urlopen(r).read()
	except urllib.error.HTTPError as e:
		return (str(e), [])

	soup = BeautifulSoup(page, 'lxml')
	scripts = soup.findAll('script');

	prefix = "window.UGAPP.store.page"
	scripts = map(lambda tag: tag.text.strip(), scripts)
	scripts = list(filter(lambda script: script.startswith(prefix), scripts))
	if len(scripts) != 1:
		error("Cannot get results: " + len(scripts))
	json_data = scripts[0][len(prefix):].strip()[1:].strip()[:-1]
	data = json.loads(json_data)
	data = data['data']['results']
	items = []
	for datum in data:
		try:
			if datum['type'] == 'Chords':
				items.append({
					"song_name": datum['song_name'],
					"artist_name": datum['artist_name'],
					"rating": datum['rating'],
					"url": datum['tab_url'],
				})
		except KeyError:
			pass	# we are not interested in special items that dont't contain the keys above.
	return ('success', items)

def search(query):
	debug("search for ", query)
	n = 10
	args = zip([query] * n, range(1, n+1))
	with multiprocessing.Pool(n) as pool:
		items = pool.starmap(search_page_n, args)
	items = list(itertools.chain(*items))
	print(json.dumps({
		"status": "success",
		"results": items
		}))