# src/core/retriever.py
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src.utils.config import OPENAI_API_KEY

def get_embeddings():
    """Get OpenAI embeddings"""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found. Please set it in .env file")
    
    return OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def get_retriever():
    """Get vector store retriever"""
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings
    )
    return vectorstore.as_retriever()

def get_vectorstore():
    """Get vector store for adding documents"""
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings
    )
    return vectorstore