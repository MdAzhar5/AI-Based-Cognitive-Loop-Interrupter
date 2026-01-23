from langchain_core.runnables import RunnableParallel
from agents.pattern_agent import pattern_agent
from agents.safety_agent import safety_agent


parallel_chain = RunnableParallel(
pattern=pattern_agent,
safety=safety_agent,
)