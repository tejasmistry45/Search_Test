from gtts import gTTS
from pathlib import Path
import os

# Create TTS output directory
TTS_OUTPUT_DIR = "tts_outputs"
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)


def synthesize_speech(text: str, lang: str = "en", filename: str = "tts_output.mp3") -> str:
    """Convert text to speech using gTTS and save to file."""
    output_path = Path(TTS_OUTPUT_DIR) / filename

    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(str(output_path))

    return str(output_path)
