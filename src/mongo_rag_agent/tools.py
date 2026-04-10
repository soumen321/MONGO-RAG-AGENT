# Tools Module
# Defines the tools available to the RAG agent for information retrieval

from langchain_core.tools import tool
from .database import init_mongodb
from .embeddings import generate_embedding


@tool
def get_information_for_question_answering(user_query: str) -> str:
    """
    Retrieve relevant documents for a user query using vector search.

    Args:
        user_query (str): The user's query.

    Returns:
        str: The retrieved documents as a string.
    """

    query_embedding = generate_embedding(user_query)
    vs_collection = init_mongodb()[1]

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 150,
                "limit": 5,
            }
        },
        {
            "$project": {
                "_id": 0,
                "body": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    results = vs_collection.aggregate(pipeline)
    context = "\n\n".join([doc.get("body") for doc in results])

    return context


@tool
def get_page_content_for_summarization(user_query: str) -> str:
    """
    Retrieve the content of a documentation page for summarization.

    Args:
        user_query (str): The user's query (title of the documentation page).

    Returns:
        str: The content of the documentation page.
    """
    full_collection = init_mongodb()[2]

    query = {"title": user_query}
    projection = {"_id": 0, "body": 1}

    document = full_collection.find_one(query, projection)

    if document:
        return document["body"]
    return "Document not found"
