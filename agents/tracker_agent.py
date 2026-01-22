from langchain.schema.runnable import RunnableLambda


tracker_agent = RunnableLambda(
lambda x: {
"user_id": x["user_id"],
"summary": f"User said: {x['input']} | AI: {x['response']}"
}
)