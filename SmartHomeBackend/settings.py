import json


def load_settings(filePath='settings_PI1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
