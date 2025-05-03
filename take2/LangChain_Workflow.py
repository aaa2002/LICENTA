from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableMap, RunnableBranch
from LangChainTools import (
    detect_fake_news,
    wiki_lookup,
    scrape_web,
    check_coherence
)
from aggregator import Aggregator

# Step 1: Check Coherence
coherence_step = check_coherence

# Step 2: Branch on coherence result
def should_continue(result):
    return result["label"].lower() == "real"

branch = RunnableBranch(
    (should_continue, RunnableMap({
        "fn_result": detect_fake_news,
        "wiki_result": wiki_lookup,
        "scraper_result": scrape_web,
        "coherence_result": lambda x: x,
    })),
    lambda _: {"error": "Input is incoherent. Aborting."}  # ← This must not be in a tuple
)

def maybe_aggregate(output):
    if "error" in output:
        return output
    return Aggregator().invoke(output)

pipeline = coherence_step | branch | RunnableLambda(maybe_aggregate)