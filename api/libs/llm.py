import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

# Chroma setup
client = chromadb.Client()
vector = client.create_collection("rss-aggregator", get_or_create=True)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
