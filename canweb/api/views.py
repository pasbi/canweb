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
from external.get_pattern import search
import json

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongLabelSerializer

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    serializer_class = SongDetailSerializer

def searchPattern(request, service, query):
  search_results = search(service, query)
  search_results = json.dumps(search_results)
  return HttpResponse(search_results)