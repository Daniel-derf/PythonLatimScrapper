from components import get_random_words as words, make_word_doc as doc, wiktionary_bot as bot


rand_words = words.get_random_words()

words_data = bot.get_words_formated_data(rand_words)

print(words_data)

#doc.build_document(words_data)






    


