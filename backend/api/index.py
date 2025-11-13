"""Vercel serverless function handler"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Export app directly for Vercel
# Vercel will handle ASGI apps natively
