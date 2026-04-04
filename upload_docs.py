import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from retriever import get_vectorstore

DATA_PATH = "data"

def load_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)

        try:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(path)

            elif file.endswith(".txt") or file.endswith(".md"):
                loader = TextLoader(path, encoding="utf-8")

            elif file.endswith(".csv"):
                loader = CSVLoader(path)

            elif file.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(path)

            else:
                print(f"Skipped unsupported file: {file}")
                continue

            documents.extend(loader.load())
            print(f"Loaded: {file}")

        except Exception as e:
            print(f"Error loading {file}: {e}")

    return documents


def ingest_documents():
    documents = load_documents()

    if not documents:
        print("No valid documents found.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    db = get_vectorstore()
    db.add_documents(chunks)
    db.persist()

    print("✅ Documents stored in Chroma DB")


if __name__ == "__main__":
    ingest_documents()