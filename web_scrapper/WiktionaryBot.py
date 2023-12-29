# SELENIUM IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import re

# SELENIUM VARIABLES
options = Options()
options.add_argument("--headless")
webdriver_service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=webdriver_service, options=options)


WIKTIONARY_LINK = 'https://en.wiktionary.org/wiki/'


class Wiktionary:
    def __init__(self, browser, By):
        self.browser = browser
        self.By = By
        self.data = None

    def get_page_data(self):
        page_data = self.browser.find_element(self.By.XPATH, "/html/body").text
        return page_data
    
    def open(self, latin_word):
        if latin_word:
            self.browser.get(WIKTIONARY_LINK + latin_word)

    def get_word_declination(self, word: str):
        self.open(latin_word=word)
        page_data = self.get_page_data()
        pattern = '([a-zA-Zīāōēū]+ [a-zA-Zīāōūē]+ [a-zA-Zīāōūē]+\n){7}'
        result = re.search(pattern, page_data)

        if result:
            return result.group()
        else:
            page_html_data = self.browser.page_source
            pattern = 'href="/wiki/[a-z]+#Latin"'
            result = re.search(pattern, page_html_data)

            if result:
                btn_selector = result.group()
                button = browser.find_element(self.By.XPATH, f'//a[@{btn_selector}]')
                button.click()
                page_data = self.get_page_data()
                pattern = '([a-zA-Zīāōēū]+ [a-zA-Zīāōūē]+ [a-zA-Zīāōūē]+\n){7}'
                result = re.search(pattern, page_data)
                if result:
                    return result.group()
                else:
                    return 'ERRO'
            else:
                return 'PALAVRA NÃO ENCONTRADA'

    def get_all_words_declinations(self, words: list):
        words_declinations: list = [self.get_word_declination(word) for word in words]
        return words_declinations


def get_formated_words_data(words_list):
    wik_bot = Wiktionary(browser, By)

    w_decs = wik_bot.get_all_words_declinations(words_list)

    formated_w_decs: list = []

    for word_dec in w_decs:
        lines = word_dec.split('\n')
        lines = [line for line in lines if line]
        formated_result = [line.split() for line in lines]

        genitive_case: str

        for line in formated_result:
            for idx, word in enumerate(line):
                if word == 'Genitive':
                    genitive_case = line[idx + 1]

        for idx1, line in enumerate(formated_result):
            for idx, word in enumerate(line):
                if word == 'Case':
                    formated_result[idx1][idx] = genitive_case

        formated_w_decs.append(formated_result) 
    
    return formated_w_decs


results = get_formated_words_data(['hominum', 'rosa', 'exercitus'])

for result in results:
    print(result)



# para o processo não demorar demais, modificar o scrapper para aceitar uma lista de palavras e
# já buscá-las de uma vez