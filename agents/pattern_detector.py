from langchain_core.runnables import RunnableLambda
from llm.ollama import get_llm


llm = get_llm()


pattern_agent = (
RunnableLambda(lambda x: f"Detect thinking pattern: {x['input']}")
| llm
)