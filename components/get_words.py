from components import wiktionary_bot as w
import re
import random

declination_links = {
    "first": r"https://en.wiktionary.org/w/index.php?title=Category:Latin_first_declension_nouns&from=AZ",
    "second": r'https://en.wiktionary.org/w/index.php?title=Category:Latin_second_declension_nouns&from=AZ',
    "third": r'https://en.wiktionary.org/w/index.php?title=Category:Latin_third_declension_nouns&from=AZ',
    "fourth": r'https://en.m.wiktionary.org/w/index.php?title=Category:Latin_fourth_declension_nouns&filefrom=AZ&subcatfrom=AZ&pageuntil=AZ#mw-pages',
    "fifth": r'https://en.wiktionary.org/wiki/Category:Latin_fifth_declension_nouns'
}

browser = w.browser

bot = w.Wiktionary(browser, w.By)

def get_random_word(declination):
    bot.open(declination_links[declination])
    words = []
    path = '//*[text()="next page"]'

    while True:
        try:
            content = browser.find_element(w.By.ID, 'mw-pages').text
            pattern = r'\n([a-zīāōēū]{2,15})\n'
            words += re.findall(pattern, content)
            el = browser.find_element(w.By.XPATH, path)
            el.click()
        except:
            break
    
    return random.choice(words)


def get_random_words():
    declinations = declination_links.keys()
    words = []
    
    for declination in declinations:
        words.append(get_random_word(declination)) 
        
    return words