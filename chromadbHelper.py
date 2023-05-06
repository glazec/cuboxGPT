import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os


# @todo update entires in chromadb
# @todo add hash metadata to chromadb
# @todo add alert to file which has too short introduction
# @todo add use case or scenario to metadata


# get environment variable
chroma_client = chromadb.Client()
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    # Optional, defaults to .chromadb/ in the current directory
    persist_directory="db"
))
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get('OPENAI_API_KEY'),
    model_name="text-embedding-ada-002"
)
collection = client.get_collection(
    name="my_collection", embedding_function=openai_ef)
