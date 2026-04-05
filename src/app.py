from rag_pipeline import query_rag

print("🚀 Improved RAG Agent Ready\n")

while True:
    query = input("\nAsk: ")

    if query.lower() in ["exit", "quit"]:
        break

    print("\n⏳ Thinking...\n")

    answer = query_rag(query)

    print(answer)