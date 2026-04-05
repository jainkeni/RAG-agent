from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY

def get_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=OPENAI_API_KEY
    )