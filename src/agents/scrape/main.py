from take2.agents.scrape.pipeline import main_pipeline

class ScraperAgent:
    def __init__(self):
        pass

    def analyze(self, claim):
        print(f"[LOG] Analyzing claim: {claim}")
        result = main_pipeline(claim, False)
        return result