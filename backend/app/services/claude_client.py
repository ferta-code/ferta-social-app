from anthropic import Anthropic
from typing import List, Dict, Any
from app.config import get_settings

settings = get_settings()


class ClaudeClient:
    """Client for Anthropic Claude API"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest as of Nov 2024

    def generate_tweets(
        self,
        count: int,
        brand_voice_examples: List[str],
        topics: List[str],
        common_phrases: List[str]
    ) -> List[str]:
        """
        Generate tweet ideas based on brand voice and topics

        Args:
            count: Number of tweets to generate
            brand_voice_examples: Example tweets showing brand voice
            topics: Common topics to focus on
            common_phrases: Common phrases used in past tweets

        Returns:
            List of generated tweet texts
        """
        # Create prompt with context
        prompt = self._build_tweet_generation_prompt(
            count, brand_voice_examples, topics, common_phrases
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.8,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse response - expecting numbered list
            content = response.content[0].text
            tweets = self._parse_tweet_list(content)

            return tweets[:count]  # Ensure we return exactly the requested count

        except Exception as e:
            print(f"Error generating tweets with Claude: {str(e)}")
            raise

    def _build_tweet_generation_prompt(
        self,
        count: int,
        brand_voice_examples: List[str],
        topics: List[str],
        common_phrases: List[str]
    ) -> str:
        """Build the prompt for tweet generation"""
        return f"""Generate {count} deeply insightful tweet ideas for @joinferta. These tweets should sound like Preethi Kasireddy and Alexander Cortes sharing hard-earned wisdom and nuanced perspectives on fertility with their community.

BRAND VOICE EXAMPLES:
{chr(10).join(f'- "{example}"' for example in brand_voice_examples)}

KEY TOPICS TO EXPLORE WITH DEPTH:
{', '.join(topics)}

COMMON PHRASES THAT RESONATE:
{', '.join(common_phrases)}

CONTENT DEPTH REQUIREMENTS:
- Challenge conventional thinking with specific, evidence-based counterpoints
- Share nuanced perspectives that acknowledge complexity, not just platitudes
- Include specific mechanisms, observations, or lesser-known insights
- Reference real experiences, case observations, or data points when relevant
- Reveal the "why" behind the advice, not just the "what"
- Address common misconceptions or contradictions in fertility advice
- Explore the psychological, physiological, or systemic aspects of fertility
- Make connections between seemingly unrelated factors (stress, nutrition, hormones, lifestyle)

TOPICS TO EXPLORE MORE DEEPLY:
- Why natural fertility restoration often works when conventional approaches fail
- The specific mechanisms of how lifestyle factors affect hormone balance
- Misconceptions about age, ovarian reserve, and fertility potential
- The role of insulin resistance, inflammation, and metabolic health in conception
- How stress and nervous system dysregulation impact reproductive hormones
- The fertility industry's incentives vs what actually helps people conceive
- Specific nutrition interventions and their hormonal impacts
- The difference between treating symptoms vs addressing root causes
- Personal journey insights from building Ferta and helping real people

VOICE & TONE REQUIREMENTS:
- Sound like a knowledgeable founder who's been in the trenches, not a generic wellness account
- Share specific insights and observations, not generic advice
- Be direct and sometimes contrarian when evidence supports it
- Use "I've seen", "what I've learned", "here's what most people miss" framing
- Sound like you're revealing something valuable that most people don't know
- Be authentic and vulnerable when sharing personal experiences
- Avoid oversimplification - embrace nuance and complexity
- Don't be preachy or judgmental, but be confident in evidence-based perspectives

STRICT FORMATTING RULES:
- NO hashtags at all
- NO emojis or icons
- 200-280 characters per tweet (allow space for depth)
- Pure text only

Please generate {count} tweet ideas. Return ONLY the tweets as a numbered list, with each tweet on a new line. Do not include any explanations or additional text.

Format:
1. [Tweet text]
2. [Tweet text]
etc.
"""

    def _parse_tweet_list(self, content: str) -> List[str]:
        """Parse numbered list of tweets from response"""
        tweets = []
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Remove numbering (1., 2., etc.)
            import re
            cleaned = re.sub(r'^\d+\.\s*', '', line)

            # Remove quotes if present
            cleaned = cleaned.strip('"\'')

            if cleaned and len(cleaned) <= 280:
                tweets.append(cleaned)

        return tweets

    def expand_caption(self, tweet_text: str) -> str:
        """
        Expand a tweet into a longer Instagram caption

        Args:
            tweet_text: Original tweet text

        Returns:
            Expanded Instagram caption
        """
        prompt = f"""You are creating Instagram content for Ferta, a holistic fertility education company.

Take this tweet and expand it into a thoughtful, engaging Instagram caption (3-5 sentences, about 150-200 words):

Tweet: "{tweet_text}"

Guidelines:
- Maintain the core message but add more depth and context
- Keep the educational, empowering tone
- Focus on holistic fertility and natural approaches
- Add a call-to-action or thought-provoking question at the end
- Make it Instagram-friendly and engaging
- Do not use hashtags (we'll add those separately)

Return ONLY the caption text, no explanations or additional formatting.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip().strip('"\'')

        except Exception as e:
            print(f"Error expanding caption with Claude: {str(e)}")
            raise


# Singleton instance
_claude_client = None


def get_claude_client() -> ClaudeClient:
    """Get or create Claude client instance"""
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client
