import json
from pathlib import Path

DATA_DIR = Path("tournament_data")
STATE_FILE = DATA_DIR / "live_state.json"
TOURNEY_FILE = DATA_DIR / "active_tournament.json"
RESULTS_FILE = DATA_DIR / "results.json"


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ---------- LOADERS ----------

def get_live_state():
    return load_json(STATE_FILE)


def get_tournament():
    return load_json(TOURNEY_FILE)


def get_results():
    return load_json(RESULTS_FILE)


def save_results(data):
    save_json(RESULTS_FILE, data)


# ---------- RACE LOOKUP ----------

def get_current_race(ring: int):
    state = get_live_state()
    tourney = get_tournament()

    race_number = state["current_race_per_ring"][str(ring)]

    for race in tourney["races"]:
        if race["race"] == race_number:
            return race

    return None


# ---------- BREAKOUT LOGIC ----------

def check_breakout(team_name, division, time):
    if time == "NF":
        return False

    tourney = get_tournament()
    breakout_time = tourney["breakouts"][division]

    return float(time) < breakout_time


def register_breakout(team_name):
    results = get_results()

    if team_name not in results["teams"]:
        results["teams"][team_name] = {
            "breakouts": 0,
            "ineligible": False,
            "status": "NORMAL"
        }

    results["teams"][team_name]["breakouts"] += 1

    # NAFA rule: 2 breakouts = placement ineligible (1 day)
    if results["teams"][team_name]["breakouts"] >= 2:
        results["teams"][team_name]["ineligible"] = True

    save_results(results)