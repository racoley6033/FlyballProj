import csv
import io
import requests

SCHEDULE = []
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNYSb0GiEfW2j0dJPJB8nR8ccployPPsz3SpYuKkKM6jxZQKdWmnZ4hQtBATm1Q1ZaFfqfYQ6ifrgW/pub?gid=0&single=true&output=csv"

def load_schedule():
    global SCHEDULE
    SCHEDULE = []

    try:
        response = requests.get(GOOGLE_SHEET_URL, timeout=10)
        response.raise_for_status()

        decoded = response.content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded))

        for row in reader:
            SCHEDULE.append({
                "heat": int(row["heat"]),
                "division": row["division"],
                "lane1": row["lane1_team"],
                "lane2": row["lane2_team"],
            })

        print(f"Loaded {len(SCHEDULE)} heats from Google Sheets")

    except Exception as e:
        print("FAILED to load Google Sheet schedule:", e)

def get_schedule():
    return SCHEDULE