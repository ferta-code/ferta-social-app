from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.content_generator import ContentGenerator
from app.config import get_settings
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class SchedulerService:
    """Service for scheduling automated tasks"""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.running = False

    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return

        # Parse content generation time (format: "HH:MM")
        hour, minute = map(int, settings.content_generation_time.split(':'))

        # Schedule daily content generation
        self.scheduler.add_job(
            self.generate_daily_content,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_content_generation',
            name='Generate daily tweet ideas',
            replace_existing=True
        )

        # Schedule tweet posting (check every hour for scheduled tweets)
        self.scheduler.add_job(
            self.post_scheduled_tweets,
            trigger=CronTrigger(minute=0),  # Every hour at minute 0
            id='post_scheduled_tweets',
            name='Post scheduled tweets',
            replace_existing=True
        )

        self.scheduler.start()
        self.running = True
        logger.info("Scheduler started successfully")

    def stop(self):
        """Stop the scheduler"""
        if not self.running:
            return

        self.scheduler.shutdown()
        self.running = False
        logger.info("Scheduler stopped")

    def generate_daily_content(self):
        """Generate daily tweet ideas"""
        logger.info("Starting daily content generation")
        db = SessionLocal()
        try:
            generator = ContentGenerator(db)

            # Fetch latest historical tweets (if any new ones)
            try:
                stored = generator.fetch_and_store_historical_tweets(count=50)
                logger.info(f"Fetched and stored {stored} new historical tweets")
            except Exception as e:
                logger.error(f"Error fetching historical tweets: {e}")

            # Generate new tweet ideas
            results = generator.generate_daily_tweets(count=settings.tweets_per_day)
            logger.info(f"Generated {results['total']} tweets: {results['claude']} from Claude, {results['chatgpt']} from ChatGPT")

        except Exception as e:
            logger.error(f"Error in daily content generation: {e}")
        finally:
            db.close()

    def post_scheduled_tweets(self):
        """Post tweets that are scheduled for this hour"""
        logger.info("Checking for scheduled tweets to post")
        db = SessionLocal()
        try:
            from app.models import Tweet

            # Get current hour window
            now = datetime.now()
            hour_start = now.replace(minute=0, second=0, microsecond=0)
            hour_end = hour_start + timedelta(hours=1)

            # Find tweets scheduled for this hour
            scheduled_tweets = db.query(Tweet).filter(
                Tweet.status == 'scheduled',
                Tweet.scheduled_time >= hour_start,
                Tweet.scheduled_time < hour_end
            ).all()

            logger.info(f"Found {len(scheduled_tweets)} tweets to post")

            generator = ContentGenerator(db)
            posted_count = 0

            for tweet in scheduled_tweets:
                try:
                    generator.post_tweet(tweet.id)
                    posted_count += 1
                    logger.info(f"Posted tweet {tweet.id}: {tweet.content[:50]}...")
                except Exception as e:
                    logger.error(f"Error posting tweet {tweet.id}: {e}")

            logger.info(f"Successfully posted {posted_count}/{len(scheduled_tweets)} tweets")

        except Exception as e:
            logger.error(f"Error in scheduled tweet posting: {e}")
        finally:
            db.close()


# Global scheduler instance
_scheduler_service = None


def get_scheduler_service() -> SchedulerService:
    """Get or create scheduler service instance"""
    global _scheduler_service
    if _scheduler_service is None:
        _scheduler_service = SchedulerService()
    return _scheduler_service
