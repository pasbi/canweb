#!/usr/bin/env python3

import importlib
from external import common

def search(service, query):
  service = importlib.import_module('external.' + service)
  return service.search(query)

def getPattern(service, query):
  service = importlib.import_module('external.' + service)
  return service.getPattern(query)