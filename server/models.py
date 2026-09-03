# server/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class HeatEvent(Base):
    __tablename__ = "heat_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True)  # prevents duplicates
    match_id = Column(Integer)
    lane = Column(String)  # left/right
    heat_number = Column(Integer)

    teamA_time = Column(String)  # store raw input ("12.34" or "NF")
    teamB_time = Column(String)

    source_tablet = Column(String)
    edited = Column(Boolean, default=False)