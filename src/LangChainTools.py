from langchain_core.tools import tool

from agents.classic.classic_agent import StreamingFakeNewsAgent
from agents.wiki_check import WikiAgent
from agents.coherence import CoherenceAgent
from src.agents.scrape.main import ScraperAgent
from src.agents.get_web.get_web import get_top_k_results_delta

fake_news_agent = StreamingFakeNewsAgent()
wiki_agent = WikiAgent()
coherence_agent = CoherenceAgent()
scraper_agent = ScraperAgent()

@tool
def delta_search(data: dict) -> dict:
    """
    Perform a web search and return top results and concatenated text.
    Accepts a dict with 'input' text.
    """
    input_text = data.get("input", "")
    search_results, web_text = get_top_k_results_delta(input_text, k=5)
    return {
        **data,
        "search_results": search_results,
        "web_text": web_text
    }

@tool
def detect_fake_news(data: dict) -> dict:
    """Analyze the input text for fake news likelihood."""
    input_text = data.get("input", "")
    web_text = data.get("web_text", "")
    return fake_news_agent.analyze(input_text, web_text=web_text)

@tool
def wiki_lookup(data: dict) -> dict:
    """Check Wikipedia for related information to support or refute the text."""
    input_text = data.get("input", "")
    web_text = data.get("web_text", "")
    return wiki_agent.analyze(input_text, web_text=web_text)

@tool
def check_coherence(data: dict) -> dict:
    """Analyze the coherence of the given text and return a label and confidence."""
    input_text = data.get("input", "")
    web_text = data.get("web_text", "")
    return coherence_agent.analyze(input_text, web_text=web_text)

@tool
def scrape_web(data: dict) -> dict:
    """Scrape the web to gather external sources related to the input text."""
    input_text = data.get("input", "")
    web_text = data.get("web_text", "")
    return scraper_agent.analyze(input_text, web_text=web_text)
