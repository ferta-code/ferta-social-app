from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base


class HistoricalTweet(Base):
    """Historical tweets from @joinferta for brand voice analysis"""
    __tablename__ = "historical_tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, index=True)
    content = Column(Text, nullable=False)
    posted_date = Column(DateTime, nullable=False)
    engagement_metrics = Column(JSON, default={})  # {likes, retweets, replies}
    fetched_at = Column(DateTime, server_default=func.now())
    topic_tags = Column(JSON, default=[])  # Array of identified topics


class Tweet(Base):
    """Generated tweets for approval and scheduling"""
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    ai_source = Column(String, nullable=False)  # 'claude' or 'chatgpt'
    status = Column(String, default="pending")  # pending/approved/scheduled/posted/failed
    scheduled_time = Column(DateTime, nullable=True)
    posted_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    edited = Column(Boolean, default=False)
    twitter_id = Column(String, nullable=True)  # Twitter API ID after posting


class InstagramPost(Base):
    """Instagram posts generated from approved tweets"""
    __tablename__ = "instagram_posts"

    id = Column(Integer, primary_key=True, index=True)
    source_tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)
    caption = Column(Text, nullable=False)
    image_url = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending/approved/posted/failed
    posted_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    instagram_id = Column(String, nullable=True)  # Instagram API ID after posting


class APICredential(Base):
    """Encrypted API credentials storage"""
    __tablename__ = "api_credentials"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, unique=True, nullable=False)  # twitter/instagram
    credentials = Column(Text, nullable=False)  # Encrypted JSON
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PostingSchedule(Base):
    """Posting schedule configuration"""
    __tablename__ = "posting_schedule"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # twitter/instagram
    time_slot = Column(String, nullable=False)  # HH:MM format
    frequency = Column(String, default="daily")  # daily/weekdays/custom
    active = Column(Boolean, default=True)
