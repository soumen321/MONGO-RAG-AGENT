# Embeddings Module
# Handles text embedding generation using OpenAI embeddings

from typing import List
from langchain_openai import OpenAIEmbeddings
from .config import get_openai_api_key


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a piece of text.

    Args:
        text (str): The text to embed.

    Returns:
        List[float]: The embedding of the text.
    """
    embedding_model = OpenAIEmbeddings(
        openai_api_key=get_openai_api_key(),
        model="text-embedding-3-small",
        dimensions=512,
    )

    embedding = embedding_model.embed_query(text)

    return embedding
