import json

def load(plik: str):
    with open(plik, 'r') as f:
        return json.load(f)