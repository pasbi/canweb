from django.shortcuts import render
from django.http import HttpResponse
from external.format_pattern import Pattern
from api.models import Song

def create_song(request):
  return HttpResponse("create song ...")

def edit_song(request, pk):
  song = Song.objects.get(pk=pk)
  context = {
    "pk": pk,
    "pattern": song.pattern,
    "songLabel": song.label,
    "menuitems": [
      { "label": "Submit", "id": "mi-submit" },
      { "label": "Cancel", "id": "mi-cancel" }
    ]
  }
  return render(request, 'view/song_edit.html', context=context)

def view_song(request, pk):
  song = Song.objects.get(pk=pk)
  pattern = Pattern(song.pattern)
  pattern.linebreak = "<br>"
  pattern.start_tag = "<b>"
  pattern.end_tag = "</b>"
  context = {
    "pk": pk,
    "formattedPattern": pattern.toString(),
    "songLabel": song.label,
    "menuitems": [
      { "label": "Edit", "id": "mi-edit" }
    ]
  }
  return render(request, 'view/song_view.html', context=context)

def view_song_list(request):
    return render(request, 'view/song_list_view.html')
