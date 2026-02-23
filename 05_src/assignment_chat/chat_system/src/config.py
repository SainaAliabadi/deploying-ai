import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))

    # Chroma persistence
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "chat_system/chroma_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "knowledge_base")

    # App
    APP_TITLE: str = os.getenv("APP_TITLE", "Tri-Service Chat Buddy")

settings = Settings()
