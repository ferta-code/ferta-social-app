from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import Optional, List, Dict, Any
from zoneinfo import ZoneInfo

# Central Time timezone
CENTRAL_TZ = ZoneInfo("America/Chicago")


# Historical Tweet Schemas
class HistoricalTweetBase(BaseModel):
    tweet_id: str
    content: str
    posted_date: datetime
    engagement_metrics: Dict[str, Any] = {}
    topic_tags: List[str] = []


class HistoricalTweetCreate(HistoricalTweetBase):
    pass


class HistoricalTweetResponse(HistoricalTweetBase):
    id: int
    fetched_at: datetime

    class Config:
        from_attributes = True


# Tweet Schemas
class TweetBase(BaseModel):
    content: str


class TweetCreate(TweetBase):
    ai_source: str


class TweetUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None
    scheduled_time: Optional[datetime] = None


class TweetResponse(TweetBase):
    id: int
    ai_source: str
    status: str
    scheduled_time: Optional[datetime] = None
    posted_time: Optional[datetime] = None
    created_at: datetime
    edited: bool
    twitter_id: Optional[str] = None

    @field_serializer('created_at', 'scheduled_time', 'posted_time')
    def serialize_dt(self, dt: Optional[datetime], _info) -> Optional[str]:
        if dt is None:
            return None
        # If datetime is naive, assume it's UTC (SQLite stores as UTC by default)
        if dt.tzinfo is None:
            from zoneinfo import ZoneInfo
            utc = ZoneInfo("UTC")
            dt = dt.replace(tzinfo=utc)
        # Convert to Central Time
        dt_central = dt.astimezone(CENTRAL_TZ)
        # Return ISO format with timezone
        return dt_central.isoformat()

    class Config:
        from_attributes = True


# Instagram Post Schemas
class InstagramPostBase(BaseModel):
    caption: str
    image_url: str


class InstagramPostCreate(InstagramPostBase):
    source_tweet_id: Optional[int] = None


class InstagramPostUpdate(BaseModel):
    caption: Optional[str] = None
    status: Optional[str] = None


class InstagramPostResponse(InstagramPostBase):
    id: int
    source_tweet_id: Optional[int] = None
    status: str
    posted_time: Optional[datetime] = None
    created_at: datetime
    instagram_id: Optional[str] = None

    class Config:
        from_attributes = True


# Posting Schedule Schemas
class PostingScheduleBase(BaseModel):
    platform: str
    time_slot: str
    frequency: str = "daily"
    active: bool = True


class PostingScheduleCreate(PostingScheduleBase):
    pass


class PostingScheduleResponse(PostingScheduleBase):
    id: int

    class Config:
        from_attributes = True


# Generation Request/Response
class ContentGenerationRequest(BaseModel):
    count: int = 25


class ContentGenerationResponse(BaseModel):
    message: str
    tweets_generated: int
    timestamp: datetime
