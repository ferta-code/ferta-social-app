"""Clean out all generated tweets from the database"""
from app.database import SessionLocal
from app.models import Tweet

def clean_tweets():
    db = SessionLocal()
    try:
        # Delete all generated tweets
        deleted = db.query(Tweet).delete()
        db.commit()
        print(f"✓ Deleted {deleted} tweets from database")
        return deleted
    except Exception as e:
        db.rollback()
        print(f"✗ Error cleaning tweets: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_tweets()
