# Product Vision

## Goal
Save the user time by automating everyday tasks through natural interaction.

## Interface
Twilio WhatsApp channel — the user sends text or voice recordings, and the assistant reasons and activates the right tool automatically.

## Architecture
Single agent that routes to domain-specific tools based on the request. Tools are self-contained and added incrementally over time.

## Planned Tools
- **Email writer** — draft and send emails to a specified person
- **Recording summarizer** — transcribe and summarize voice recordings
- **Calendar event creator** — add events to Google Calendar

## Principles
- Every tool should save meaningful time compared to doing it manually
- The interaction model should feel natural — no commands, no forms, just tell it what you need
