from langchain.schema.runnable import RunnableLambda


conditional_chain = RunnableLambda(
lambda x: "ESCALATE" if "yes" in x["safety"].lower() else "CONTINUE"
)