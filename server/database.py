import json
from pathlib import Path

DB_FILE = Path("db.json")

DEFAULT_DB = {
    "settings": {
        "mode": "setup",   # setup | running | finished
        "rings": 0
    },
    "dog_points": {str(i): 0 for i in range(1,7)},
    "heats": []
}

def load_db():
    if not DB_FILE.exists():
        save_db(DEFAULT_DB)
        return DEFAULT_DB
    return json.loads(DB_FILE.read_text())

def save_db(data):
    DB_FILE.write_text(json.dumps(data, indent=2))