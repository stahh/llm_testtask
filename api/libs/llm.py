import chromadb
from chromadb.api.models import Collection

# Chroma setup
client = chromadb.Client()
chroma_collection = client.create_collection("rss-aggregator", get_or_create=True)


async def vector_store() -> Collection:
    return chroma_collection
