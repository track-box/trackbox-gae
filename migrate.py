# -*- coding: utf-8 -*-
import csv
import json
import codecs

edit_ids = {}

with open('edit.csv') as f1:
    edit_reader = csv.reader(f1)
    header = next(edit_reader)

    for row in edit_reader:
        edit_ids[row[1]] = row[0]

with open('track.json') as f2:
    data = json.load(f2)

    for track in data['values']:
        track_id = track[0]
        track_data = track[1]

        if track_id == 'test' or track_data is None:
            continue

        edit_id = edit_ids[track_id]

        with codecs.open('track/' + track_id, 'w', 'utf-8') as f:
            json.dump(track_data, f, ensure_ascii=False)

        with codecs.open('edit/' + edit_id, 'w', 'utf-8') as f:
            json.dump(track_data, f, ensure_ascii=False)

