from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from chains.parallel_chain import parallel_chain
from chains.conditional_chain import conditional_chain
from agents.strategist_agent import strategist_agent
from agents.responder_agent import responder_agent
from agents.tracker_agent import tracker_agent
from memory.user_memory import memory_retriever, memory_writer


master_chain = (
RunnablePassthrough()
| parallel_chain
| RunnablePassthrough.assign(decision=conditional_chain)
| RunnableBranch(
(lambda x: x["decision"] == "ESCALATE", lambda x: "Contact emergency help"),
(
lambda x: True,
RunnablePassthrough.assign(
memory=memory_retriever(),
strategy=strategist_agent,
)
| RunnablePassthrough.assign(response=responder_agent)
| tracker_agent
| memory_writer()
| (lambda x: x["response"]),
),
)
)