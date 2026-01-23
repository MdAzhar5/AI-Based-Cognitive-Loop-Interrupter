from langchain_core.runnables import RunnableLambda
from memory.chroma_store import get_user_store




def memory_retriever():
    def _retrieve(input):
        store = get_user_store(input["user_id"])
        docs = store.similarity_search(input["input"], k=3)
        return "\n".join([d.page_content for d in docs])
    return RunnableLambda(_retrieve)

def memory_writer():
    def _write(input):
        store = get_user_store(input["user_id"])
        store.add_texts([input["summary"]])
        return input
    return RunnableLambda(_write)