from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo
from app.database import get_db
from app.models import PostingSchedule, Tweet
from app.schemas import PostingScheduleResponse, PostingScheduleCreate
from app.services.content_generator import get_content_generator
from app.services.twitter_client import get_twitter_client
from app.config import get_settings

router = APIRouter()
settings = get_settings()
CENTRAL_TZ = ZoneInfo("America/Chicago")


@router.get("/", response_model=List[PostingScheduleResponse])
def get_schedules(db: Session = Depends(get_db)):
    """Get all posting schedules"""
    schedules = db.query(PostingSchedule).all()
    return schedules


@router.post("/", response_model=PostingScheduleResponse)
def create_schedule(schedule: PostingScheduleCreate, db: Session = Depends(get_db)):
    """Create a new posting schedule"""
    db_schedule = PostingSchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Delete a posting schedule"""
    schedule = db.query(PostingSchedule).filter(PostingSchedule.id == schedule_id).first()
    if not schedule:
        return {"message": "Schedule not found"}

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}


@router.get("/cron/generate-daily-tweets")
async def cron_generate_daily_tweets(request: Request, db: Session = Depends(get_db)):
    """
    Cron job endpoint: Generate daily tweets
    Called by Vercel Cron at scheduled time (9 AM CT = 2/3 PM UTC depending on DST)
    """
    # Verify this is coming from Vercel Cron
    user_agent = request.headers.get("user-agent", "")
    if "vercel-cron" not in user_agent.lower() and settings.environment == "production":
        return {"error": "Unauthorized - must be called by Vercel Cron"}

    try:
        generator = get_content_generator(db)

        # Delete old pending tweets
        old_pending = db.query(Tweet).filter(Tweet.status == "pending").all()
        deleted_count = len(old_pending)
        for tweet in old_pending:
            db.delete(tweet)
        db.commit()

        # Generate new tweets
        tweets_per_day = settings.tweets_per_day
        results = generator.generate_daily_tweets(count=tweets_per_day)

        return {
            "success": True,
            "message": f"Generated {results['total']} tweets",
            "deleted_old": deleted_count,
            "generated": results['total'],
            "timestamp": datetime.now(CENTRAL_TZ).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(CENTRAL_TZ).isoformat()
        }


@router.get("/cron/post-scheduled-tweets")
async def cron_post_scheduled_tweets(request: Request, db: Session = Depends(get_db)):
    """
    Cron job endpoint: Post scheduled tweets that are due
    Called by Vercel Cron every 15 minutes
    """
    # Verify this is coming from Vercel Cron
    user_agent = request.headers.get("user-agent", "")
    if "vercel-cron" not in user_agent.lower() and settings.environment == "production":
        return {"error": "Unauthorized - must be called by Vercel Cron"}

    try:
        twitter_client = get_twitter_client()
        now = datetime.now(CENTRAL_TZ)

        # Find tweets that are scheduled and due to be posted
        due_tweets = db.query(Tweet).filter(
            Tweet.status == "scheduled",
            Tweet.scheduled_time <= now
        ).all()

        posted_count = 0
        failed_count = 0
        errors = []

        for tweet in due_tweets:
            try:
                # Post to Twitter
                twitter_id = twitter_client.post_tweet(tweet.content)

                # Update tweet status
                tweet.status = "posted"
                tweet.posted_time = now
                tweet.twitter_id = twitter_id
                db.commit()

                posted_count += 1
            except Exception as e:
                tweet.status = "failed"
                db.commit()
                failed_count += 1
                errors.append(f"Tweet {tweet.id}: {str(e)}")

        return {
            "success": True,
            "posted": posted_count,
            "failed": failed_count,
            "total_checked": len(due_tweets),
            "errors": errors if errors else None,
            "timestamp": datetime.now(CENTRAL_TZ).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(CENTRAL_TZ).isoformat()
        }
