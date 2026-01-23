import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import OllamaEmbeddings

EMBEDDINGS = OllamaEmbeddings(model="nomic-embed-text")

# ---- Chroma DB Config ----
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "agentic_rag"

# ---- Text Splitter ----
SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

# ---- Agent Definitions ----
AGENTS = {
    "pattern_detector": "data/agent_patterns",
    "clinical_strategist": "data/agent_strategies",
    "reflective_responder": "data/agent_responses",
    "safety_guard": "data/agent_safety",
}


def load_pdfs(folder_path: str) -> List:
    """Load all PDFs from a folder"""
    documents = []
    for pdf_file in Path(folder_path).glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())
    return documents


def ingest_agent_docs(agent_name: str, folder_path: str, vectordb: Chroma):
    print(f"\n📥 Ingesting PDFs for agent: {agent_name}")

    raw_docs = load_pdfs(folder_path)
    if not raw_docs:
        print("⚠️  No PDFs found.")
        return

    chunks = SPLITTER.split_documents(raw_docs)

    # Add agent metadata
    for doc in chunks:
        doc.metadata.update({
            "agent": agent_name,
            "source_type": "pdf"
        })

    vectordb.add_documents(chunks)
    print(f"Added {len(chunks)} chunks for {agent_name}")


def main():
    vectordb = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=EMBEDDINGS,
        persist_directory=CHROMA_DIR
    )

    for agent_name, folder in AGENTS.items():
        ingest_agent_docs(agent_name, folder, vectordb)

    vectordb.persist()
    print("\n All agents ingested successfully!")


if __name__ == "__main__":
    main()
