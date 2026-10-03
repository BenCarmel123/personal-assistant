import os
from fastapi import Request
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from agent.assistant import handle_message

validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])


def is_valid_twilio_request(request: Request, form: dict) -> bool:
    signature = request.headers.get("X-Twilio-Signature", "")

    # Twilio signs the exact URL it called. Lambda Function URLs always
    # terminate HTTPS at the edge, so we trust the forwarded proto/host
    # rather than request.url, which Mangum may report as http internally.
    proto = request.headers.get("x-forwarded-proto", "https")
    host = request.headers.get("x-forwarded-host", request.url.hostname)
    url = f"{proto}://{host}{request.url.path}"

    return validator.validate(url, form, signature)


def build_reply(body: str) -> str:
    reply_text = handle_message(body)

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml)
