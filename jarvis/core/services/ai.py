import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

SYSTEM_INSTRUCTION = (
    "You are Jarvis, a helpful beginner AI assistant. "
    "Give short, clear, useful answers."
)


def get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def ask_ai(question: str) -> str:
    question = (question or "").strip()
    if not question:
        return "Please ask something first."

    client = get_client()
    if client is None:
        return "GEMINI_API_KEY is not set. Add it to your .env file."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.4,
                max_output_tokens=300,
            ),
        )
        text = getattr(response, "text", None)
        return text.strip() if text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Sorry, I could not get an AI response: {e}"