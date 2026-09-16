from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import GEMINI_API_KEY


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY,
)