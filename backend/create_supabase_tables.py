"""
Create all database tables in Supabase PostgreSQL
"""
from app.database import Base, engine
from app.models import (
    HistoricalTweet,
    Tweet,
    TweetEdit,
    InstagramPost,
    APICredential,
    PostingSchedule
)

def create_tables():
    """Create all tables in Supabase"""
    print("Creating tables in Supabase PostgreSQL...")

    # Drop all tables first (clean slate)
    print("Dropping existing tables if any...")
    Base.metadata.drop_all(bind=engine)

    # Create all tables
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)

    print("✓ All tables created successfully!")
    print("\nTables created:")
    print("  - historical_tweets")
    print("  - tweets")
    print("  - tweet_edits")
    print("  - instagram_posts")
    print("  - api_credentials")
    print("  - posting_schedule")

if __name__ == "__main__":
    create_tables()
