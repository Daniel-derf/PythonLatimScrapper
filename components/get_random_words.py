import random as rand

words_file = open("./words.txt")
all_words = words_file.read().split('\n')

def get_random_words():
    words: list = []
    for i in range(1,7):
        rand_word = rand.choice(all_words)
        words.append(rand_word)
    return words





