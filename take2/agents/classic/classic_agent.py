import joblib
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer


class StreamingFakeNewsAgent:
    def __init__(self,
                 vectorizer_path="./agents/classic/saved_models/hashing_vectorizer.joblib",
                 model_path="./agents/classic/saved_models/online_fake_news_model.joblib",
                 encoder_path="./agents/classic/saved_models/label_encoder.joblib"):

        try:
            # Load components
            self.vectorizer = joblib.load(vectorizer_path)
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(encoder_path)

            # Verify components
            if not isinstance(self.vectorizer, HashingVectorizer):
                raise ValueError("Vectorizer must be HashingVectorizer for streaming")
            if not hasattr(self.model, 'partial_fit'):
                raise ValueError("Model must support partial_fit for streaming")

        except Exception as e:
            raise RuntimeError(f"Initialization failed: {str(e)}")

    def analyze(self, text):
        """Analyze text with streaming-compatible prediction"""
        try:
            X = self.vectorizer.transform([text])
            proba = self.model.predict_proba(X)[0]

            label_idx = np.argmax(proba)
            label = self.label_encoder.inverse_transform([label_idx])[0]

            return {
                'label': label,
                'confidence': float(proba[label_idx]),
                'probabilities': {
                    'fake': float(proba[0]),
                    'real': float(proba[1])
                }
            }
        except Exception as e:
            return {
                'error': str(e),
                'label': 'error',
                'confidence': 0.0
            }

    def update(self, text, true_label):
        """Update model with new streaming data"""
        try:
            # Normalize true_label
            if str(true_label) in ['0', '1']:
                true_label = 'fake' if str(true_label) == '0' else 'real'

            # Transform input
            X = self.vectorizer.transform([text])
            y = self.label_encoder.transform([true_label])

            # Dynamically get class list
            class_labels = list(self.label_encoder.transform(self.label_encoder.classes_))
            class_labels = sorted(set(class_labels))  # Ensure no weird order

            # Online learning update
            self.model.partial_fit(X, y, classes=class_labels)

            # Save updated model
            joblib.dump(self.model, "./agents/classic/saved_models/online_fake_news_model.joblib")

            return True

        except Exception as e:
            print(f"Update error: {str(e)}")
            print(f"True label (raw): {true_label}")
            print(f"Transformed y: {y}")
            print(f"Classes used: {class_labels}")
            return False

    def batch_update(self, texts, labels):
        """Update model with a batch of new data"""
        try:
            # Convert labels
            labels = [('fake' if str(l) in ['0', 'fake'] else 'real') for l in labels]

            X = self.vectorizer.transform(texts)
            y = self.label_encoder.transform(labels)

            # Online batch update
            self.model.partial_fit(X, y, classes=[0, 1])

            # Save updated model
            joblib.dump(self.model, "./saved_models/online_fake_news_model.joblib")

            return True
        except Exception as e:
            print(f"Batch update error: {str(e)}")
            return False