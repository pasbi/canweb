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
import external.get_pattern
import json
import base64

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongLabelSerializer

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    serializer_class = SongDetailSerializer

def searchPattern(request, service, query):
  search_results = external.get_pattern.search(service, query)
  search_results = json.dumps(search_results)
  return HttpResponse(search_results)

def getPattern(request, service, query):
  url = base64.b64decode(query.encode('utf-8')).decode('utf-8')
  pattern = external.get_pattern.getPattern(service, url)
  result = json.dumps({"pattern": pattern})
  return HttpResponse(result)
