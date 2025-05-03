from langchain_core.runnables import Runnable

def label_to_bool(label):
    return 1 if label.lower() == 'real' else 0

def float_to_label(value):
    return 'real' if value >= 0.5 else 'fake'

class Aggregator(Runnable):
    def invoke(self, input: dict, config=None) -> dict:
        fn = input["fn_result"]
        wiki = input["wiki_result"]
        scraper = input["scraper_result"]
        coherence = input["coherence_result"]

        avg_score = sum([
            label_to_bool(fn["label"]) * fn["confidence"],
            label_to_bool(wiki["label"]) * wiki["confidence"],
            label_to_bool(scraper["label"]) * scraper["confidence"],
            label_to_bool(coherence["label"]) * coherence["confidence"]
        ]) / 4

        return {
            "final_label": float_to_label(avg_score),
            "score": avg_score
        }
