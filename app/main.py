from crud import meetings, members, legislation
from database import engine, SessionLocal, reset_table
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Start a new connection to the PostgreSQL database, and close the connection when no longer in use."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/meetings/")
def get_meetings(db: Session = Depends(get_db)):
    """Fetch all meetings from the database."""

    meetings_from_db = meetings.get_all_meetings(db)
    return meetings_from_db


@app.get("/meetings/links")
def get_meeting_links(db: Session = Depends(get_db)):
    """Fetch the links for each meeting. Used for extracting legislation from each meeting."""

    meetings.get_meeting_links(db)


@app.post("/meetings/")
def post_meetings_to_db(db: Session = Depends(get_db)):
    """Fetch City Council meetings from City Clerk's RSS feed and add meetings to database."""

    meeting_entries = meetings.fetch_meetings()
    meeting_records = meetings.create_records(meeting_entries)
    db.query(models.Meeting).delete()
    reset_table("meetings")
    db.add_all(meeting_records)
    db.commit()
    return {"msg": "City Council meetings added to database."}


@app.post("/members/")
def post_members_to_db(db: Session = Depends(get_db)):
    """Fetch City Council members from City Clerk's site and add members to database."""

    member_entries = members.fetch_members()
    member_records = members.create_records(member_entries)
    db.query(models.Member).delete()
    reset_table("members")
    db.add_all(member_records)
    db.commit()
    return {"msg": "City Council members added to database."}


@app.post("/legislation/")
def post_legislation_to_db(db: Session = Depends(get_db)):

    legislation_entries = legislation.fetch_legislation(db)
    legislation_records = legislation.create_records(legislation_entries)
    db.query(models.Legislation).delete()
    reset_table("legislation")
    db.add_all(legislation_records)
    db.commit()
    return {"msg": "City Council legislation added to database."}
