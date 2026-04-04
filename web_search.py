from tavily import TavilyClient
from config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query):
    results = client.search(query=query, max_results=3)
    return "\n\n".join([r["content"] for r in results["results"]])