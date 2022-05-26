# NLP-course-4002

## Setup
1. Create virtual environment

   `python3 -m venv venv`

2. Activate virtual environment

   `source venv/bin/activate`

3. Install requirements

   `pip install -r requirements.txt`

## Usage
Run `reproduce.py` to collect, preprocess and analyze data.

`python src/reproduce.py`

### Run collection script
Maximum crawling recursion can be configured using `MAX_DEPTH` variable.
Topics to start crawling from can also be configured using `TOPIC_URLS` variable.
`python src/data-collection/crawl-quora-texts.py`

Downloading quora question pairs dataset is pretty much straightforward.

`python src/data-collection/download-quora-question-pairs.py`


### Run individual preprocessing steps:
Each step of data preprocessing c`an be done individually.
Run preprocessing code using arguments below to perform preprocessing steps independently:

| Argument |          Preprocessing step           |
|----------|:-------------------------------------:|
| -l       |     Convert strings to lowercase      |
| -d       |         Remove duplicate data         |
| -p       | Remove punctuatuon and special tokens |
| -t       |             Tokenize data             |  
| -s       |           Remove stopwords            |

Code below will run lower-casing and tokenization steps on question-texts data:

`python src/preprocess/preprocess-quora-texts.py -lt
`

### Run analyze script
`python src/analyze/analyze-quora-texts.py`