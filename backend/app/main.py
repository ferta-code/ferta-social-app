from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import engine, Base
from app.api import tweets, instagram, scheduler, config as config_router
from app.services.scheduler_service import get_scheduler_service

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup: Start the scheduler
    scheduler_service = get_scheduler_service()
    scheduler_service.start()
    print("✓ Scheduler started - daily content generation and tweet posting active")

    yield

    # Shutdown: Stop the scheduler
    scheduler_service.stop()
    print("✓ Scheduler stopped")


# Initialize FastAPI app
app = FastAPI(
    title="Ferta Social Media Automation",
    description="AI-powered content generation and scheduling for Ferta's social media",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tweets.router, prefix="/api/tweets", tags=["tweets"])
app.include_router(instagram.router, prefix="/api/instagram", tags=["instagram"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])
app.include_router(config_router.router, prefix="/api/config", tags=["config"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ferta Social Media Automation API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
