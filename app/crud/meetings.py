from sqlalchemy.orm import Session
import models, schemas
import webdriver


def fetch_meetings():
    """Fetch City Council meetings from City Clerk calendar RSS feed."""

    url = "https://chicago.legistar.com/Feed.ashx?M=Calendar&ID=13369895&GUID=d03e61f9-1d04-47cf-96d1-772746fcb39a&Mode=All&Title=Office+of+the+City+Clerk+-+Calendar+(All)"
    entries = webdriver.fetch_rss_entries(url, "meetings")
    meetings = map(map_meetings, entries)
    return list(meetings)


def map_meetings(entry):
    """Accepts an entry from the RSS calendar feed and returns a parsed dictionary: {type, date, time, link}."""

    meeting = split_meeting_title(entry.title)
    meeting["link"] = entry.link
    return meeting


def split_meeting_title(title):
    """Accepts a string, 'title', and splits it on each hyphen. Returns a dictionary with keys/values for the 'type', 'date', and 'time' extracted from 'title': {type, date, time}."""

    columns = ["type", "date", "time"]
    data = title.split(" - ")
    meeting = dict(zip(columns, data))
    return meeting


def create_meeting(meeting: schemas.CreateMeeting):
    """Create a new Meeting ORM object."""

    db_meeting = models.Meeting(
        type=meeting["type"],
        date=meeting["date"],
        time=meeting["time"],
        link=meeting["link"],
    )
    return db_meeting


def create_records(entries):
    """Create a list of new Meeting row objects for inserting to the database."""

    meetings = []
    for entry in entries:
        meeting = create_meeting(entry)
        meetings.append(meeting)
    return meetings


def get_all_meetings(db: Session):
    meetings = db.query(models.Meeting).all()
    return meetings


def get_meeting_links(db: Session):
    links_list = []
    links = db.query(models.Meeting.link).all()
    for link in links:
        links_list.append(link[0])
    return links_list
