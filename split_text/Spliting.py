from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

#Разделяем текст на слова, словами также явялются метки (скобки).
#На входе строка с именем файла. На выходе список разделенных слов.
def split_text(file):
    fp = open('test.txt', 'r')
    text = fp.read()
    fp.close()
    words = word_tokenize(text, "russian")
    return words

#Разбиваем все слова на блоки из слов.
#На входе список слов words и количество слов в одном блоке num_of_words. Пока не закончились слова, возвращает блоки.
def chunked(words, num_of_words):
    current = 0
    while True:
        chunk = words[current: current + num_of_words]
        current += num_of_words
        if chunk:
            yield chunk
        else:
            break

#Обёртка для функции chunked. На входе те же данные. На выходе список из блоков слов.
def unite_in_blocks(words, num_of_words):
    return list(chunked(words, num_of_words))

#Функция выполняет стемминг для списка слов. На входе список слов words. На выходе список изменных слов result.
def stemming(words):
    stemmer = SnowballStemmer("russian")
    result = [stemmer.stem(word) for word in words]
    return result

#Удалаяет стоп-слова. На входе список слов words и список дополнительных стоп-слов. На выходе список без стоп-слов.
def del_words(words, extra_words):
    new_words = list()
    stop_words = list(stopwords.words('russian'))
    stop_words.extend(extra_words)
    for word in words:
        if word not in stop_words:
            new_words.append(word)
    return new_words

#Разделение текста на блоки слов, уже нормализованных стеммингом. На входе имя файла и количество слов в блоке.
#На выходе список блоков слов заданного размера.
def splitting(file, num_of_words):
    words = split_text(file)
    words = del_words(words, ['.'])
    words = stemming(words)
    blocks_of_words = unite_in_blocks(words, num_of_words)
    return blocks_of_words
