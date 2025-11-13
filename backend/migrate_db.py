"""Database migration to add edit tracking features"""
from app.database import engine, Base
from app.models import Tweet, TweetEdit
from sqlalchemy import inspect, text

def migrate():
    """Run database migration"""
    print("Running database migration...")

    # Get inspector to check existing columns
    inspector = inspect(engine)

    with engine.connect() as conn:
        # Check if original_content column exists in tweets table
        columns = [col['name'] for col in inspector.get_columns('tweets')]

        if 'original_content' not in columns:
            print("Adding original_content column to tweets table...")
            conn.execute(text(
                "ALTER TABLE tweets ADD COLUMN original_content TEXT"
            ))
            conn.commit()
            print("✓ Added original_content column")
        else:
            print("✓ original_content column already exists")

    # Create tweet_edits table if it doesn't exist
    if not inspector.has_table('tweet_edits'):
        print("Creating tweet_edits table...")
        TweetEdit.__table__.create(engine)
        print("✓ Created tweet_edits table")
    else:
        print("✓ tweet_edits table already exists")

    print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
