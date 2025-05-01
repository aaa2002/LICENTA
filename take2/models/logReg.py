from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import pandas as pd
import numpy as np

# Load and concatenate data
df_fake = pd.read_csv("../filtered/filtered_fake.csv")
df_real = pd.read_csv("../filtered/filtered_real.csv")
df = pd.concat([df_fake, df_real], ignore_index=True)

# Drop empty/null text
df = df.dropna(subset=["text"])
df = df[df["text"].str.strip().astype(bool)]

# Convert numeric labels to meaningful strings
df['truth'] = df['truth'].map({0: 'fake', 1: 'real'})

# Verify data balance
print("\n=== Data Balance ===")
print(df["truth"].value_counts(normalize=True))

# Features and labels
X = df["text"]
y = df["truth"]

# Label encoding
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("\n=== Label Encoding ===")
print(f"Classes: {label_encoder.classes_}")
print(f"'fake' → {label_encoder.transform(['fake'])[0]}")
print(f"'real' → {label_encoder.transform(['real'])[0]}")

# Vectorize text using TF-IDF
vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=10000,
    ngram_range=(1, 2)
)

# Transform text
X_vectorized = vectorizer.fit_transform(X)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train the model
model = LogisticRegression(
    class_weight='balanced',
    max_iter=1000,
    random_state=42,
    solver='liblinear'
)

print("\n=== Training Model ===")
model.fit(X_train, y_train)

# Evaluate
print("\n=== Training Evaluation ===")
train_pred = model.predict(X_train)
print(classification_report(y_train, train_pred, target_names=label_encoder.classes_))

print("\n=== Test Evaluation ===")
test_pred = model.predict(X_test)
print(classification_report(y_test, test_pred, target_names=label_encoder.classes_))

# Save model components
joblib.dump(vectorizer, "../model/tfidf_vectorizer.joblib")
joblib.dump(model, "../model/fake_news_model.joblib")
joblib.dump(label_encoder, "../model/label_encoder.joblib")

print("\nModel components saved successfully!")