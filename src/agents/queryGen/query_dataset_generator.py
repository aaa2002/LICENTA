import json
import random

SAMPLE_ENTITIES = {
    'technology': ['machine learning', 'AI', 'deep learning', 'NLP', 'blockchain'],
    'organizations': ['OpenAI', 'Google', 'Meta', 'Tesla'],
    'people': ['Elon Musk', 'Yann LeCun', 'Andrew Ng'],
}

TEMPLATE_QUERIES = {
    'google': lambda es: ' AND '.join([f'"{e}"' for e in es]),
    'bing': lambda es: ' OR '.join([f'"{e}"' for e in es]),
    'duckduckgo': lambda es: '(' + ' OR '.join([f'"{e}"' for e in es]) + ')'
}


def generate_examples(num=1000):
    examples = []
    for i in range(num):
        category = random.choice(list(SAMPLE_ENTITIES.keys()))
        entities = random.sample(SAMPLE_ENTITIES[category], random.randint(1, 3))

        queries = {k: fn(entities) for k, fn in TEMPLATE_QUERIES.items()}
        examples.append({
            'input': ', '.join(entities),
            'target': queries['google']  # you can change to other engines
        })
    return examples


def save_dataset(path='query_generation_dataset.json', num=1000):
    data = generate_examples(num)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} examples to {path}")
