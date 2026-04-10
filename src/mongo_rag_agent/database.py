# Database Module
# Handles MongoDB client initialization and database operations

from pymongo import MongoClient
from .config import get_mongodb_uri


def init_mongodb():
    """
    Initialize MongoDB client and collections.

    Returns:
        tuple: MongoDB client, vector search collection, full documents collection.
    """
    mongodb_client = MongoClient(get_mongodb_uri())

    DB_NAME = "ai_agents"

    vs_collection = mongodb_client[DB_NAME]["chunked_docs"]
    full_collection = mongodb_client[DB_NAME]["full_docs"]

    return mongodb_client, vs_collection, full_collection
