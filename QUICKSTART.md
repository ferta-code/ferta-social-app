# Quick Start Guide

Get the Ferta Social Media Automation app running in 5 minutes.

## Step 1: Install Dependencies

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Step 2: Configure API Keys

Copy the example environment file:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and add your API keys:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
TWITTER_BEARER_TOKEN=...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...

# Optional (for Instagram)
INSTAGRAM_APP_ID=...
INSTAGRAM_APP_SECRET=...
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_BUSINESS_ACCOUNT_ID=...
```

## Step 3: Start the Application

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the helper script:

```bash
cd backend
./start.sh
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

Or use the helper script:

```bash
cd frontend
./start.sh
```

## Step 4: Access the App

Open your browser to: http://localhost:5173

## Step 5: Generate Your First Tweets

1. Click "Generate New Tweets" button
2. Wait ~30 seconds while AI generates 25 tweet ideas
3. Review and edit the generated tweets
4. Click "Approve" on tweets you like
5. Click "Schedule" to queue them for posting

## Workflow Summary

```
Generate Tweets → Review & Edit → Approve → Schedule → Auto-Post
                         ↓
              Convert to Instagram Post
```

## API Access

**Backend API**: http://localhost:8000
**API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

## Common First Steps

### 1. Generate Initial Content

```bash
curl -X POST http://localhost:8000/api/tweets/generate \
  -H "Content-Type: application/json" \
  -d '{"count": 25}'
```

### 2. View Generated Tweets

```bash
curl http://localhost:8000/api/tweets/
```

### 3. Approve a Tweet

```bash
curl -X PATCH http://localhost:8000/api/tweets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

## What Gets Generated

**Daily at 9:00 AM** (configurable in `.env`):
- 25 new tweet ideas (12-13 from Claude, 12-13 from ChatGPT)
- Each tagged with AI source
- All focus on holistic fertility education
- Brand voice learned from @joinferta's past tweets

**Hourly**:
- Auto-posts any scheduled tweets

## Troubleshooting

### "No historical tweets found"

The app needs to fetch past tweets from @joinferta first. This happens automatically on first generation, but requires valid Twitter API credentials.

**Solution**: Ensure your Twitter credentials in `.env` are correct and have read access.

### "Module not found" errors

Make sure you've activated the virtual environment:

```bash
cd backend
source venv/bin/activate
```

### Frontend won't connect to backend

1. Ensure backend is running on port 8000
2. Check terminal output for errors
3. Try accessing http://localhost:8000/health

### API Rate Limits

**Twitter**: Basic tier allows 50 tweets/day
**OpenAI**: Pay-per-use, ~$0.10-0.50 per generation batch
**Claude**: Pay-per-use, ~$0.05-0.30 per generation batch

## Next Steps

- **Customize**: Edit prompts in `backend/app/services/claude_client.py` and `chatgpt_client.py`
- **Schedule**: Configure posting times in `.env`
- **Instagram**: Add Instagram credentials to enable auto-posting
- **Monitor**: Check logs for generation success/failures

## Need Help?

See full documentation in `README.md` or check the API docs at http://localhost:8000/docs
