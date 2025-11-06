# Ferta Social Media Automation App - Specification

## Overview
An application that generates and schedules social media content for Ferta's Twitter (@joinferta) and Instagram (@joinferta) accounts.

## Tech Stack

### Backend
- **Framework**: Python with FastAPI (async support for schedulers)
- **Database**: SQLite (development) or PostgreSQL (production)
- **Task Queue**: APScheduler or Celery with Redis
- **API Integrations**: Twitter API v2, Instagram Graph API

### Frontend
- **Framework**: React with Vite
- **UI Components**: Modern, responsive dashboard

### AI Services
- **Text Generation**: Claude API + ChatGPT (GPT-4o)
- **Image Generation**: GPT-4o native image generation

## Content Guidelines

### Ferta Brand Focus
- **Primary Topic**: Holistic fertility education
- **Key Message**: Natural fertility restoration vs conventional fertility treatments (IVF, etc.)
- **Voice & Tone**: Educational, empowering, evidence-based
- **Target Audience**: People seeking natural approaches to fertility

### Tweet Topics
- Benefits of natural fertility restoration
- Limitations and risks of IVF and conventional treatments
- Holistic health approaches to fertility
- Evidence-based fertility education
- Success stories and testimonials
- Lifestyle factors affecting fertility
- Nutrition and fertility connection

## Content Generation Workflow

### Daily Tweet Generation Process
1. **Historical Context Loading**: Load past tweets from @joinferta to understand brand voice
2. **Topic Analysis**: Analyze what topics and angles have performed well
3. **AI Prompt Creation**: Create prompts for Claude and ChatGPT with:
   - Brand voice examples from historical tweets
   - Focus on holistic fertility education
   - Emphasis on natural approaches vs IVF
4. **Generate 20-30 Ideas**: Each AI generates 10-15 tweet ideas
5. **Store & Present**: Save to database and display in dashboard for review

### Instagram Post Generation Process (v1)
1. **Tweet Selection**: User selects 1 approved tweet to convert to Instagram post
2. **Caption Expansion**: AI expands tweet into thoughtful Instagram caption
3. **Image Generation**: GPT-4o generates aesthetic background image with:
   - Calming, professional aesthetic aligned with fertility/wellness brand
   - Tweet text overlaid on image
   - Brand-consistent color palette
4. **Review & Edit**: User reviews, edits caption if needed, approves for posting

## Core Features

### 1. Content Generation Service
- **Historical Tweet Analysis**: Fetch and analyze past tweets from @joinferta to understand brand voice and topic patterns
- **Daily Tweet Generation**: Generate 20-30 tweet ideas daily using both Claude and ChatGPT, informed by past tweets
- **Content Focus**: All tweets focus on holistic fertility education and natural restoration approaches
- **Instagram Post Generation (v1)**:
  - Select 1 best tweet per day from approved tweets
  - Transform into aesthetic image post with thoughtful caption
  - Generate visually appealing background image using GPT-4o
- **AI Source Tracking**: Tag each piece of content with its AI source (Claude/ChatGPT)
- **Storage**: Save all generated content to database with metadata

### 2. User Review Interface
- **Tweet Dashboard**: Display all daily tweet suggestions
- **AI Source Labels**: Show which AI generated each piece of content
- **Inline Editing**: Edit selected tweets directly in the interface
- **Selection Workflow**: Checkboxes to approve tweets for posting
- **Instagram Generation**:
  - After approving tweets, select 1 tweet to convert to Instagram post
  - Preview generated aesthetic image with tweet text overlay
  - Edit Instagram caption as needed
  - Approve for posting or manual export

### 3. Scheduling System
- **Tweet Queue**: Queue approved tweets for scheduled posting
- **Configurable Timing**: Set custom posting times throughout the day
- **Auto-Posting**: Automatically post approved tweets via Twitter API v2
- **Instagram Export**: Export images for manual posting or auto-post if API configured
- **Status Tracking**: Track scheduled, posted, and failed posts

### 4. API Integration Layer
- **Twitter API v2**: OAuth 2.0 authentication and tweet posting
- **Instagram Graph API**: Business account integration for automated posting
- **Rate Limiting**: Handle API rate limits gracefully
- **Error Handling**: Robust error handling and logging
- **Retry Logic**: Automatic retry for failed posts

## Database Schema

