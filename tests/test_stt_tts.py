import asyncio
from app.services.stt import transcribe_audio_groq
from app.services.tts import synthesize_speech

async def main():
    audio_file = input("Enter path to WAV audio file: ").strip()
    print("Transcribing with Groq whisper...")
    transcript = await transcribe_audio_groq(audio_file)
    print("\nTranscript:")
    print(transcript)

    print("\nSynthesizing speech from transcript...")
    tts_file = synthesize_speech(transcript, filename="reply.mp3")
    print(f"Generated TTS file at: {tts_file}")

if __name__ == "__main__":
    asyncio.run(main())
