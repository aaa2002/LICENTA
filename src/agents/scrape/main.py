from src.agents.scrape.pipeline import main_pipeline

class ScraperAgent:
    def __init__(self):
        pass

    def analyze(self, claim, web_text=None):
        print(f"[LOG] --- [main.py] - Analyzing claim: {claim}")
        result = main_pipeline(claim, web_text=web_text, logging=False)
        return result