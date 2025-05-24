from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda, RunnableMap, RunnableBranch
from LangChainTools import (
    detect_fake_news,
    wiki_lookup,
    scrape_web,
    check_coherence
)
from aggregator import Aggregator

# coherence check including original input
def coherence_step_with_passthrough(input_data):
    result = check_coherence.invoke(input_data)
    return {"coherence_result": result, "original_input": input_data}

# Branch on coherence result
def should_continue(result):
    print(result["coherence_result"])
    return result["coherence_result"]["label"].lower() == "real"

# Step 3: Tools runner
def run_tools_with_original_input(data):
    original_input = data["original_input"]
    return RunnableMap({
        "fn_result": detect_fake_news,
        "wiki_result": wiki_lookup,
        "scraper_result": scrape_web,
        "coherence_result": lambda _: data["coherence_result"],
    }).invoke(original_input)

branch = RunnableBranch(
    (should_continue, RunnableLambda(run_tools_with_original_input)),
    lambda _: {"error": "Input is incoherent. Aborting."}
)

def maybe_aggregate(output):
    if "error" in output:
        return output
    return Aggregator().invoke(output)

# Final pipeline
pipeline = RunnableLambda(coherence_step_with_passthrough) | branch | RunnableLambda(maybe_aggregate)
