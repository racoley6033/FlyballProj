# server/events.py
from sqlalchemy.orm import Session
from models import HeatEvent

def record_heat_event(db: Session, data):

    existing = db.query(HeatEvent).filter_by(event_id=data["event_id"]).first()
    if existing:
        return "duplicate"

    event = HeatEvent(
        event_id=data["event_id"],
        match_id=data["match_id"],
        lane=data["lane"],
        heat_number=data["heat_number"],
        teamA_time=data["teamA_time"],
        teamB_time=data["teamB_time"],
        source_tablet=data["source_tablet"]
    )

    db.add(event)
    db.commit()

    return "accepted"