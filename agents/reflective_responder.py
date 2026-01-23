from langchain_core.runnables import RunnableLambda
from llm.ollama import get_llm


llm = get_llm()


responder_agent = (
RunnableLambda(
lambda x: f"Respond using strategy {x['strategy']} and memory {x['memory']}"
)
| llm
)