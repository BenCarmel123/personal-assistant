import datetime
from typing import List, Literal
from langchain_core.tools import tool
from config.calendar import calendar_service
from config.contacts import CONTACTS
from config.settings import TIMEZONE, PRIMARY_CALENDAR_ID

# Google Calendar palette slots: 3=Grape, 4=Flamingo, 5=Banana, 11=Tomato
CATEGORY_COLORS = {
    "workout": "3",
    "important": "11",
    "logistics": "5",
    "social": "4",
}
DEFAULT_COLOR = "9"  # Blueberry, for anything uncategorized


def resolve_attendees(attendees: List[str]) -> list[dict]:
    attendee_emails = []
    for name in attendees:
        name = name.strip()
        email = CONTACTS.get(name.lower(), name)
        attendee_emails.append({"email": email})
    return attendee_emails


@tool
def add_event(
    title: str,
    start_time: str,
    duration_minutes: int,
    category: Literal["workout", "important", "logistics", "social"] = None,
    location: str = None,
    attendees: List[str] = None,
) -> str:
    """Adds an event to the user's Google Calendar.

    Args:
        title: The event title
        start_time: ISO format datetime, e.g. 2026-04-25T14:00:00
        duration_minutes: Duration of the event in minutes
        category: Which kind of event this is, which sets its calendar color.
            workout: gym, running, training, sports, physio
            important: meetings, work commitments, deadlines, anything
                non-negotiable or that cannot be moved
            logistics: errands, appointments, admin, travel, deliveries,
                bureaucracy, anything functional
            social: time with friends or with Lihi, dates, dinners, parties
            Omit only if the event genuinely fits none of these.
        location: Optional event location
        attendees: Optional list of attendee names or emails.
            Known people can be given by first name, e.g. ["lihi", "busha"].
    """
    start = datetime.datetime.fromisoformat(start_time)
    end = start + datetime.timedelta(minutes=duration_minutes)

    event = {
        "summary": title,
        "start": {"dateTime": start.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end.isoformat(), "timeZone": TIMEZONE},
        "colorId": CATEGORY_COLORS.get(category, DEFAULT_COLOR),
    }

    if location:
        event["location"] = location

    if attendees:
        event["attendees"] = resolve_attendees(attendees)

    try:
        created = calendar_service.events().insert(calendarId=PRIMARY_CALENDAR_ID, body=event).execute()
        return f"Event '{title}' created: {created.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"
