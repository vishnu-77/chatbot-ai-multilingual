import os
from groq import Groq

try:
    from langdetect import detect, DetectorFactory, LangDetectException
    DetectorFactory.seed = 0
except Exception:
    detect = None
    LangDetectException = Exception


def _map_lang_code_to_name(code: str) -> str:
    """Map short language codes returned by langdetect to the UI language names."""
    if not code:
        return "English"

    code = code.lower()
    if code.startswith("en"):
        return "English"
    if code.startswith("es"):
        return "Spanish"
    if code.startswith("fr"):
        return "French"
    if code.startswith("de"):
        return "German"
    if code.startswith("hi"):
        return "Hindi"
    if code.startswith("ja"):
        return "Japanese"
    if code.startswith("zh"):
        return "Chinese"
    if code.startswith("ar"):
        return "Arabic"

    return "English"


class MultilingualChatbot:
    def __init__(self):
        # First try the environment variable
        api_key = os.getenv("GROQ_API_KEY")

        # If not set, and we're running inside Streamlit, try streamlit secrets
        if not api_key:
            try:
                import streamlit as _st
                api_key = _st.secrets.get("GROQ_API_KEY")
            except Exception:
                api_key = None

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Set GROQ_API_KEY as an environment variable or add it to Streamlit Secrets."
            )

        self.client = Groq(api_key=api_key)

    @staticmethod
    def detect_language(text: str) -> str:
        """Detect language using langdetect and return a UI-friendly name.

        Falls back to English if detection fails or text is empty. Raises a
        RuntimeError if langdetect is not installed.
        """
        if not text or not text.strip():
            return "English"

        if detect is None:
            raise RuntimeError("langdetect is not installed. Install it with `pip install langdetect`.")

        try:
            code = detect(text)
        except LangDetectException:
            return "English"

        return _map_lang_code_to_name(code)

    def chat(self, message, language="English", history=None):
        # Make history default to an empty list when not provided
        if history is None:
            history = []

        # Add system message for language
        messages = [
            {"role": "system", "content": f"Reply in {language}"}
        ]

        # Add chat history and current message
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        # Get response from Groq
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content
