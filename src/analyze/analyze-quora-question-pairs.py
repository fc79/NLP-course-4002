from collections import Counter
import matplotlib.pyplot as plt
import os

import nltk
import pandas as pd

file_path = os.path.dirname(__file__)
os.chdir(file_path)

BASE_DATA_PATH = os.path.join('..', '..', 'data')
DATA_NAME = 'quora-question-pairs'

try:
    data = pd.read_pickle(os.path.join(BASE_DATA_PATH, 'no_stopwords', f'{DATA_NAME}.pk'))
except FileNotFoundError:
    data = None
    print('Preprocessing incomplete. run preprocessing (at least with -s) to analyze data')

if data is not None:
    data = data.loc[:, ['question1_no_stopwords', 'question2_no_stopwords', 'question1', 'question2']]

    # Count number of sentences
    sentences = [nltk.sent_tokenize(text) for text in data['question1'] + data['question2']]
    sentences_count = sum([len(i) for i in sentences])
    print(f'Number of all sentences [{DATA_NAME}]: {sentences_count}')


    # Count words
    words = [word for words_list in data['question1_no_stopwords'] + data['question2_no_stopwords'] for word in words_list]
    words_count = len(words)
    print(f'Number of all words (tokens) [{DATA_NAME}]: {words_count}')

    # Count unique words
    unique_words_counts = Counter(words)
    print(f" Number of unique words [{DATA_NAME}]: {len(unique_words_counts)}")

    # Visualizing most common words in data
    most_common_word_counts = unique_words_counts.most_common(15)
    most_common_words = [i[0] for i in most_common_word_counts]
    most_common_counts = [i[1] for i in most_common_word_counts]

    plt.bar(most_common_words, most_common_counts)
    plt.xticks(rotation=90)
    plt.title(f'Most common words in {DATA_NAME}')
    plt.xlabel("Words")
    plt.ylabel("Occurrence")
    plt.show()

    try:
        os.mkdir(os.path.join(BASE_DATA_PATH, 'word_count_plots'))
    except FileExistsError:
        pass
    plt.savefig(os.path.join(BASE_DATA_PATH, 'word_count_plots', f'{DATA_NAME}.png'))
