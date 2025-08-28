import sys
import os

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio
import tempfile
import wave
import pyaudio
from pathlib import Path
from app.services.stt import transcribe_audio_groq
from app.services.tts import synthesize_speech

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5


async def main():
    print("🎤 Voice STT → TTS Demo")
    print("=" * 40)
    print(f"🔊 Recording {RECORD_SECONDS} seconds of audio...")
    print("Start speaking now...")

    # Record audio
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio_interface.terminate()
    print("✅ Recording complete!")

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    with wave.open(temp_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    try:
        # Transcribe with Groq
        print("🤖 Transcribing with Groq Whisper...")
        transcript = await transcribe_audio_groq(temp_path)
        print(f"📝 Transcript: '{transcript}'")

        if not transcript:
            transcript = "Sorry, I didn't catch that."

        # Generate TTS response
        print("🔄 Generating speech...")
        output_file = synthesize_speech(transcript, filename="voice_reply.mp3")
        print(f"🎵 TTS saved to: {output_file}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        os.unlink(temp_path)


if __name__ == "__main__":
    asyncio.run(main())
