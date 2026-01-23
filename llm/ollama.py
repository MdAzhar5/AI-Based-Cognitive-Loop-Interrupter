from langchain_ollama import ChatOllama


def get_llm():
    return ChatOllama(model="gpt-oss:20b-cloud")