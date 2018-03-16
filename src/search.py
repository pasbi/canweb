#!/usr/bin/env python3

import sys
import search_ultimateguitar
import common
import json

if len(sys.argv) != 3:
	print("Expected two arguments: service and query. Got: " + str(sys.argv))
	sys.exit(1)
else:
	service = sys.argv[1]
	query = sys.argv[2]

if service == "ultimateguitar":
	status, data = search_ultimateguitar.search(query);
else:
	print(json.dumps({
		'status': 'fail',
		'data': "unexpected service: " + service
	}))

if (status == common.STATUS_REQUEST_SUCCESS):
	print(json.dumps({
		'status': 'success',
		'data': data
	}))
else:
	print(json.dumps({
		'status': 'fail',
		'data': status
	}))

