import chromadb
from chromadb.api.models import Collection
from langchain_huggingface import HuggingFaceEmbeddings

# Chroma setup
client = chromadb.Client()
chroma_collection = client.create_collection("rss-aggregator", get_or_create=True)


async def vector_store() -> Collection:
    return chroma_collection

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


async def embeddings():
    return embedding_model