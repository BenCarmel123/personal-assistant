import datetime
from zoneinfo import ZoneInfo
from typing import List, Literal
from langchain_core.tools import tool
from config.calendar import calendar_service
from config.contacts import CONTACTS
from config.settings import TIMEZONE, PRIMARY_CALENDAR_ID

# Google Calendar palette slots: 3=Grape, 4=Flamingo, 5=Banana, 6=Tangerine,
# 9=Blueberry, 11=Tomato
CATEGORY_COLORS = {
    "workout": "3",
    "important": "11",
    "logistics": "5",
    "social": "4",
    "work": "9",
}
DEFAULT_COLOR = "6"  # Tangerine, for anything uncategorized


def _to_rfc3339(value) -> str:
    """Interprets a bare ISO string (or datetime) as local TIMEZONE time and
    formats it as RFC3339, which is what the Calendar list API requires.
    """
    dt = datetime.datetime.fromisoformat(value) if isinstance(value, str) else value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(TIMEZONE))
    return dt.isoformat()


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
    category: Literal["workout", "important", "logistics", "social", "work"] = None,
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
            work: regular work/office blocks (e.g. "עבודה")
            important: meetings, deadlines, anything non-negotiable or that
                cannot be moved (that isn't a regular work block)
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


@tool
def find_events(
    query: str = None,
    time_min: str = None,
    time_max: str = None,
) -> str:
    """Searches the user's Google Calendar for events, returning each match's
    ID so it can be passed to update_event or delete_event.

    Always call this before update_event or delete_event — you need the
    event's ID, which only this tool provides. If multiple events match,
    list them for the user to disambiguate rather than guessing.

    Args:
        query: Optional free-text search (matches title, description, location).
            Omit to list all events in the time range.
        time_min: Optional ISO datetime lower bound, e.g. 2026-04-25T00:00:00.
            Defaults to now if omitted.
        time_max: Optional ISO datetime upper bound. Omit for no upper bound
            (be sure to pass this for "today"/"this week"-type questions so
            you don't get back everything from now to the end of time).
    """
    params = {
        "calendarId": PRIMARY_CALENDAR_ID,
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": 20,
    }
    if query:
        params["q"] = query
    params["timeMin"] = _to_rfc3339(time_min) if time_min else _to_rfc3339(datetime.datetime.now())
    if time_max:
        params["timeMax"] = _to_rfc3339(time_max)

    try:
        events = calendar_service.events().list(**params).execute().get("items", [])
    except Exception as e:
        return f"Failed to search events: {str(e)}"

    if not events:
        return "No matching events found."

    lines = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        lines.append(f"- {event.get('summary', '(no title)')} | {start} | id={event['id']}")
    return "\n".join(lines)


@tool
def update_event(
    event_id: str,
    title: str = None,
    start_time: str = None,
    duration_minutes: int = None,
    category: Literal["workout", "important", "logistics", "social", "work"] = None,
    location: str = None,
    attendees: List[str] = None,
) -> str:
    """Updates an existing Google Calendar event. Call find_events first to
    get the event_id.

    Only pass the fields that should change; everything else is left as-is.
    To change the end time, pass start_time and/or duration_minutes together
    (the end time is always derived from start + duration).

    Args:
        event_id: The event's ID, from find_events.
        title: New title, if changing.
        start_time: New ISO format start datetime, if changing.
        duration_minutes: New duration in minutes, if changing. If start_time
            is given without this, the event's existing duration is kept.
        category: New category (see add_event for definitions), if changing.
        location: New location, if changing.
        attendees: New full list of attendee names or emails, if changing
            (replaces the existing attendee list, not merged with it).
    """
    try:
        event = calendar_service.events().get(calendarId=PRIMARY_CALENDAR_ID, eventId=event_id).execute()
    except Exception as e:
        return f"Failed to find event {event_id}: {str(e)}"

    if title:
        event["summary"] = title

    if start_time or duration_minutes:
        existing_start = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        existing_end = datetime.datetime.fromisoformat(event["end"]["dateTime"])
        existing_duration = existing_end - existing_start

        new_start = datetime.datetime.fromisoformat(start_time) if start_time else existing_start
        new_duration = datetime.timedelta(minutes=duration_minutes) if duration_minutes else existing_duration
        new_end = new_start + new_duration

        event["start"] = {"dateTime": new_start.isoformat(), "timeZone": TIMEZONE}
        event["end"] = {"dateTime": new_end.isoformat(), "timeZone": TIMEZONE}

    if category:
        event["colorId"] = CATEGORY_COLORS.get(category, DEFAULT_COLOR)

    if location:
        event["location"] = location

    if attendees:
        event["attendees"] = resolve_attendees(attendees)

    try:
        updated = calendar_service.events().update(
            calendarId=PRIMARY_CALENDAR_ID, eventId=event_id, body=event
        ).execute()
        return f"Event '{updated.get('summary')}' updated: {updated.get('htmlLink')}"
    except Exception as e:
        return f"Failed to update event: {str(e)}"


@tool
def delete_event(event_id: str) -> str:
    """Deletes an event from the user's Google Calendar. Call find_events
    first to get the event_id. If the user asked for this event to be
    deleted, delete it directly — do not ask for confirmation first.

    Args:
        event_id: The event's ID, from find_events.
    """
    try:
        calendar_service.events().delete(calendarId=PRIMARY_CALENDAR_ID, eventId=event_id).execute()
        return "Event deleted."
    except Exception as e:
        return f"Failed to delete event: {str(e)}"
