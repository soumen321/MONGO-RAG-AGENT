# Configuration Module
# Handles environment variables and configuration settings for the RAG application

import os
from dotenv import load_dotenv

load_dotenv()


def get_mongodb_uri():
    """Get MongoDB connection URI from environment variables."""
    return os.getenv("MONGODB_URI")


def get_openai_api_key():
    """Get OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")
