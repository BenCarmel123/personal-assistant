import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from agent.assistant import run
from config.settings import DEFAULT_SERVER_PORT

load_dotenv()

app = FastAPI()


@app.post("/whatsapp")
async def whatsapp(Body: str = Form(...), From: str = Form(...)):
    reply_text = run(Body)

    twiml = MessagingResponse()
    twiml.message(reply_text)

    return Response(content=str(twiml), media_type="application/xml")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", DEFAULT_SERVER_PORT))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
