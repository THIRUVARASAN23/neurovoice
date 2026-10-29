"""
Vercel serverless entry point for the NeuroNexus FastAPI backend.
Vercel runs this file from the repo root, so we add the backend/ directory
to sys.path so that 'from app.main import app' resolves correctly.
Uses Mangum to wrap the FastAPI ASGI app as a serverless handler.
"""
import sys
import os

# Add this file's own directory (backend/) to sys.path so 'app' package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mangum import Mangum
from app.main import app  # noqa: E402

# Vercel calls `handler` for every incoming request
handler = Mangum(app, lifespan="off")
