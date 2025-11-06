from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Tweet, HistoricalTweet
from app.schemas import TweetResponse, TweetUpdate, ContentGenerationRequest, ContentGenerationResponse
from app.services.content_generator import get_content_generator
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[TweetResponse])
def get_tweets(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all tweets, optionally filtered by status"""
    query = db.query(Tweet)
    if status:
        query = query.filter(Tweet.status == status)
    tweets = query.order_by(Tweet.created_at.desc()).offset(skip).limit(limit).all()
    return tweets


@router.get("/{tweet_id}", response_model=TweetResponse)
def get_tweet(tweet_id: int, db: Session = Depends(get_db)):
    """Get a specific tweet by ID"""
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet


@router.patch("/{tweet_id}", response_model=TweetResponse)
def update_tweet(tweet_id: int, tweet_update: TweetUpdate, db: Session = Depends(get_db)):
    """Update a tweet (edit content, change status, schedule)"""
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    update_data = tweet_update.model_dump(exclude_unset=True)

    # If content is being updated, mark as edited
    if "content" in update_data:
        tweet.edited = True

    for key, value in update_data.items():
        setattr(tweet, key, value)

    db.commit()
    db.refresh(tweet)
    return tweet


@router.delete("/{tweet_id}")
def delete_tweet(tweet_id: int, db: Session = Depends(get_db)):
    """Delete a tweet"""
    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    db.delete(tweet)
    db.commit()
    return {"message": "Tweet deleted successfully"}


@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_tweets(
    request: ContentGenerationRequest,
    db: Session = Depends(get_db)
):
    """Trigger tweet generation using AI"""
    try:
        generator = get_content_generator(db)

        # Only fetch historical tweets if we don't have enough
        historical_count = db.query(HistoricalTweet).count()
        if historical_count < 50:
            try:
                stored = generator.fetch_and_store_historical_tweets(count=100)
                print(f"Fetched {stored} new historical tweets (total: {historical_count + stored})")
            except Exception as e:
                print(f"Note: Could not fetch historical tweets: {e}")
                # Continue anyway - might already have some stored
        else:
            print(f"Using existing {historical_count} historical tweets (skipping fetch to avoid rate limits)")

        # Generate new tweets
        results = generator.generate_daily_tweets(count=request.count)

        return ContentGenerationResponse(
            message=f"Successfully generated {results['total']} tweets ({results['claude']} from Claude, {results['chatgpt']} from ChatGPT)",
            tweets_generated=results['total'],
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating tweets: {str(e)}"
        )
