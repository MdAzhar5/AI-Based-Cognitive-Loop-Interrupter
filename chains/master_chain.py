from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch
from agents.safety_agent import PatternDetectorAgent
from agents.pattern_agent import SafetyGuardAgent
from agents.strategist_agent import ClinicalStrategistAgent
from agents.responder_agent import ReflectiveResponderAgent
from agents.tracker_agent import OutcomeTrackerAgent
from memory.memory_summarizer import MemorySummarizer

# -------- Agent wrappers (Runnables) --------
pattern_runnable = RunnableLambda(
    lambda x: PatternDetectorAgent().run(x["user_id"], x["input"])
)

safety_runnable = RunnableLambda(
    lambda x: SafetyGuardAgent().run(x["input"])
)

strategy_runnable = RunnableLambda(
    lambda x: ClinicalStrategistAgent().run(x["pattern"], x["input"])
)

response_runnable = RunnableLambda(
    lambda x: ReflectiveResponderAgent().run(
        x["user_id"], x["strategy"], x["input"]
    )
)

memory_runnable = RunnableLambda(
    lambda x: OutcomeTrackerAgent().run(
        x["user_id"],
        MemorySummarizer().summarize(x["input"] + " " + x["response"]),
    )
)

# -------- Parallel detection --------
detection_parallel = RunnableParallel(
    pattern=pattern_runnable,
    safety=safety_runnable,
)

# -------- Conditional routing --------
branch = RunnableBranch(
    (
        lambda x: "true" in x["safety"].lower(),
        RunnableLambda(
            lambda _: "I’m really concerned about your safety. Please contact local emergency services or a trusted person immediately."
        ),
    ),
    RunnableLambda(lambda x: x),
)

# -------- Sequential therapeutic pipeline --------
therapeutic_chain = (
    RunnableLambda(lambda x: {**x, "strategy": strategy_runnable.invoke(x)})
    | RunnableLambda(lambda x: {**x, "response": response_runnable.invoke(x)})
    | RunnableLambda(lambda x: (memory_runnable.invoke(x), x["response"]))
    | RunnableLambda(lambda x: x[1])
)

# -------- Master Runnable Chain --------
MasterRunnableChain = (
    detection_parallel
    | branch
    | RunnableLambda(
        lambda x: x
        if isinstance(x, str)
        else therapeutic_chain.invoke(x)
    )
)

# Example invocation:
# MasterRunnableChain.invoke({"user_id": "azhar_0300", "input": "I feel stuck in the same thoughts"})