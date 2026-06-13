import json
import os

# Path to the JSON file used for simple persistence
DATA_FILE = "data/storage.json"

def initialize_storage():
    # Ensure the storage directory and file exist before reading/writing.
    # If the file does not exist or is empty, create a basic structure.
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
        # If the file is corrupted or unreadable, return an empty structure.
        print("[Bold Red]Error reading database storage file. Initializing empty fallback.[/Bold Red]")
        return {"users": [], "projects": [], "tasks": []}

def save_data(data: dict):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        # If writing fails, print a simple error message so the user knows.
        print(f"Failed to write data file layout: {e}")