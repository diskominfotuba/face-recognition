import json
import numpy as np

DATABASE_FILE = "models/face_encoding.json"

def save_encoding(name, encoding):
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[name] = encoding.tolist()  # Simpan encoding dalam format list

    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file)

def load_encodings():
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
            return {name: np.array(encoding) for name, encoding in data.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
