import httpx
import tempfile
import os
from app.config import settings


async def transcribe_audio_groq(file_path: str) -> str:
    """Send audio file to Groq whisper endpoint for transcription."""
    url = f"{settings.GROQ_BASE_URL}/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}"
    }

    # Use whisper-large-v3-turbo for best performance
    data = {
        "model": "whisper-large-v3-turbo",
        "response_format": "text"
    }

    # Open file and send to Groq
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            return response.text.strip()
