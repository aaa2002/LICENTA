from langchain_core.tools import tool

from agents.classic.classic_agent import StreamingFakeNewsAgent
from agents.wiki_check import WikiAgent
from agents.coherence import CoherenceAgent
from take2.agents.scrape.main import ScraperAgent

fake_news_agent = StreamingFakeNewsAgent()
wiki_agent = WikiAgent()
coherence_agent = CoherenceAgent()
scraper_agent = ScraperAgent()

@tool
def check_coherence(text: str) -> dict:
    """Analyze the coherence of the given text and return a label and confidence."""
    return coherence_agent.analyze(text)

@tool
def detect_fake_news(text: str) -> dict:
    """Analyze the input text for fake news likelihood."""
    return fake_news_agent.analyze(text)

@tool
def wiki_lookup(text: str) -> dict:
    """Check Wikipedia for related information to support or refute the text."""
    return wiki_agent.analyze(text)

@tool
def scrape_web(text: str) -> dict:
    """Scrape the web to gather external sources related to the input text."""
    return scraper_agent.analyze(text)
