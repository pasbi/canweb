#!/usr/bin/env python3

import sys
import json
import sqlite3

inputfilename = sys.argv[1]
connection = sqlite3.connect(sys.argv[2])
cur = connection.cursor()


with open(inputfilename) as f:
  data = json.load(f)

cmd = "INSERT INTO api_song" + \
      " (pattern, midiCommand, label, spotifyTrackId, youtubeTrackId)" + \
      " VALUES (?, ?, ?, '', '');"
for item in data['items']:
  midiProgram = item["MidiProgram"]
  midiProgram['type'] = "NS2"
  midiProgram = json.dumps(midiProgram)
  cur.execute(cmd, (item["pattern"], midiProgram, item["name"]))

  print("inserted ", item['name'])
connection.commit();