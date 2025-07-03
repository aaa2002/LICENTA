import pandas as pd
import json
from sklearn.model_selection import train_test_split
from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments
)
from datasets import Dataset
import joblib

df = pd.read_csv("./queries_train.csv")
df["target"] = df.apply(
    lambda r: json.dumps({
        "google": r["google"],
        "bing": r["bing"],
        "duckduckgo": r["duckduckgo"]
    }),
    axis=1
)

train_df, val_df = train_test_split(
    df[["input", "target"]],
    test_size=0.1,
    random_state=42
)

train_ds = Dataset.from_pandas(train_df.reset_index(drop=True))
val_ds   = Dataset.from_pandas(val_df.reset_index(drop=True))

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model     = T5ForConditionalGeneration.from_pretrained("t5-small")

def preprocess(batch):
    inputs = tokenizer(
        ["generate queries: " + t for t in batch["input"]],
        truncation=True,
        padding="max_length",
        max_length=64
    )
    outputs = tokenizer(
        batch["target"],
        truncation=True,
        padding="max_length",
        max_length=64
    )
    batch["input_ids"]      = inputs.input_ids
    batch["attention_mask"] = inputs.attention_mask
    batch["labels"]         = outputs.input_ids
    return batch

train_ds = train_ds.map(
    preprocess,
    batched=True,
    remove_columns=["input", "target"]
)
val_ds   = val_ds.map(
    preprocess,
    batched=True,
    remove_columns=["input", "target"]
)

training_args = Seq2SeqTrainingArguments(
    output_dir="./querygen_model",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    predict_with_generate=True,
    logging_steps=500,
    save_steps=1000,
    eval_steps=1000,
    num_train_epochs=3,
    save_total_limit=2,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    tokenizer=tokenizer
)

trainer.train()

model.save_pretrained("./querygen_model")
tokenizer.save_pretrained("./querygen_model")

joblib.dump(model, "./querygen_model.joblib")
