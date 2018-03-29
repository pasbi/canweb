#!/usr/bin/env python3

import sys
import common
import json
import importlib

def fail(data):		
	print(json.dumps({
		'status': 'fail',
		'data': data
	}))
	sys.exit(0)

def success(data):		
	print(json.dumps({
		'status': "success",
		'data': data
	}))
	sys.exit(0)



if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Expected 3 args: service command query. Got: " + str(sys.argv))
		sys.exit(1)
	else:
		service = sys.argv[1]
		command = sys.argv[2]
		query = sys.argv[3]

	try:
		service = importlib.import_module(service)
	except Exception as e:
		print(e)
		fail("unexpected service: " + service)

	if command == "search":
		if len(query) == 0:
			status = "empty"
		else:
			status, data = service.search(query)
	elif command == "get":
		status, data = service.getPattern(query)
	else:
		fail("unexpected command: " + command)

	if status == common.STATUS_REQUEST_SUCCESS:
		success(data)
	else:
		fail(status)