from langchain.schema.runnable import RunnableLambda
from llm.ollama import get_llm


llm = get_llm()


strategist_agent = (
RunnableLambda(
lambda x: f"Given pattern {x['pattern']}, choose therapy strategy"
)
| llm
)