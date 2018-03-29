import sys
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import multiprocessing
import itertools
import common
import urllib.error

def search_page_n(query, page):
	common.debug("search_page")
	max_repetitions = 10
	for _ in range(max_repetitions):
		(status, items) = search_page(query, page)
		common.debug("search_page status:", status)
		if status == common.STATUS_REQUEST_SUCCESS:
			common.debug("success")
			return items
		elif status == common.STATUS_REQUEST_PARSE_ERROR:
			common.debug("parse error")
			return [] # the page is not parsable. Probably because the format is unexpected.
		elif status == common.STATUS_REQUEST_503:
			common.debug("503")
			continue # try again
		elif status == common.STATUS_REQUEST_404:
			common.debug("404")
			return [] # there is no such page. Don't try again.
		else:
			common.debug("Unexpedted fail-status: " + status)
			return []
	# After `max_repetitions` 503-errors, give up.
	return []

def getContent(page):
	soup = BeautifulSoup(page, 'lxml')
	scripts = soup.findAll('script');
	prefix = "window.UGAPP.store.page"

	scripts = list(map(lambda tag: tag.text.strip(), scripts))
	scripts = list(filter(lambda script: script.startswith(prefix), scripts))
	if len(scripts) != 1:
		return None
	else:
		jsonData = scripts[0][len(prefix):].strip()[1:].strip()[:-1]
		data = json.loads(jsonData)
		return data['data']

def search_page(query, page):
	# print("search")
	common.debug("search_page", query, page)
	url = "https://www.ultimate-guitar.com/search.php?search_type=title&value={:s}&page={:d}"
	url = url.format(urllib.parse.quote_plus(query), page)
	try:
		page = common.loadPage(url)
	except urllib.error.HTTPError as e:
		return (str(e), None)

	content = getContent(page)
	if content == None:
		return (common.STATUS_REQUEST_PARSE_ERROR, None)
	else:
		content = content['results']
	items = []
	for datum in content:
		try:
			if datum['type'] == 'Chords':
				items.append({
					"song_name": datum['song_name'],
					"artist_name": datum['artist_name'],
					"rating": datum['rating'],
					"url": datum['tab_url'],
				})
		except KeyError:
			# we are not interested in special items that dont't contain the keys above.
			pass
	return (common.STATUS_REQUEST_SUCCESS, items)

def search(query):
	common.debug("search for ", query)
	n = 10
	args = zip([query] * n, range(1, n+1))
	with multiprocessing.Pool(n) as pool:
		items = pool.starmap(search_page_n, args)
	items = list(itertools.chain(*items))
	return (common.STATUS_REQUEST_SUCCESS, items)


def getPattern(query):
	page = common.loadPage(query)
	try:
		content = getContent(page)['tab_view']['wiki_tab']['content']
	except KeyError:
		return (common.STATUS_REQUEST_PARSE_ERROR, None)

	content = content.replace('[ch]', '').replace('[/ch]', '')
	return (common.STATUS_REQUEST_SUCCESS, content)

