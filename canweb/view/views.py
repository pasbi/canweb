from django.shortcuts import render
from django.http import HttpResponse
from external.pattern import Pattern
from api.models import Song

def edit_song(request, pk):
  song = Song.objects.get(pk=pk)
  context = {
    "pk": pk,
    "pattern": song.pattern,
    "songLabel": song.label,
    "menuitems": [
      { "label": "Submit", "id": "mi-submit" },
      { "label": "Cancel", "id": "mi-cancel" },
      { "label": "Search Pattern", "id": "mi-searchpattern" },
      { "label": "Remove", "id": "mi-remove" },
      { "label": "Transpose up", "id": "mi-trup" },
      { "label": "Transpose down", "id": "mi-trdown" }
    ]
  }
  return render(request, 'view/song_edit.html', context=context)

def view_song(request, pk):
  song = Song.objects.get(pk=pk)
  pattern = Pattern(song.pattern)
  markup = {}
  markup["chord/prefix"] = "<span class='chord'>"
  markup["chord/postfix"] = "</span class='chord'>"
  markup["headline/prefix"] = "<span class='headline'>"
  markup["headline/postfix"] = "</span class='headline'>"
  markup["chordline/prefix"] = "<span class='chordline'>"
  markup["chordline/postfix"] = "</span class='chordline'>"
  markup["chordline/linebreak"] = ""    # style='display: block'
  markup["headline/linebreak"] = ""     # style='display: block'
  markup["default/linebreak"] = "\n"
  context = {
    "pk": pk,
    "formattedPattern": pattern.toString(markup=markup, transpose=0),
    "songLabel": song.label,
    "menuitems": [
      { "label": "Edit", "id": "mi-edit" }
    ]
  }
  return render(request, 'view/song_view.html', context=context)

def view_song_list(request):
    context = {
      "menuitems": [
        { "label": "Create", "id": "mi-create" }
      ]
    }
    return render(request, 'view/song_list_view.html', context=context)
