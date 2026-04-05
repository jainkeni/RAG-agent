# src/core/llm.py
from langchain_openai import ChatOpenAI
from src.utils.config import OPENAI_API_KEY

def get_llm():
    """Get OpenAI LLM"""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found. Please set it in .env file")
    
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=OPENAI_API_KEY
    )