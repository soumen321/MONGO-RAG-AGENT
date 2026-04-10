
from pymongo import MongoClient
from datasets import load_dataset
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

docs = load_dataset("MongoDB/mongodb-docs")
chunked_docs = load_dataset("MongoDB/mongodb-docs-embedded")



# Initialize a MongoDB Python client
mongodb_client = MongoClient(os.getenv("MONGODB_URI"))

#  Database name
DB_NAME = "ai_agents"
# Name of the collection with full documents- used for summarization
FULL_COLLECTION_NAME = "full_docs"
# Name of the collection for vector search- used for Q&A
VS_COLLECTION_NAME = "chunked_docs"
# Name of the vector search index
VS_INDEX_NAME = "vector_index"


db = mongodb_client[DB_NAME]
vs_collection = db[VS_COLLECTION_NAME]
full_collection = db[FULL_COLLECTION_NAME]

for doc in docs["train"]:
    # Insert the document into the full_docs collection
    full_collection.insert_one(doc)


for chunked_doc in chunked_docs["train"]:
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")
    embedding = embeddings.embed_query(chunked_doc["body"])
    print(chunked_doc["body"])
    print(embedding)
    chunked_doc["embedding"] = embedding
    vs_collection.insert_one(chunked_doc)
    

model = {
    "name": VS_INDEX_NAME,
    "type": "vectorSearch",
    "definition": {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 512,
                "similarity": "cosine",
            }
        ]
    },
}

vs_collection.create_search_index(model=model) 