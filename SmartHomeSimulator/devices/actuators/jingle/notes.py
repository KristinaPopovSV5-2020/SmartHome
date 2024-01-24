import json

notes = {}
with open('notes.json', 'r') as f:
    notes = json.load(f)


def load_song(filePath):
    song = {}
    with open(filePath, 'r') as f:
        song = json.load(f)

    return song
