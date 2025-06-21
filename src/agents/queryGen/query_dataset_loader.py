from torch.utils.data import Dataset

class QueryGenerationDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=256):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        input_enc = self.tokenizer(
            item['input'], padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        target_enc = self.tokenizer(
            item['target'], padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')

        return {
            'input_ids': input_enc['input_ids'].squeeze(),
            'attention_mask': input_enc['attention_mask'].squeeze(),
            'labels': target_enc['input_ids'].squeeze()
        }
