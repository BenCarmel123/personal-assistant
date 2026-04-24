import datetime
from langchain_core.tools import tool
from config.calendar import calendar_service


@tool
def add_event(title: str, start_time: str, duration_minutes: int) -> str:
    """Adds an event to the user's Google Calendar.

    Args:
        title: The event title
        start_time: ISO format datetime, e.g. 2026-04-25T14:00:00
        duration_minutes: Duration of the event in minutes
    """
    start = datetime.datetime.fromisoformat(start_time)
    end = start + datetime.timedelta(minutes=duration_minutes)

    event = {
        "summary": title,
        "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
    }

    try:
        created = calendar_service.events().insert(calendarId="primary", body=event).execute()
        return f"Event '{title}' created: {created.get('htmlLink')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"
