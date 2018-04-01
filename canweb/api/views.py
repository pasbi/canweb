from api.models import Song
from api.serializers import SongDetailSerializer, SongLabelSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import JsonResponse
from external.pattern import Pattern
from external import service_interface
import json
import base64
import json
import traceback

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongLabelSerializer

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    serializer_class = SongDetailSerializer

def searchPattern(request, service, query):
  search_results = service_interface.search(service, query)
  search_results = json.dumps(search_results)
  return HttpResponse(search_results)

def getPattern(request, service, query):
  url = base64.b64decode(query.encode('utf-8')).decode('utf-8')
  pattern = service_interface.getPattern(service, url)
  result = json.dumps({"pattern": pattern})
  return HttpResponse(result)

def transpose(request, d):
  response = HttpResponse()
  try:
    pattern = request.POST["pattern"]
  except Exception:
    traceback.print_exc();
    print(request.POST)
    return HttpResponseBadRequest()

  try:
    pattern = Pattern(pattern).toString(markup={}, transpose=d)
  except Exception:
    traceback.print_exc();
    return HttpResponseServerError()

  print(pattern)
  return JsonResponse({"pattern": pattern})
