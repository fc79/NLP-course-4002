import requests
import os

file_path = os.path.dirname(__file__)
os.chdir(file_path)

url = 'http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv'
print("Downloading quora-question-pairs data ...")
response = requests.get(url)

try:
    os.mkdir(os.path.join('..', '..', 'data', 'raw'))
except FileExistsError:
    pass

with open(os.path.join('..', '..', 'data', 'raw', 'quora-question-pairs.tsv'), 'wb') as file:
    file.write(response.content)
