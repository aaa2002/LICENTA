from langchain_core.runnables import RunnableLambda
from LangChainTools import (
    detect_fake_news,
    wiki_lookup,
    scrape_web,
    check_coherence, delta_search
)
from aggregator import Aggregator

pipeline = (
    RunnableLambda(lambda x: {"data": {"input": x["text"]}})
    | RunnableLambda(lambda d: delta_search.invoke(d))
    | RunnableLambda(lambda d: {
        **d,
        "fn_result": detect_fake_news.invoke({"data": {
            "input": d["input"],
            "web_text": d.get("web_text", "")
        }})
    })
    | RunnableLambda(lambda d: {
        **d,
        "wiki_result": wiki_lookup.invoke({"data": {
            "input": d["input"],
            "web_text": d.get("web_text", "")
        }})
    })
    | RunnableLambda(lambda d: {
        **d,
        "scraper_result": scrape_web.invoke({"data": {
            "input": d["input"],
            "web_text": d.get("web_text", "")
        }})
    })
    | RunnableLambda(lambda d: {
        **d,
        "coherence_result": check_coherence.invoke({"data": {
            "input": d["input"],
            "web_text": d.get("web_text", "")
        }})
    })
    | RunnableLambda(Aggregator().invoke)
)
