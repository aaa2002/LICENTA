import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from query_dataset_loader import QueryGenerationDataset
from query_dataset_generator import save_dataset

save_dataset()

# Load dataset
with open('query_generation_dataset.json') as f:
    raw_data = json.load(f)

split = int(0.8 * len(raw_data))
train_data, val_data = raw_data[:split], raw_data[split:]

# Load tokenizer and model
model_name = 't5-small'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Prepare datasets
train_dataset = QueryGenerationDataset(train_data, tokenizer)
val_dataset = QueryGenerationDataset(val_data, tokenizer)

# Training setup
args = TrainingArguments(
    output_dir='./query-generator',
    do_eval=True,
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    save_total_limit=1,
    save_steps=500,
    eval_steps=500
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

trainer.train()

trainer.save_model("querygen_model")  # or any custom path
tokenizer.save_pretrained("querygen_model")
