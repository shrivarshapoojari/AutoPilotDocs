import json

def load_input(file_path="data/mock_input.json"):
    with open(file_path, "r") as f:
        return json.load(f)