### `historical_tweets` table
- `id`: Primary key
- `tweet_id`: Twitter API tweet ID
- `content`: Tweet text
- `posted_date`: When tweet was posted
- `engagement_metrics`: JSON (likes, retweets, replies)
- `fetched_at`: When we fetched this tweet
- `topic_tags`: JSON array of identified topics

### `tweets` table
- `id`: Primary key
- `content`: Tweet text
- `ai_source`: Source AI (claude/chatgpt)
- `status`: pending/approved/scheduled/posted/failed
- `scheduled_time`: Timestamp for posting
- `posted_time`: Actual posting timestamp
- `created_at`: Generation timestamp
- `edited`: Boolean flag if user edited
- `twitter_id`: Twitter API ID after posting

### `instagram_posts` table
- `id`: Primary key
- `source_tweet_id`: Foreign key to tweets table (the tweet this was generated from)
- `caption`: Instagram caption text
- `image_url`: Generated aesthetic image URL
- `status`: pending/approved/posted/failed
- `posted_time`: Actual posting timestamp
- `created_at`: Generation timestamp
- `instagram_id`: Instagram API ID after posting

### `api_credentials` table
- `id`: Primary key
- `service`: twitter/instagram
- `credentials`: Encrypted JSON of tokens and keys
- `updated_at`: Last update timestamp

### `posting_schedule` table
- `id`: Primary key
- `platform`: twitter/instagram
- `time_slot`: Scheduled time
- `frequency`: daily/weekdays/custom
- `active`: Boolean flag

## Implementation Steps

### Phase 1: Project Setup
1. Initialize FastAPI backend project structure
2. Set up React + Vite frontend
3. Configure database (SQLite for dev, PostgreSQL for prod)
4. Set up environment variables for API keys

### Phase 2: Historical Data & AI Integration
5. Implement Twitter API v2 client to fetch historical tweets from @joinferta
6. Build historical tweet analyzer to extract topics and brand voice patterns
7. Implement Claude API client for content generation
8. Implement ChatGPT (GPT-4o) API client for content generation
9. Create content generation service that uses both AIs with historical context
10. Implement GPT-4o image generation for Instagram aesthetic posts

### Phase 3: Backend Core
11. Build database models and migrations
12. Create API endpoints for content management
13. Implement daily cron job for content generation
14. Build scheduling service with APScheduler

### Phase 4: Social Media APIs
15. Implement Twitter API v2 authentication and posting
16. Implement Instagram Graph API integration
17. Add rate limiting and error handling
18. Create retry logic for failed posts

### Phase 5: Frontend
19. Build main dashboard UI
20. Create tweet review and editing interface
21. Build Instagram conversion UI (tweet → aesthetic post)
22. Add configuration UI for posting schedules and preferences

### Phase 6: Testing & Deployment
23. Write unit tests for core services
24. Test API integrations with sandbox accounts
25. Deploy to production environment
26. Set up monitoring and logging

## API Keys Required

### AI Services
- **Anthropic Claude API Key**: For Claude-generated content
- **OpenAI API Key**: For ChatGPT text generation and GPT-4o image generation

### Social Media Platforms
- **Twitter API Credentials**:
  - API Key
  - API Secret
  - Bearer Token
  - Access Token
  - Access Token Secret
- **Instagram/Facebook Graph API Credentials**:
  - App ID
  - App Secret
  - Access Token
  - Instagram Business Account ID

## Important Notes

### Twitter API Requirements
- **Tier**: Basic tier ($100/month) required for write access
- **Rate Limits**: 50 tweets per 24 hours (Basic tier)
- **Authentication**: OAuth 2.0 required for posting

### Instagram API Requirements
- **Account Type**: Instagram Business or Creator account required
- **Facebook Connection**: Must be linked to a Facebook Business Page
- **Media Limits**: Maximum 10 items per carousel via API
- **Image Format**: JPEG only, minimum 600px width
- **Posting Limits**: 25 posts per 24 hours

### GPT-4o Image Generation
- **Advantages**: Native multimodal architecture, better text rendering in images
- **Capabilities**: Can generate up to 20 different items, multi-turn refinement
- **Method**: Autoregressive generation (vs diffusion in DALL-E)

## Future Enhancements
- Analytics dashboard showing engagement metrics
- A/B testing to compare Claude vs ChatGPT performance
- Thread generation for Twitter
- Video generation for Instagram Reels
- Automated hashtag suggestions
- Best time to post recommendations based on historical data
