# Ferta Social Media Automation App

AI-powered content generation and scheduling for Ferta's Twitter (@joinferta) and Instagram (@joinferta) accounts.

## Features

- **AI-Powered Content Generation**: Generate 20-30 tweet ideas daily using Claude and ChatGPT
- **Historical Analysis**: Analyzes past tweets to maintain brand voice and topic consistency
- **Smart Scheduling**: Automatically schedule and post approved tweets
- **Instagram Integration**: Convert tweets into aesthetic Instagram posts with AI-generated images
- **Dual AI Approach**: Compare content from both Claude and ChatGPT
- **Interactive Dashboard**: Review, edit, and approve content before posting

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy + SQLite/PostgreSQL
- Anthropic Claude API
- OpenAI GPT-4o (text + image generation)
- Twitter API v2
- Instagram Graph API
- APScheduler (task scheduling)

**Frontend:**
- React + TypeScript
- Vite (build tool)
- TanStack Query (data fetching)
- Axios (HTTP client)

## Prerequisites

1. **Python 3.9+**
2. **Node.js 18+**
3. **API Keys:**
   - Anthropic Claude API key
   - OpenAI API key
   - Twitter API v2 credentials (requires Basic tier $100/month for posting)
   - Instagram Graph API credentials (optional)

## Installation

### 1. Clone or Navigate to Project

```bash
cd "Ferta socials bot"
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `backend/.env` with your API keys:

```env
# Database
DATABASE_URL=sqlite:///./ferta_social.db

# Anthropic Claude API
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI API (ChatGPT + GPT-4o)
OPENAI_API_KEY=your_openai_api_key_here

# Twitter API v2
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here

# Instagram Graph API (optional)
INSTAGRAM_APP_ID=your_instagram_app_id_here
INSTAGRAM_APP_SECRET=your_instagram_app_secret_here
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id_here

# Application Settings
CONTENT_GENERATION_TIME=09:00
TWEETS_PER_DAY=25
ENVIRONMENT=development
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # Activate venv if not already active
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## Usage

### First Time Setup

1. **Fetch Historical Tweets**:
   - The app needs to analyze past tweets from @joinferta to understand brand voice
   - This happens automatically on first content generation
   - Or manually trigger via API:
     ```bash
     curl -X POST http://localhost:8000/api/tweets/generate
     ```

2. **Generate Tweet Ideas**:
   - Click "Generate New Tweets" button in the dashboard
   - The app will generate 20-30 tweet ideas using Claude and ChatGPT
   - Each tweet is tagged with its AI source

3. **Review and Edit**:
   - Browse generated tweets in the dashboard
   - Edit any tweet by clicking "Edit"
   - Approve tweets you like by clicking "Approve"

4. **Schedule Tweets**:
   - Click "Schedule" on approved tweets
   - Set desired posting time
   - Tweets will be posted automatically

5. **Create Instagram Posts**:
   - Select an approved tweet
   - Convert it to an Instagram post
   - AI generates aesthetic image with text overlay
   - Edit caption if needed
   - Download or post to Instagram

## API Endpoints

### Tweets

- `GET /api/tweets/` - List all tweets (filter by status)
- `GET /api/tweets/{id}` - Get specific tweet
- `PATCH /api/tweets/{id}` - Update tweet (edit content, change status)
- `DELETE /api/tweets/{id}` - Delete tweet
- `POST /api/tweets/generate` - Generate new tweet ideas

### Instagram

- `GET /api/instagram/` - List Instagram posts
- `GET /api/instagram/{id}` - Get specific post
- `POST /api/instagram/` - Create Instagram post
- `PATCH /api/instagram/{id}` - Update post
- `DELETE /api/instagram/{id}` - Delete post

### Scheduler

- `GET /api/scheduler/` - List posting schedules
- `POST /api/scheduler/` - Create posting schedule
- `DELETE /api/scheduler/{id}` - Delete schedule

### Config

- `GET /api/config/` - Get application configuration

## Scheduled Tasks

The app runs two automated tasks:

1. **Daily Content Generation** (default: 9:00 AM):
   - Fetches latest tweets from @joinferta
   - Analyzes brand voice and topics
   - Generates new tweet ideas

2. **Scheduled Tweet Posting** (hourly):
   - Checks for tweets scheduled to post in the current hour
   - Posts them to Twitter automatically
   - Updates status in database

## Project Structure

```
Ferta socials bot/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── services/      # Business logic services
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database setup
│   │   ├── main.py        # FastAPI application
│   │   ├── models.py      # Database models
│   │   └── schemas.py     # Pydantic schemas
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── api/           # API client functions
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── types/         # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── SPEC.md
└── README.md
```

## Content Guidelines

The app generates content focused on:

- Holistic fertility education
- Natural fertility restoration vs IVF/conventional treatments
- Evidence-based, educational tone
- Lifestyle and nutrition for fertility
- Empowering and hopeful messaging

Brand voice is learned from historical @joinferta tweets.

## Troubleshooting

### Twitter API Issues

- **Error: "Not authorized"**: Check your API credentials in `.env`
- **Error: "Rate limit exceeded"**: Wait and try again, or upgrade API tier
- **Error: "Tweet not found"**: Ensure @joinferta username is correct

### Database Issues

- **Error: "Table doesn't exist"**: Delete `ferta_social.db` and restart backend
- The database is created automatically on first run

### Frontend Not Connecting to Backend

- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify proxy settings in `frontend/vite.config.ts`

## API Rate Limits

**Twitter API (Basic Tier - $100/month):**
- 50 tweets per 24 hours
- 10,000 tweet reads per month

**OpenAI API:**
- Pay-per-use pricing
- GPT-4o: ~$2.50-$10 per 1M tokens
- Image generation: ~$0.04-$0.08 per image

**Anthropic Claude API:**
- Pay-per-use pricing
- Claude 3.5 Sonnet: ~$3 per 1M input tokens

## Future Enhancements

- Analytics dashboard for engagement tracking
- A/B testing for Claude vs ChatGPT performance
- Twitter thread generation
- Instagram Reels generation
- Automated hashtag suggestions
- Best time to post recommendations
- Multi-account support

## Support

For issues or questions:
1. Check this README
2. Review `SPEC.md` for detailed specifications
3. Check API documentation:
   - [Twitter API v2 Docs](https://developer.twitter.com/en/docs/twitter-api)
   - [OpenAI API Docs](https://platform.openai.com/docs)
   - [Anthropic Claude Docs](https://docs.anthropic.com)

## License

Private project for Ferta.
