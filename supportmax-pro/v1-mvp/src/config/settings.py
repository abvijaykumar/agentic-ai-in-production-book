import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings and configuration for v1 MVP.
    """
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SupportMax Pro v1.0"
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Selection
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    ANTHROPIC_MODEL: str = "claude-3-sonnet-20240229"
    
    # Vector DB Configuration
    CHROMA_PERSIST_DIRECTORY: str = "../../../db/chroma_db_v1"
    COLLECTION_NAME: str = "support_docs"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
