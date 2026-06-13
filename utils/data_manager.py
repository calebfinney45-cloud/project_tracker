import json
import os

DATA_FILE = "data/storage.json"

def initialize_storage():
    # Ensures directories and data files exist safely.
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, "w") as f:
            json.dump({"users": [], "projects": [], "tasks": []}, f, indent=4)

def load_data() -> dict:
    initialize_storage()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("[Bold Red]Error reading database storage file. Initializing empty fallback.[/Bold Red]")
        return {"users": [], "projects": [], "tasks": []}

def save_data(data: dict):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Failed to write data file layout: {e}")