from langchain_community.vectorstores import Chroma
from embeddings import get_embeddings

CHROMA_PATH = "chroma_db"

def get_vectorstore():
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings()
    )
    return db


def get_retriever():
    db = get_vectorstore()
    return db.as_retriever(
        search_type="mmr",  # better diversity
        search_kwargs={
            "k": 8,         # increased from 3
            "fetch_k": 20   # fetch more candidates
        }
    )