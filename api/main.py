"""
Vercel serverless entrypoint for FastAPI application.
This file imports the FastAPI app from backend/main.py for Vercel deployment.
"""
import sys
import os

# Add the parent directory to the Python path so we can import the backend module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app from backend.main
from backend.main import app

# This is the entrypoint that Vercel will use
