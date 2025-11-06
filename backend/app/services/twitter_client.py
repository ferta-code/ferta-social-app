import tweepy
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.config import get_settings

settings = get_settings()


class TwitterClient:
    """Client for Twitter API v2 operations"""

    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=settings.twitter_bearer_token,
            consumer_key=settings.twitter_api_key,
            consumer_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret,
            wait_on_rate_limit=True
        )

    def fetch_user_tweets(
        self,
        username: str,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent tweets from a user's timeline

        Args:
            username: Twitter username (without @)
            max_results: Maximum number of tweets to fetch (max 100 per request)

        Returns:
            List of tweet dictionaries with content and metadata
        """
        try:
            # Get user ID from username
            user = self.client.get_user(username=username)
            if not user.data:
                raise ValueError(f"User @{username} not found")

            user_id = user.data.id

            # Fetch user's tweets
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'text'],
                exclude=['retweets', 'replies']  # Only original tweets
            )

            if not tweets.data:
                return []

            # Format tweets
            formatted_tweets = []
            for tweet in tweets.data:
                formatted_tweets.append({
                    'tweet_id': str(tweet.id),
                    'content': tweet.text,
                    'posted_date': tweet.created_at,
                    'engagement_metrics': {
                        'likes': tweet.public_metrics.get('like_count', 0),
                        'retweets': tweet.public_metrics.get('retweet_count', 0),
                        'replies': tweet.public_metrics.get('reply_count', 0),
                        'quotes': tweet.public_metrics.get('quote_count', 0)
                    }
                })

            return formatted_tweets

        except Exception as e:
            print(f"Error fetching tweets for @{username}: {str(e)}")
            raise

    def post_tweet(self, content: str) -> Optional[str]:
        """
        Post a tweet

        Args:
            content: Tweet text (max 280 characters)

        Returns:
            Tweet ID if successful, None otherwise
        """
        try:
            if len(content) > 280:
                raise ValueError("Tweet content exceeds 280 characters")

            response = self.client.create_tweet(text=content)
            return str(response.data['id']) if response.data else None

        except Exception as e:
            print(f"Error posting tweet: {str(e)}")
            raise

    def delete_tweet(self, tweet_id: str) -> bool:
        """
        Delete a tweet

        Args:
            tweet_id: ID of the tweet to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.delete_tweet(id=tweet_id)
            return response.data.get('deleted', False)

        except Exception as e:
            print(f"Error deleting tweet {tweet_id}: {str(e)}")
            return False


# Singleton instance
_twitter_client = None


def get_twitter_client() -> TwitterClient:
    """Get or create Twitter client instance"""
    global _twitter_client
    if _twitter_client is None:
        _twitter_client = TwitterClient()
    return _twitter_client
