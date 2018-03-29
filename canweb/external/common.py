#!/usr/bin/env python3

import sys
import json
import urllib.request

if __name__ == "__main__":
	print("This lib is not meant to be run.")
	sys.exit(1)


def debug(*args):
	pass
	# print(*args)

def loadPage(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
	}
	r = urllib.request.Request(url, headers=headers)
	page = urllib.request.urlopen(r).read()
	return page.decode('utf-8')

STATUS_REQUEST_SUCCESS = 'success'
STATUS_REQUEST_PARSE_ERROR = 'parse error'
STATUS_REQUEST_404 = 'HTTP Error 404: Not Found'
STATUS_REQUEST_503 = 'HTTP Error 503: Service Unavailable'