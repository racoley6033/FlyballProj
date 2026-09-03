from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import asyncio

from server.realtime import manager
from server.schedule_loader import load_schedule, get_schedule
from server.tournament import get_current_race, check_breakout, register_breakout

app = FastAPI()

# --------------------------
# Static iPad UI
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def ipad_screen():
    return FileResponse(STATIC_DIR / "ipad.html")


# --------------------------
# Startup events
# --------------------------
@app.on_event("startup")
async def startup_load_schedule():
    print("Loading schedule...")
    load_schedule()

@app.on_event("startup")
async def auto_refresh_schedule():
    async def refresh_loop():
        while True:
            load_schedule()
            await asyncio.sleep(20)  # auto refresh from Google Sheets
    asyncio.create_task(refresh_loop())


# --------------------------
# API — Current Race
# --------------------------
@app.get("/api/current_race")
def current_race():
    race = get_current_race(get_schedule())
    if not race:
        return {"status": "waiting"}
    return race


# --------------------------
# API — Submit Heat Result
# --------------------------
@app.post("/api/submit_heat")
async def submit_heat(data: dict):
    """
    Expected:
    {
        heat: 1,
        lane: 1 or 2,
        time: 21.345 OR null,
        result: "W" | "L" | "T" | "NF"
    }
    """

    breakout = False
    if data.get("time") is not None:
        breakout = check_breakout(data["heat"], data["lane"], data["time"])
        if breakout:
            register_breakout(data["heat"], data["lane"])

    # broadcast update to tablets
    await manager.broadcast({
        "type": "heat_update",
        "data": data,
        "breakout": breakout
    })

    return {"ok": True, "breakout": breakout}


# --------------------------
# WebSocket — Live Tablets
# --------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)