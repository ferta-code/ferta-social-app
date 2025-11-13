"""
Migrate data from SQLite to Supabase PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import (
    HistoricalTweet,
    Tweet,
    TweetEdit,
    InstagramPost,
    APICredential,
    PostingSchedule
)

# SQLite connection
SQLITE_URL = "sqlite:///./ferta_social.db"
sqlite_engine = create_engine(SQLITE_URL)
SQLiteSession = sessionmaker(bind=sqlite_engine)

# PostgreSQL connection (from .env)
from app.database import engine as postgres_engine, SessionLocal as PostgresSession

def migrate_data():
    """Migrate all data from SQLite to Supabase"""
    print("Starting data migration from SQLite to Supabase...")

    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()

    try:
        # Migrate HistoricalTweets
        print("\nMigrating historical_tweets...")
        historical_tweets = sqlite_session.query(HistoricalTweet).all()
        for tweet in historical_tweets:
            # Create new instance with same data
            new_tweet = HistoricalTweet(
                id=tweet.id,
                tweet_id=tweet.tweet_id,
                content=tweet.content,
                posted_date=tweet.posted_date,
                engagement_metrics=tweet.engagement_metrics,
                fetched_at=tweet.fetched_at,
                topic_tags=tweet.topic_tags
            )
            postgres_session.merge(new_tweet)
        postgres_session.commit()
        print(f"✓ Migrated {len(historical_tweets)} historical tweets")

        # Migrate Tweets
        print("\nMigrating tweets...")
        tweets = sqlite_session.query(Tweet).all()
        for tweet in tweets:
            new_tweet = Tweet(
                id=tweet.id,
                content=tweet.content,
                original_content=tweet.original_content,
                ai_source=tweet.ai_source,
                status=tweet.status,
                scheduled_time=tweet.scheduled_time,
                posted_time=tweet.posted_time,
                created_at=tweet.created_at,
                edited=tweet.edited,
                twitter_id=tweet.twitter_id
            )
            postgres_session.merge(new_tweet)
        postgres_session.commit()
        print(f"✓ Migrated {len(tweets)} tweets")

        # Migrate TweetEdits
        print("\nMigrating tweet_edits...")
        tweet_edits = sqlite_session.query(TweetEdit).all()
        for edit in tweet_edits:
            new_edit = TweetEdit(
                id=edit.id,
                tweet_id=edit.tweet_id,
                original_text=edit.original_text,
                edited_text=edit.edited_text,
                edit_timestamp=edit.edit_timestamp,
                ai_source=edit.ai_source
            )
            postgres_session.merge(new_edit)
        postgres_session.commit()
        print(f"✓ Migrated {len(tweet_edits)} tweet edits")

        # Migrate InstagramPosts
        print("\nMigrating instagram_posts...")
        instagram_posts = sqlite_session.query(InstagramPost).all()
        for post in instagram_posts:
            new_post = InstagramPost(
                id=post.id,
                source_tweet_id=post.source_tweet_id,
                caption=post.caption,
                image_url=post.image_url,
                status=post.status,
                posted_time=post.posted_time,
                created_at=post.created_at,
                instagram_id=post.instagram_id
            )
            postgres_session.merge(new_post)
        postgres_session.commit()
        print(f"✓ Migrated {len(instagram_posts)} instagram posts")

        # Migrate APICredentials
        print("\nMigrating api_credentials...")
        api_credentials = sqlite_session.query(APICredential).all()
        for cred in api_credentials:
            new_cred = APICredential(
                id=cred.id,
                service=cred.service,
                credentials=cred.credentials,
                updated_at=cred.updated_at
            )
            postgres_session.merge(new_cred)
        postgres_session.commit()
        print(f"✓ Migrated {len(api_credentials)} API credentials")

        # Migrate PostingSchedules
        print("\nMigrating posting_schedule...")
        schedules = sqlite_session.query(PostingSchedule).all()
        for schedule in schedules:
            new_schedule = PostingSchedule(
                id=schedule.id,
                platform=schedule.platform,
                time_slot=schedule.time_slot,
                frequency=schedule.frequency,
                active=schedule.active
            )
            postgres_session.merge(new_schedule)
        postgres_session.commit()
        print(f"✓ Migrated {len(schedules)} posting schedules")

        print("\n✅ Data migration completed successfully!")
        print(f"\nSummary:")
        print(f"  - Historical tweets: {len(historical_tweets)}")
        print(f"  - Tweets: {len(tweets)}")
        print(f"  - Tweet edits: {len(tweet_edits)}")
        print(f"  - Instagram posts: {len(instagram_posts)}")
        print(f"  - API credentials: {len(api_credentials)}")
        print(f"  - Posting schedules: {len(schedules)}")

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        postgres_session.rollback()
        raise
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    migrate_data()
