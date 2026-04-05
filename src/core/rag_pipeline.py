from src.core.llm import get_llm
from src.core.retriever import get_retriever

llm = get_llm()
retriever = get_retriever()

def expand_query(query):
    return [
        query,
        f"{query} explanation",
        f"{query} challenges",
        f"{query} issues",
        f"{query} meaning"
    ]

def retrieve_docs(question):
    all_docs = []
    queries = expand_query(question)
    
    for q in queries:
        docs = retriever.invoke(q)
        all_docs.extend(docs)
    
    # Remove duplicates
    unique_docs = []
    seen = set()
    
    for doc in all_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_docs.append(doc)
    
    return unique_docs[:8]

def query_rag(question):
    docs = retrieve_docs(question)
    
    if not docs:
        return "No relevant information found in uploaded documents."
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
You are an HR Assistant for the company.

Use the context below to answer the question.
Even if partial information is available, provide the best possible answer.

Context:
{context}

Question: {question}

Answer in clear structured points.
"""
    
    answer = llm.invoke(prompt)
    return answer.content if hasattr(answer, 'content') else str(answer)