import os
from dotenv import load_dotenv
from fastapi import FastAPI
from mangum import Mangum
from whatsapp.controller import router as whatsapp_router
from config.settings import DEFAULT_SERVER_PORT

load_dotenv()

app = FastAPI()
app.include_router(whatsapp_router)


# Entry point AWS Lambda invokes; translates the Lambda event into an ASGI
# request against the FastAPI app above, and the response back into Lambda's
# expected shape. Irrelevant when running locally via `python server.py`.
handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", DEFAULT_SERVER_PORT))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
