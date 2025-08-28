import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    # ChromaDB
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Groq API (OpenAI-compatible endpoint)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "whisper-large-v3")
    TTS_OUTPUT_DIR: str = os.getenv("TTS_OUTPUT_DIR", "tts_outputs")

    # Tavily API
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Search settings
    MAX_SEARCH_RESULTS: int = 10
    MAX_CONTENT_LENGTH: int = 8000


settings = Settings()
