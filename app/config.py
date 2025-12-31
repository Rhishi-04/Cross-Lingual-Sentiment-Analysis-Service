"""Configuration management for the sentiment analysis service."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_title: str = "Cross-Lingual Sentiment Analysis Service"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Translation API Configuration
    # Google Translate doesn't require API key for basic usage
    # But you can set GOOGLE_TRANSLATE_API_KEY if using paid version
    google_translate_api_key: Optional[str] = None
    
    # Sentiment Model Configuration
    sentiment_model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

