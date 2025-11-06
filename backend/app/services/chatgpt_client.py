from openai import OpenAI
from typing import List
from app.config import get_settings

settings = get_settings()


class ChatGPTClient:
    """Client for OpenAI ChatGPT API"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.text_model = "gpt-4o"
        self.image_model = "gpt-4o"  # GPT-4o with native image generation

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
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {"role": "system", "content": "You are a social media content creator for Ferta, specializing in holistic fertility education."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )

            # Parse response
            content = response.choices[0].message.content
            tweets = self._parse_tweet_list(content)

            return tweets[:count]

        except Exception as e:
            print(f"Error generating tweets with ChatGPT: {str(e)}")
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

Return ONLY a numbered list of tweets, one per line. No explanations.

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

            # Remove numbering
            import re
            cleaned = re.sub(r'^\d+\.\s*', '', line)
            cleaned = cleaned.strip('"\'')

            if cleaned and len(cleaned) <= 280:
                tweets.append(cleaned)

        return tweets

    def generate_image(self, prompt: str, tweet_text: str) -> str:
        """
        Generate an aesthetic image for Instagram using GPT-4o

        Args:
            prompt: Image generation prompt
            tweet_text: Text to overlay on image

        Returns:
            URL of generated image
        """
        # Build comprehensive prompt for aesthetic wellness image
        full_prompt = f"""Create a calming, professional aesthetic image for an Instagram post about fertility and wellness.

Style requirements:
- Soft, muted color palette (pastels, earth tones, calming blues/greens)
- Clean, minimalist design
- Professional and trustworthy aesthetic
- Wellness/health/nature themed
- Modern and Instagram-friendly

The image should include this text overlaid beautifully:
"{tweet_text}"

Additional context: {prompt}

The overall feel should be: calming, empowering, hopeful, and professional."""

        try:
            # Note: As of 2025, GPT-4o supports native image generation
            # This is a placeholder for the actual API call
            # The actual implementation would use the image generation endpoint
            response = self.client.images.generate(
                model="dall-e-3",  # Using DALL-E 3 for now as GPT-4o image API may have different syntax
                prompt=full_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            return response.data[0].url

        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise

    def expand_caption(self, tweet_text: str) -> str:
        """
        Expand a tweet into a longer Instagram caption

        Args:
            tweet_text: Original tweet text

        Returns:
            Expanded Instagram caption
        """
        prompt = f"""Expand this tweet into a thoughtful Instagram caption (3-5 sentences, 150-200 words):

Tweet: "{tweet_text}"

Guidelines:
- Maintain core message but add depth
- Educational, empowering tone for holistic fertility education
- Focus on natural approaches
- End with engaging call-to-action or question
- Instagram-friendly
- No hashtags

Return only the caption text.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {"role": "system", "content": "You are creating Instagram captions for Ferta's holistic fertility education content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )

            return response.choices[0].message.content.strip().strip('"\'')

        except Exception as e:
            print(f"Error expanding caption: {str(e)}")
            raise


# Singleton instance
_chatgpt_client = None


def get_chatgpt_client() -> ChatGPTClient:
    """Get or create ChatGPT client instance"""
    global _chatgpt_client
    if _chatgpt_client is None:
        _chatgpt_client = ChatGPTClient()
    return _chatgpt_client
