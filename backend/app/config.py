from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str = "sqlite:///./ferta_social.db"

    # Anthropic Claude API
    anthropic_api_key: str

    # OpenAI API
    openai_api_key: str

    # Twitter API v2
    twitter_api_key: str
    twitter_api_secret: str
    twitter_bearer_token: str
    twitter_access_token: str
    twitter_access_token_secret: str

    # Instagram Graph API
    instagram_app_id: str = ""
    instagram_app_secret: str = ""
    instagram_access_token: str = ""
    instagram_business_account_id: str = ""

    # Supabase (optional - only needed if using Supabase features)
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""

    # Application Settings
    content_generation_time: str = "09:00"
    tweets_per_day: int = 25
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
