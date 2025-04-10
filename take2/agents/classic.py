import joblib

class FakeNewsAgent:
    def __init__(self, vectorizer_path="/home/aaa/uni/LICENTA/AGENTIC/take2/model/tfidf_vectorizer.joblib",
                 model_path="/home/aaa/uni/LICENTA/AGENTIC/take2/model/fake_news_model.joblib"):
        self.vectorizer = joblib.load(vectorizer_path)
        self.model = joblib.load(model_path)

    def analyze(self, text):
        X = self.vectorizer.transform([text])
        prob = self.model.predict_proba(X)[0][1]
        label = "REAL" if prob > 0.5 else "FAKE"
        return {
            "label": label,
            "confidence": round(prob if label == "REAL" else 1 - prob, 3)
        }