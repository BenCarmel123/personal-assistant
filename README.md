# Personal Assistant

A conversational AI agent that automates everyday tasks through WhatsApp. Send natural language requests via Twilio WhatsApp, and the assistant reasons about what you need and activates the appropriate tool.

## Current Status

### Implemented
- **Calendar integration** — Create Google Calendar events with natural language. Supports attendee resolution from a contacts book, including Hebrew name aliases.
- **OpenAI backend** — GPT-4o-mini for reasoning and tool orchestration

### In Progress
- **WhatsApp/Twilio integration** — Channel for natural conversational interaction

### Planned
- **Email writer** — Draft and send emails to specified recipients
- **Recording summarizer** — Transcribe and summarize voice recordings

## Architecture

Single agent that routes to domain-specific tools based on the request. Tools are self-contained and added incrementally.

```
User Message (WhatsApp)
    ↓
Agent (OpenAI)
    ↓
Tool Router → Calendar | Email | Recording Summarizer
    ↓
User Response
```

## Setup

1. Clone the repo and create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_key_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_ACCOUNT_SID=your_sid_here
```

4. Set up Google Calendar OAuth:
- Create a Google Cloud project and enable the Calendar API
- Download credentials as `credentials.json`
- Run the app once to complete OAuth flow (generates `token.json`)

5. Create a `contacts.json` file with your contacts (not committed to repo):
```json
{
  "Name": "email@example.com",
  "שם": "email@example.com"
}
```

## Design Principles

- Every tool should save meaningful time compared to doing it manually
- The interaction model should feel natural — no commands, no forms, just tell it what you need
- Support multiple languages (currently English and Hebrew)
