import argparse

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
DATA_NAME = 'quora-question-pairs'
DATA_FILE_NAME = 'quora-question-pairs.tsv'

quora_question_pairs_data_filepath = os.path.join(BASE_DATA_PATH, 'raw', DATA_FILE_NAME)
data = pd.read_csv(quora_question_pairs_data_filepath, sep='\t')

print(f'Raw data count [{DATA_NAME}]: {len(data)}')

# As we only need question texts and label, we only use these columns
data = data.loc[:, ['question1', 'question2', 'is_duplicate']]

# drop null values
data = data.dropna()

if default or args.l:
    # Preprocessing step 1: Convert strings to lowercase
    print(f'Lowercasing {DATA_NAME}')
    data['question1_lower'] = [text.lower() for text in data['question1']]
    data['question2_lower'] = [text.lower() for text in data['question2']]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'lower'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'lower', f'{DATA_NAME}.pk'))

if default or args.d:
    # Preprocessing step 2: Remove duplicate data
    print(f'Removing duplicates from {DATA_NAME}')
    data = data.drop_duplicates()
    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'no_duplicate'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'no_duplicate', f'{DATA_NAME}.pk'))

if default or args.p:
    # Preprocessing step 3: remove punctuation and special tokens
    print(f'Removing punctuations and special tokens from {DATA_NAME}')
    pattern = re.compile('[^a-zA-Z\s]+')

    if 'question1_lower' in data.columns and 'question2_lower' in data.columns:
        source1 = data['question1_lower']
        source2 = data['question2_lower']
    else:
        source1 = data['question1']
        source2 = data['question2']

    data['question1_no_special'] = [re.sub(pattern, '', text) for text in source1]
    data['question2_no_special'] = [re.sub(pattern, '', text) for text in source2]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'no_special'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'no_special', f'{DATA_NAME}.pk'))

if default or args.t or args.s:
    # Preprocessing step 4: tokenize texts
    print(f'Tokenizing {DATA_NAME}')
    if 'question1_no_special' in data.columns and 'question2_no_special' in data.columns:
        source1 = data['question1_no_special']
        source2 = data['question2_no_special']
    elif 'question1_lower' in data.columns and 'question2_lower' in data.columns:
        source1 = data['question1_lower']
        source2 = data['question2_lower']
    else:
        source1 = data['question1']
        source2 = data['question2']

    data['question1_tokens'] = [nltk.word_tokenize(text) for text in source1]
    data['question2_tokens'] = [nltk.word_tokenize(text) for text in source2]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'tokenized'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'tokenized', f'{DATA_NAME}.pk'))

if default or args.s:
    # Preprocessing step 5: remove stopwords
    print(f'Removing stopwords from {DATA_NAME}')
    stopwords = nltk.corpus.stopwords.words('english')
    data['question1_no_stopwords'] = [[word for word in words_list if word not in stopwords] for words_list in data['question1_tokens']]
    data['question2_no_stopwords'] = [[word for word in words_list if word not in stopwords] for words_list in data['question2_tokens']]

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'no_stopwords'))
    except FileExistsError:
        pass
    data.to_pickle(os.path.join(BASE_DATA_PATH, 'no_stopwords', f'{DATA_NAME}.pk'))

print(data.columns)
