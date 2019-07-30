import json

class JSONWriter:
    def __init__(self):
        print()

    def export(_json, _filename):
        f = open(_filename, 'w')
        json.dump(_json, f)