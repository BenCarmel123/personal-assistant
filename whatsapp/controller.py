from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
from whatsapp.service import is_valid_twilio_request, build_reply

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp(request: Request):
    form = await request.form()

    if not is_valid_twilio_request(request, dict(form)):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    reply_twiml = build_reply(form.get("Body", ""))

    return Response(content=reply_twiml, media_type="application/xml")
