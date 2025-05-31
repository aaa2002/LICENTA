from src.agents.get_web.get_web import get_top_k_results_delta

def delta_search_step(d):
    question = d["input"]
    search_results, web_text = get_top_k_results_delta(question, k=10)
    return {
        **d,
        "search_results": search_results,
        "web_text": web_text
    }
