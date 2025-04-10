# orchestrator.py
from agents.classic import FakeNewsAgent
from agents.wiki_check import WikiAgent
from agents.coherence import CoherenceAgent

if __name__ == "__main__":
    text = "Breaking news: Aliens have landed in Times Square to discuss trade deals."

    fake_news_agent = FakeNewsAgent()
    fn_result = fake_news_agent.analyze(text)

    wiki_agent = WikiAgent()
    wiki_result = wiki_agent.analyze(text)

    coherence_agent = CoherenceAgent()
    coherence_result = coherence_agent.analyze(text)

    print("\nFake News Analysis Result:")
    print(fn_result)

    print("\nWikipedia Knowledge Result:")
    print(wiki_result)

    print("\nText Coherence Analysis Result:")
    print(coherence_result)
