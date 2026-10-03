# Personal Assistant

A conversational AI agent that automates everyday tasks through WhatsApp. Send natural language requests via Twilio WhatsApp, and the assistant reasons about what you need and activates the appropriate tool.

## Current Status

### Implemented
- **Calendar integration** — Create Google Calendar events with natural language. Supports attendee resolution from a contacts book (including Hebrew name aliases) and automatic color-coding by category (workout, important, logistics, social).
- **Gemini backend** — Gemini 3.8 Flash for reasoning and tool orchestration, via `langchain` 1.x's `create_agent`
- **WhatsApp/Twilio integration** — FastAPI webhook (`server.py`) receives inbound WhatsApp messages via Twilio and replies with the agent's response. Verified working end-to-end locally (tunneled through ngrok to Twilio's WhatsApp Sandbox).

### Planned
- **Cloud deployment** — Move off local + ngrok onto a proper serverless deployment (targeting AWS Lambda via a container image on ECR) so the webhook has a stable, always-on URL
- **Email writer** — Draft and send emails to specified recipients
- **Recording summarizer** — Transcribe and summarize voice recordings

## Architecture

Single agent that routes to domain-specific tools based on the request. Tools are self-contained and added incrementally.

```
User Message (WhatsApp)
    ↓
Twilio → FastAPI webhook (server.py)
    ↓
Agent (Gemini)
    ↓
Tool Router → Calendar | Email | Recording Summarizer
    ↓
User Response (TwiML)
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
GEMINI_API_KEY=your_key_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_ACCOUNT_SID=your_sid_here
GOOGLE_CLIENT_ID=your_oauth_client_id
GOOGLE_CLIENT_SECRET=your_oauth_client_secret
PORT=8000
```

4. Set up Google Calendar OAuth:
- Create a Google Cloud project, enable the Calendar API, and create an OAuth client (Desktop app type)
- Put its client ID/secret in `.env` as above (no `credentials.json` file needed — `config/calendar.py` builds the client config from env vars)
- Run the app once to complete the OAuth flow in your browser (generates `token.json`, which is gitignored)
- Publish the OAuth consent screen (Google Cloud Console → OAuth consent screen → Publish app) so the refresh token doesn't expire after 7 days

5. Create a `contacts.json` file with your contacts (not committed to repo):
```json
{
  "name": "email@example.com",
  "שם": "email@example.com"
}
```

6. Run the server locally:
```bash
python server.py
```

7. Expose it publicly for Twilio with ngrok:
```bash
ngrok http 8000
```
Then set that ngrok URL + `/whatsapp` as the "when a message comes in" webhook in the Twilio WhatsApp Sandbox settings (method POST).

## Design Principles

- Every tool should save meaningful time compared to doing it manually
- The interaction model should feel natural — no commands, no forms, just tell it what you need
- Support multiple languages (currently English and Hebrew)
