from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings


_embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")


def get_user_store(user_id: str):
    return Chroma(
        collection_name=f"user_{user_id}",
        embedding_function=_embeddings,
        persist_directory="./chroma_db",
        )
