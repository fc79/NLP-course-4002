import os

file_path = os.path.dirname(__file__)
os.chdir(file_path)

try:
    os.mkdir(os.path.join('..', 'data'))
except FileExistsError:
    pass

os.system("python data-collection/download-quora-question-pairs.py")
os.system("python data-collection/crawl-quora-texts.py")

os.system("python preprocess/preprocess-quora-texts.py")
os.system("python preprocess/preprocess-quora-question-pairs.py")

os.system("python analyze/analyze-quora-texts.py")
os.system("python analyze/analyze-quora-question-pairs.py")
