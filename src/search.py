#!/usr/bin/env python3

import sys
import search_ultimateguitar

if len(sys.argv) != 3:
	print("Expected two arguments: service and query. Got: " + str(sys.argv))
	sys.exit(0)
else:
	service = sys.argv[1]
	query = sys.argv[2]

if service == "ultimateguitar":
	search_ultimateguitar.search(query);

