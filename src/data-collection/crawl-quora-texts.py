import os
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


file_path = os.path.dirname(__file__)
os.chdir(file_path)


def connect_chrome():
    print('Creating webdriver')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    time.sleep(2)
    return driver


def scroll_down(browser):
    # scroll down and wait until page does not change after 3 scrolls
    last_height = browser.page_source
    loop_scroll = True
    attempt = 0
    print('scrolling down to get all answers...')
    while loop_scroll:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = browser.page_source
        if new_height == last_height:
            attempt += 1
            if attempt == 3:  # in the third attempt we end the scrolling
                loop_scroll = False
        else:
            attempt = 0
        last_height = new_height


def crawl_question_page(browser, url, depth, step_number):
    print(f'Step #{step_number} href {url}')
    try:
        try:
            browser.get(url)
            time.sleep(QUESTION_PAGE_WAIT_TIME)
        except:
            print(f'Question page not found {url}')
            return set(), step_number

        html_source = browser.page_source
        related_questions_soup = BeautifulSoup(html_source, 'html.parser')
        related_questions = related_questions_soup.find_all('a', {
            'class': 'q-box qu-display--block qu-cursor--pointer qu-hover--textDecoration--none Link___StyledBox-t2xg9c-0 KlcoI'})

        urls_to_crawl = set()

        for related in related_questions:
            related_url = related.attrs.get('href')
            related_text = related.find_all('span', {'style': 'background: none;'})
            if related_text:
                urls_to_crawl.add((related_url,
                                   related_text[0].contents[0],
                                   url))
        related_crawled = urls_to_crawl.copy()
        if depth < MAX_DEPTH:
            for data in urls_to_crawl:
                crawl_result, step_number = crawl_question_page(browser, data[0], depth + 1, step_number + 1)
                related_crawled.update(crawl_result)
        return related_crawled, step_number
    except Exception as e:
        print(step_number, depth, url, e)
        return set(), step_number


TOPIC_URLS = ['https://www.quora.com/topic/Intelligence',
              'https://www.quora.com/topic/High-Level-IQ',
              'https://www.quora.com/topic/Smart-People',
              'https://www.quora.com/topic/Stupidity',
              'https://www.quora.com/topic/Genius-and-Geniuses',

              'https://www.quora.com/topic/Intelligence-Quotient',
              'https://www.quora.com/topic/IQ-Testing',
              'https://www.quora.com/topic/Understanding-Smart-People',
              'https://www.quora.com/topic/Emotional-Intelligence',

              'https://www.quora.com/topic/Computer-Science',
              'https://www.quora.com/topic/Data-Science',
              'https://www.quora.com/topic/Data-Mining',
              'https://www.quora.com/topic/Classification-machine-learning',
              'https://www.quora.com/topic/Data-Analysis',
              'https://www.quora.com/topic/Computer-Vision',
              'https://www.quora.com/topic/Algorithms',
              'https://www.quora.com/topic/Artificial-Intelligence',
              'https://www.quora.com/topic/Machine-Learning',
              'https://www.quora.com/topic/Deep-Learning',
              'https://www.quora.com/topic/Artificial-Neural-Networks',
              'https://www.quora.com/topic/Artificial-General-Intelligence',

              'https://www.quora.com/topic/Mobile-Technology',
              'https://www.quora.com/topic/Cellular-Service-Providers',
              'https://www.quora.com/topic/Smartphones',
              'https://www.quora.com/topic/Telephones',
              'https://www.quora.com/topic/Phone-Hacking',
              'https://www.quora.com/topic/Cell-Phone-Hacking',
              'https://www.quora.com/topic/Mobile-Hacking',
              'https://www.quora.com/topic/Technology',
              'https://www.quora.com/topic/Espionage-and-Spying',

              'https://www.quora.com/topic/Vegetables',
              'https://www.quora.com/topic/Healthy-Fruit',
              'https://www.quora.com/topic/Fruit-Identification',
              'https://www.quora.com/topic/Vegetable-Gardening',
              'https://www.quora.com/topic/Apple-company',
              'https://www.quora.com/topic/Apple-Products-and-Services',
              'https://www.quora.com/topic/Apples-fruit',

              'https://www.quora.com/topic/Football-Players-soccer',
              'https://www.quora.com/topic/American-Football',
              'https://www.quora.com/topic/Association-Football-1',
              'https://www.quora.com/topic/FIFA-World-Cup',

              'https://www.quora.com/topic/Professional-Wrestling-1',
              'https://www.quora.com/topic/Professional-Wrestlers',
              'https://www.quora.com/topic/WWE-Raw-46',

              'https://www.quora.com/topic/Equality-society',
              'https://www.quora.com/topic/Gender-Relations',
              'https://www.quora.com/topic/Feminism',
              'https://www.quora.com/topic/Gender',
              'https://www.quora.com/topic/Gender-Inequality',
              'https://www.quora.com/topic/Equal-Rights',
              'https://www.quora.com/topic/Sexism',
              'https://www.quora.com/topic/Feminists',
              'https://www.quora.com/topic/Gender-Differences'
              ]

MAX_DEPTH = 3
TOPIC_PAGE_WAIT_TIME = 2
QUESTION_PAGE_WAIT_TIME = 2
SAVE_PATH = os.path.join('..', '..', 'data')

if __name__ == '__main__':
    question_urls = set()

    browser = connect_chrome()

    for url in TOPIC_URLS:
        print('Crawling topic url: ', url)

        try:
            browser.get(url)
            time.sleep(TOPIC_PAGE_WAIT_TIME)
        except Exception as e0:
            print(f'Topic does not exist in Quora.\n{e0}')
            continue

        scroll_down(browser)

        html_source = browser.page_source
        question_count_soup = BeautifulSoup(html_source, 'html.parser')
        all_question_htmls = question_count_soup.find_all('div', {
            'class': 'q-box qu-borderAll qu-borderRadius--small qu-borderColor--raised qu-boxShadow--small qu-mb--small qu-bg--raised'})

        question_count = len(all_question_htmls)
        print(f"Found {question_count} questions for topic {url}")

        if question_count is None:
            print('topic does not have questions...')
            continue
        if question_count == 0:
            print('topic does not have questions...')

        for question_card in all_question_htmls[:10]:
            question_url = question_card.find_all('a', {
                'class': 'q-box qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 KlcoI'})
            if question_url:
                question_text = question_url[0].find_all('span', {'style': 'background: none;'})
                if question_text:
                    question_urls.add((question_url[0].attrs.get('href'),
                                       question_text[0].contents[0],
                                       url))
    step = 0
    result = question_urls.copy()
    for data in question_urls:
        child_result, step = crawl_question_page(browser, data[0], 1, step + 1)
        result.update(child_result)

    json_result = []
    for url, text, parent in result:
        json_result.append({
            'url': url,
            'text': text,
            'parent': parent
        })
    browser.quit()
    try:
        os.mkdir(os.path.join(SAVE_PATH, 'raw'))
    except FileExistsError:
        pass
    with open(os.path.join(SAVE_PATH, 'raw', 'quora-texts.json'), 'w') as out_file:
        json.dump(json_result, out_file)
