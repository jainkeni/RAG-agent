# src/utils/upload_docs.py
import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.retriever import get_vectorstore

DATA_PATH = "data/hr_documents"

def load_documents():
    """Load all HR documents from data/hr_documents/"""
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
                print(f"⏭️  Skipped unsupported file: {file}")
                continue

            documents.extend(loader.load())
            print(f"✅ Loaded: {file}")

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

    return documents

def ingest_documents():
    """Ingest documents into ChromaDB"""
    print("\n" + "="*60)
    print("📂 HR AGENT - DOCUMENT INGESTION")
    print("="*60 + "\n")
    
    print("Step 1: Loading HR documents from data/hr_documents/...")
    documents = load_documents()

    if not documents:
        print("\n❌ No valid documents found.")
        print("ℹ️  Make sure you have .txt, .pdf, or .docx files in data/hr_documents/")
        return

    print(f"\n📄 Found {len(documents)} document chunks")
    
    print("\nStep 2: Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)
    print(f"✂️  Split into {len(chunks)} chunks")

    print("\nStep 3: Storing in ChromaDB...")
    db = get_vectorstore()
    db.add_documents(chunks)
    # Remove the persist() call - ChromaDB auto-persists now
    # db.persist()

    print("\n" + "="*60)
    print("✅ INGESTION COMPLETE!")
    print("="*60)
    print("\nYour HR documents are now ready for queries!\n")

if __name__ == "__main__":
    ingest_documents()