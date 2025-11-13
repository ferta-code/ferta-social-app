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
        common_phrases: List[str],
        edit_examples: List[dict] = None
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
            count, brand_voice_examples, topics, common_phrases, edit_examples
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
        common_phrases: List[str],
        edit_examples: List[dict] = None
    ) -> str:
        """Build the prompt for tweet generation"""

        # Build the edit examples section if available
        edit_section = ""
        if edit_examples and len(edit_examples) > 0:
            edit_section = "\n\nLEARN FROM THESE EDITS - Your previous tweets were edited to be better. Study these to understand what makes a great tweet:\n\n"
            for i, example in enumerate(edit_examples, 1):
                edit_section += f"Example {i}:\n"
                edit_section += f"Original (not good enough): \"{example['original']}\"\n"
                edit_section += f"Improved version: \"{example['improved']}\"\n\n"
            edit_section += "IMPORTANT: Analyze what changed in these edits. Notice the patterns:\n"
            edit_section += "- Did the improved version add more directness?\n"
            edit_section += "- Did it add actionable advice?\n"
            edit_section += "- Did it make bolder claims?\n"
            edit_section += "- Did it simplify the language?\n"
            edit_section += "Apply these lessons to the new tweets you generate.\n"

        return f"""Generate {count} substantive, high-impact tweet ideas for @joinferta. These tweets should be bold, direct, and actionable - like Preethi Kasireddy cutting through the noise with hard truths about fertility.

BRAND VOICE EXAMPLES:
{chr(10).join(f'- "{example}"' for example in brand_voice_examples)}

KEY TOPICS TO EXPLORE WITH DEPTH:
{', '.join(topics)}

COMMON PHRASES THAT RESONATE:
{', '.join(common_phrases)}{edit_section}

CRITICAL: WRITE WITH SUBSTANCE AND IMPACT

BAD EXAMPLE (too academic, no punch):
"Why stress matters: Chronic stress dysregulates the nervous system, throwing hormones like cortisol out of balance. This cascade directly impacts fertility."

GOOD EXAMPLE (direct, actionable, impactful):
"Stress is the #1 killer of fertility. Cortisol will steal resources from all your other reproductive hormones, making you less fertile. If there is one thing you can do today to improve your fertility, it is to get better at managing stress."

WHAT MAKES THE GOOD EXAMPLE WORK:
- Opens with a bold, direct statement (#1 killer)
- Explains the mechanism simply (cortisol steals resources)
- Ends with clear, actionable advice (do this today)
- Uses strong, confident language (will steal, less fertile)
- No hedging or academic distance

CONTENT REQUIREMENTS:
- Lead with the bold claim or most important insight first
- Explain the mechanism in simple, direct language
- Include specific, actionable advice when relevant
- Use strong, confident language ("will", "is", "causes" not "may" or "can")
- Make it feel urgent and important
- Focus on what people can DO, not just what they should know
- Explain cause-and-effect clearly (X steals from Y, causing Z)
- Challenge common beliefs with evidence-based truths

TOPICS TO EXPLORE WITH BOLD CLAIMS:
- Why stress management is more important than most medical interventions
- How insulin resistance directly blocks conception pathways
- The specific ways seed oils and processed foods destroy hormone balance
- Why your doctor isn't telling you about root causes (system incentives)
- How nervous system dysregulation makes pregnancy impossible
- Why age isn't the limiting factor most people think it is
- The direct hormone-stealing effects of chronic stress
- How inflammation blocks receptor sites for fertility hormones
- Why treating PCOS with birth control makes it worse long-term
- The metabolic switches that turn fertility on and off

VOICE & TONE:
- Write like you're sharing an urgent truth, not teaching a lesson
- Be direct and confident, not hedging or academic
- Use "will" and "is" instead of "may" and "might"
- Make bold claims backed by mechanisms
- Sound like you're revealing something important people need to know
- End with clear action steps when relevant ("do this today", "start here")
- Avoid softening language ("kind of", "sort of", "a bit")
- No platitudes or generic wellness advice

STRUCTURE FORMULA:
1. Bold claim/statement of the problem
2. Explain the mechanism (how it works)
3. Actionable takeaway or next step (when relevant)

STRICT FORMATTING RULES:
- NO hashtags at all
- NO emojis or icons
- 200-280 characters per tweet
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
