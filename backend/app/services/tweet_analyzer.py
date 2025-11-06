from typing import List, Dict, Any
from collections import Counter
import re


class TweetAnalyzer:
    """Analyze historical tweets to extract patterns and insights"""

    def __init__(self, historical_tweets: List[Dict[str, Any]]):
        self.tweets = historical_tweets

    def extract_topics(self) -> List[str]:
        """
        Extract common topics/themes from tweets

        Returns:
            List of identified topics
        """
        # Common fertility-related keywords to look for
        fertility_keywords = [
            'fertility', 'ivf', 'natural', 'holistic', 'treatment', 'health',
            'nutrition', 'lifestyle', 'hormones', 'cycle', 'ovulation',
            'conception', 'pregnancy', 'women', 'wellness', 'restoration',
            'conventional', 'alternative', 'approach', 'success'
        ]

        topic_counts = Counter()

        for tweet in self.tweets:
            content_lower = tweet['content'].lower()
            for keyword in fertility_keywords:
                if keyword in content_lower:
                    topic_counts[keyword] += 1

        # Return top topics
        return [topic for topic, count in topic_counts.most_common(10)]

    def get_brand_voice_examples(self, count: int = 5) -> List[str]:
        """
        Get example tweets that represent the brand voice

        Args:
            count: Number of examples to return

        Returns:
            List of tweet texts
        """
        # Sort by engagement (sum of likes + retweets)
        sorted_tweets = sorted(
            self.tweets,
            key=lambda t: (
                t['engagement_metrics'].get('likes', 0) +
                t['engagement_metrics'].get('retweets', 0) * 2  # Weight retweets more
            ),
            reverse=True
        )

        return [tweet['content'] for tweet in sorted_tweets[:count]]

    def get_average_length(self) -> int:
        """Get average tweet length"""
        if not self.tweets:
            return 0

        total_length = sum(len(tweet['content']) for tweet in self.tweets)
        return total_length // len(self.tweets)

    def extract_common_phrases(self, min_words: int = 2, max_words: int = 4) -> List[str]:
        """
        Extract common multi-word phrases

        Args:
            min_words: Minimum words in a phrase
            max_words: Maximum words in a phrase

        Returns:
            List of common phrases
        """
        phrase_counter = Counter()

        for tweet in self.tweets:
            # Clean and tokenize
            text = re.sub(r'[^\w\s]', '', tweet['content'].lower())
            words = text.split()

            # Extract n-grams
            for n in range(min_words, max_words + 1):
                for i in range(len(words) - n + 1):
                    phrase = ' '.join(words[i:i + n])
                    # Filter out very common words
                    if not all(word in ['the', 'a', 'an', 'to', 'of', 'and', 'is', 'in', 'for', 'on'] for word in phrase.split()):
                        phrase_counter[phrase] += 1

        # Return top phrases that appear more than once
        return [phrase for phrase, count in phrase_counter.most_common(15) if count > 1]

    def get_analysis_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis summary

        Returns:
            Dictionary with analysis results
        """
        return {
            'total_tweets': len(self.tweets),
            'average_length': self.get_average_length(),
            'top_topics': self.extract_topics(),
            'brand_voice_examples': self.get_brand_voice_examples(),
            'common_phrases': self.extract_common_phrases(),
            'total_engagement': sum(
                tweet['engagement_metrics'].get('likes', 0) +
                tweet['engagement_metrics'].get('retweets', 0)
                for tweet in self.tweets
            )
        }
