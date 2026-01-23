from langchain_core.runnables import RunnableLambda
from llm.ollama import get_llm

llm = get_llm()

safety_agent = (
RunnableLambda(lambda x: f"Is this unsafe? yes/no: {x['input']}")
| llm
)