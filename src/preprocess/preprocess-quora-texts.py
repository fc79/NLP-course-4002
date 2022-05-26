import argparse
import json
import pandas as pd
import nltk
import re
import os

file_path = os.path.dirname(__file__)
os.chdir(file_path)

parser = argparse.ArgumentParser()
parser.add_argument('-l', help='Convert texts to lower', action='store_true')
parser.add_argument('-d', help='Remove duplicate data', action='store_true')
parser.add_argument('-p', help='Remove punctuations and special tokens', action='store_true')
parser.add_argument('-t', help='Tokenize data', action='store_true')
parser.add_argument('-s', help='Remove stopwords', action='store_true')
args = parser.parse_args()
# If no arguments is passed, do all preprocessing steps
default = not args.l and not args.d and not args.p and not args.t and not args.s

BASE_DATA_PATH = os.path.join('..', '..', 'data')
DATA_NAME = 'quora-texts'
DATA_FILE_NAME = 'quora-texts.json'

quora_data_filepath = os.path.join(BASE_DATA_PATH, 'raw', DATA_FILE_NAME)
with open(quora_data_filepath, 'r') as file:
    data = json.load(file)

print(f'Raw data count [{DATA_NAME}]: {len(data)}')

# Convert json data to pandas DataFrame
data = pd.DataFrame(data)

if default or args.l:
    # Preprocessing step 1: Convert strings to lowercase
    print(f'Lowercasing {DATA_NAME}')

    data['lower'] = [string.lower() for string in data['text']]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'lower'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'lower', f'{DATA_NAME}.pk'))

if default or args.d:
    # Preprocessing step 2: Remove duplicate text
    print(f'Removing duplicates from {DATA_NAME}')

    data = data.drop_duplicates()

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'no_duplicate'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'no_duplicate', f'{DATA_NAME}.pk'))

if default or args.p:
    # Preprocessing step 3: Remove punctuation and special tokens
    print(f'Removing punctuations and special tokens from {DATA_NAME}')

    pattern = re.compile('[^a-zA-Z\s]+')

    if 'lower' in data.columns:
        source = data['lower']
    else:
        source = data['text']
    data['no_special'] = [re.sub(pattern, '', text) for text in source]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'no_special'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'no_special', f'{DATA_NAME}.pk'))

if default or args.t or args.s:

    # Preprocessing step 4: Tokenize texts
    print(f'Tokenizing {DATA_NAME}')

    if 'no_special' in data.columns:
        source = data['no_special']
    elif 'lower' in data.columns:
        source = data['lower']
    else:
        source = data['text']

    data['tokens'] = [nltk.word_tokenize(text) for text in source]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'tokenized'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'tokenized', f'{DATA_NAME}.pk'))

if default or args.s:
    # Preprocessing step 5: remove stopwords
    print(f'Removing stopwords from {DATA_NAME}')

    stopwords = nltk.corpus.stopwords.words('english')
    data['no_stopwords'] = [[word for word in words_list if word not in stopwords] for words_list in data['tokens']]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'no_stopwords'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'no_stopwords', f'{DATA_NAME}.pk'))

print(data.columns)