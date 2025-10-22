"""
Application settings and configuration
To be implemented in backend phase
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Google API
    google_api_key: str

    # Database
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "company_documents"

    # Document Storage
    upload_dir: str = "./documents"
    max_file_size: int = 10485760  # 10MB

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # Model Configuration
    embedding_model: str = "models/text-embedding-004"
    llm_model: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7
    max_tokens: int = 1024

    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
