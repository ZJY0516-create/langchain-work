from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    deepseek_api_key: str
    deepseek_model: str = "deepseek-chat"
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    max_tokens: int = 4096
    temperature: float = 0.3
    
    class Config:
        env_file = ".env"

settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
SUMMARIES_DIR = BASE_DIR / "summaries"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
