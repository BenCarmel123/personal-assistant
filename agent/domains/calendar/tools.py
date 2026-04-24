import datetime
from typing import List
from langchain_core.tools import tool
from config.calendar import calendar_service
from config.contacts import CONTACTS


def resolve_attendees(attendees: str) -> list[dict]:
    attendee_emails = []
    for name in attendees.split(","):
        name = name.strip()
        email = CONTACTS.get(name, name)
        attendee_emails.append({"email": email})
    return attendee_emails


@tool
def add_event(
    title: str,
    start_time: str,
    duration_minutes: int,
    location: str = None,
    attendees: List[str] = None,
) -> str:
    """Adds an event to the user's Google Calendar.

    Args:
        title: The event title
        start_time: ISO format datetime, e.g. 2026-04-25T14:00:00
        duration_minutes: Duration of the event in minutes
        location: Optional event location
        attendees: Optional comma-separated list of attendee emails
    """
    start = datetime.datetime.fromisoformat(start_time)
    end = start + datetime.timedelta(minutes=duration_minutes)

    event = {
        "summary": title,
        "start": {"dateTime": start.isoformat(), "timeZone": "Asia/Jerusalem"},
        "end": {"dateTime": end.isoformat(), "timeZone": "Asia/Jerusalem"},
        "colorId": "9",
    }

    if location:
        event["location"] = location

    if attendees:
        event["attendees"] = resolve_attendees(attendees)

    try:
        created = calendar_service.events().insert(calendarId="primary", body=event).execute()
        return f"Event '{title}' created: {created.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"
