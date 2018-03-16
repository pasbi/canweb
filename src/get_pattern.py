#!/usr/bin/env python3

import sys
import get_pattern_ultimateguitar

if len(sys.argv) != 3:
	print("Expected two arguments: service and query. Got: " + str(sys.argv))
	sys.exit(1)
else:
	service = sys.argv[1]
	query = sys.argv[2]

if service == "ultimateguitar":
	status, data = get_pattern_ultimateguitar.getPattern(query);

