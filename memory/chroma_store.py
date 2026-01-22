from langchain import PromptTemplate, LLMChain
from langchain.llms import Ollama

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["session_text"],
    template=(
        "Summarize the following session into a short cognitive memory. "
        "Focus on recurring thoughts, emotions, and coping attempts.\n"
        "Session:\n{session_text}"
    ),
)


class MemorySummarizer:
    def __init__(self, model: str):
        self.llm = Ollama(model=model)
        self.chain = LLMChain(llm=self.llm, prompt=SUMMARY_PROMPT)

    def summarize(self, session_text: str) -> str:
        return self.chain.run(session_text=session_text)
