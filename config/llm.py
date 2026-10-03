import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_MODEL

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=os.environ["GEMINI_API_KEY"],
)
