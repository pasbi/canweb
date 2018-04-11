from django.shortcuts import render
from django.http import HttpResponse
from external.pattern import Pattern
from api.models import Song
import json

def sanitizeMidiCommand(midiCommand):
  if type(midiCommand) != str:
    print("ERROR: Expected <string> but got <" + type(midiCommand) + ">")
    midiCommand = ""
  elif midiCommand == "":
    return "{}"
  else:
    try:
      json.loads(midiCommand)
    except json.decoder.JSONDecodeError:
      print("ERROR: Midi command is not valid json.")
      return "{}"
  return midiCommand
  

def edit_song(request, pk):
  song = Song.objects.get(pk=pk)

  # verify midi command sanity
  midiCommand = sanitizeMidiCommand(song.midiCommand)
  if (midiCommand != song.midiCommand):
    print("WARNING: Midi command is not sane: '" + song.midiCommand + "'")

  context = {
    "pk": pk,
    "pattern": song.pattern,
    "songLabel": song.label,
    "songProgram": midiCommand,
    "justCreated": "true" if song.label == "" and song.pattern == "" else "false",
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
    "songLabel": song.label
  }
  return render(request, 'view/song_view.html', context=context)

def view_song_list(request):
    context = {
      "searchField": True
    }
    return render(request, 'view/song_list_view.html', context=context)
