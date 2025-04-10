import os
import pandas as pd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Handle FAKE News Processing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

file_paths_fake = [
    '../../Datasets/Fake.csv',
    '../../Datasets/FakeNewsNet/BuzzFeed_fake_news_content.csv',
    '../../Datasets/FakeNewsNet/PolitiFact_fake_news_content.csv',
    '../../Datasets/Generated/fake_news_part_1.csv',
    '../../Datasets/Generated/fake_news_part_2.csv',
    '../../Datasets/Generated/fake_news_part_3.csv',
    '../../Datasets/Generated/fake_news_part_4.csv',
    '../../Datasets/Generated/fake_news_part_5.csv',
]

for file_path in file_paths_fake:
    print(f"{file_path} - {'File exists' if os.path.exists(file_path) else 'File does not exist'}")

output_file_fake = './filtered/filtered_fake.csv'
if os.path.exists(output_file_fake):
    os.remove(output_file_fake)

# File 1
input_file = '../../Datasets/Fake.csv'
df = pd.read_csv(input_file)
df_modified = df[['text']].copy()
df_modified['truth'] = 0

# File 2
input_file = '../../Datasets/FakeNewsNet/BuzzFeed_fake_news_content.csv'
df_temp = pd.read_csv(input_file)
df_temp = df_temp[['text']].copy()
df_temp['truth'] = 0
df_modified = pd.concat([df_modified, df_temp], ignore_index=True)

# File 3
input_file = '../../Datasets/FakeNewsNet/PolitiFact_fake_news_content.csv'
df_temp = pd.read_csv(input_file)
df_temp = df_temp[['text']].copy()
df_temp['truth'] = 0
df_modified = pd.concat([df_modified, df_temp], ignore_index=True)

# Files 4-8
for i in range(1, 6):
    input_file = f'../../Datasets/Generated/fake_news_part_{i}.csv'
    df_temp = pd.read_csv(input_file)
    df_temp = df_temp.rename(columns=str.lower)
    df_temp = df_temp[df_temp['truth'] == 0]
    df_temp = df_temp[['text', 'truth']]
    df_modified = pd.concat([df_modified, df_temp], ignore_index=True)

# Ensure column names are lowercase and correct
df_modified.columns = ['text', 'truth']
df_modified.to_csv(output_file_fake, index=False)
print(f"Fake News output: {output_file_fake}")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Handle REAL News Processing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

file_paths_real = [
    '../../Datasets/True.csv',
    '../../Datasets/FakeNewsNet/BuzzFeed_real_news_content.csv',
    '../../Datasets/FakeNewsNet/PolitiFact_real_news_content.csv',
    '../../Datasets/Generated/fake_news_part_1.csv',
    '../../Datasets/Generated/fake_news_part_2.csv',
    '../../Datasets/Generated/fake_news_part_3.csv',
    '../../Datasets/Generated/fake_news_part_4.csv',
    '../../Datasets/Generated/fake_news_part_5.csv',
]

for file_path in file_paths_real:
    print(f"{file_path} - {'File exists' if os.path.exists(file_path) else 'File does not exist'}")

output_file_real = './filtered/filtered_real.csv'
if os.path.exists(output_file_real):
    os.remove(output_file_real)

# File 1
input_file = '../../Datasets/True.csv'
df = pd.read_csv(input_file)
df_modified = df[['text']].copy()
df_modified['truth'] = 1

# File 2
input_file = '../../Datasets/FakeNewsNet/BuzzFeed_real_news_content.csv'
df_temp = pd.read_csv(input_file)
df_temp = df_temp[['text']].copy()
df_temp['truth'] = 1
df_modified = pd.concat([df_modified, df_temp], ignore_index=True)

# File 3
input_file = '../../Datasets/FakeNewsNet/PolitiFact_real_news_content.csv'
df_temp = pd.read_csv(input_file)
df_temp = df_temp[['text']].copy()
df_temp['truth'] = 1
df_modified = pd.concat([df_modified, df_temp], ignore_index=True)

# Files 4-8
for i in range(1, 6):
    input_file = f'../../Datasets/Generated/fake_news_part_{i}.csv'
    df_temp = pd.read_csv(input_file)
    df_temp = df_temp.rename(columns=str.lower)
    df_temp = df_temp[df_temp['truth'] == 1]
    df_temp = df_temp[['text', 'truth']]
    df_modified = pd.concat([df_modified, df_temp], ignore_index=True)

# Ensure column names are lowercase and correct
df_modified.columns = ['text', 'truth']
df_modified.to_csv(output_file_real, index=False)
print(f"Real News output: {output_file_real}")
