from langchain_core.runnables import RunnableLambda, RunnableMap
from LangChainTools import (
    detect_fake_news,
    wiki_lookup,
    scrape_web,
    check_coherence
)
from aggregator import Aggregator

# Run all tools in parallel (same input to each)
parallel_tools = RunnableMap({
    "fn_result": detect_fake_news,
    "wiki_result": wiki_lookup,
    "scraper_result": scrape_web,
    "coherence_result": check_coherence
})

# Aggregate all results
pipeline = parallel_tools | RunnableLambda(Aggregator().invoke)
