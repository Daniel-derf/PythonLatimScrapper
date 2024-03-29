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
    
    def open_word_declination(self, latin_word):
        if latin_word:
            self.browser.get(WIKTIONARY_LINK + latin_word)
    
    def open(self, link):
        self.browser.get(link)

    def get_word_declination(self, word: str):
        self.open_word_declination(latin_word=word)
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
                    return print('Resultado não encontrado para palavra ', word)
            else:
                return 'PALAVRA NÃO ENCONTRADA'

    def get_all_words_declinations(self, words: list):
        words_declinations: list = [self.get_word_declination(word) for word in words]
        return words_declinations


def get_words_formated_data(words_list):
    wik_bot = Wiktionary(browser, By)

    w_decs = wik_bot.get_all_words_declinations(words_list)

    formated_w_decs: list = []

    for word_dec in w_decs:
        if word_dec:
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

    ordered_positions = [0, 1, 6, 2, 3, 5, 4]

    for line in formated_w_decs:
        new_line = [1, 2, 3, 4, 5, 6, 7]
        for i, index in enumerate(ordered_positions):
            new_line[i] = line[index]
        line[:] = new_line

    return formated_w_decs



