import json


def save_data(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
