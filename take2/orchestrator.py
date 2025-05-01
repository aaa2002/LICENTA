from agents.classic.classic_agent import StreamingFakeNewsAgent
from agents.wiki_check import WikiAgent
from agents.coherence import CoherenceAgent
from take2.agents.scrape.main import ScraperAgent

def label_to_bool(label):
    if str(label).lower() in ['fake', '0']:
        return 0
    elif str(label).lower() in ['real', '1']:
        return 1
    else:
        raise ValueError("Label must be 'fake' or 'real'.")

def float_to_label(float_value):
    if float_value < 0.5:
        return 'fake'
    else:
        return 'real'

if __name__ == "__main__":
    text = "Breaking news: Aliens have landed in Times Square to discuss trade deals."

    fake_news_agent = StreamingFakeNewsAgent()
    fn_result = fake_news_agent.analyze(text)

    wiki_agent = WikiAgent()
    wiki_result = wiki_agent.analyze(text)

    coherence_agent = CoherenceAgent()
    coherence_result = coherence_agent.analyze(text)

    scraper_agent = ScraperAgent()
    scraper_result = scraper_agent.analyze(text)

    print("\nFake News Analysis Result:")
    print(fn_result)

    print("\nWikipedia Knowledge Result:")
    print(wiki_result)

    print("\nText Coherence Analysis Result:")
    print(coherence_result)

    print("\nScraper Analysis Result:")
    print(scraper_result)

    # Result Aggregation
    final_result = {
        "fake_news": fn_result,
        "wiki": wiki_result,
        "coherence": coherence_result,
        "scraper": scraper_result
    }

    final_wighted_result = (label_to_bool(fn_result["label"]) * fn_result["confidence"]
                            + label_to_bool(wiki_result["label"]) * wiki_result["confidence"]
                            + label_to_bool(coherence_result["label"]) * coherence_result["confidence"]
                            + label_to_bool(scraper_result["label"]) * scraper_result["confidence"]) / 4

    print("\nFinal Result:")
    print(float_to_label(final_wighted_result))