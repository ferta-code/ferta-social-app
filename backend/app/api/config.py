from fastapi import APIRouter
from app.config import get_settings

router = APIRouter()


@router.get("/")
def get_config():
    """Get application configuration (non-sensitive values)"""
    settings = get_settings()
    return {
        "environment": settings.environment,
        "content_generation_time": settings.content_generation_time,
        "tweets_per_day": settings.tweets_per_day
    }
