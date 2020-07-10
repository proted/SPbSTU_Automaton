import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import re


def split_text(file):
    """
    :param file: str - имя файла
    :return: list(str) - список из слов
    Разделяем текст на слова и удаляем "не слова" (цифры, скобки, знаки препинания)
    """
    fp = open(file, 'r', encoding='windows-1251')
    text = fp.read()
    fp.close()
    text = del_non_words(text)
    words = word_tokenize(text, "russian")
    return words


def del_non_words(text):
    """
    :param text: str - текст
    :return: str - текст без лишних символов
    Удаляет все 'не слова', т.е. цифры, числа, знаки препинания.
    """
    pattern = r"[0-9]"
    pattern2 = r"[^\w]"
    pattern3 = r"[Speaker]"
    text = re.sub(pattern, " ", text)
    text = re.sub(pattern2, " ", text)
    text = re.sub(pattern3, " ", text)
    return text


def chunked(words, num_of_words):
    """
    :param words: list(str) - список слов
    :param num_of_words: int - количество слов
    :return: list(str) - блок слов
    """
    current = 0
    while True:
        chunk = words[current: current + num_of_words]
        current += num_of_words
        if chunk:
            yield chunk
        else:
            break


def unite_in_blocks(words, num_of_words):
    """
    :param words: list(str) - список слов
    :param num_of_words: int - количество слов
    :return: list(list(str)) - список блоков слов
    Обёртка для функции chunked.
    """
    return list(chunked(words, num_of_words))


def stemming(words):
    """
    :param words: list(str) - список слов
    :return: list(str) - список изменных слов
    Функция выполняет стемминг для списка слов.
    """
    stemmer = SnowballStemmer("russian")
    result = [stemmer.stem(word) for word in words]
    return result


def del_words(words):
    """
    :param words: list(str) - список слов
    :return: list(str) - список без стоп-слов
    """
    new_words = list()
    stop_words = list(stopwords.words('russian'))
    for word in words:
        if word not in stop_words:
            new_words.append(word)
    return new_words


def splitting(file, num_of_words):
    """
    :param file: str - имя файла
    :param num_of_words: int - количество слов в блоке
    :return: list(list(str)) - список блоков слов
    Разделение текста на блоки слов.
    """
    words = split_text(file)
    words = del_words(words)
    words = stemming(words)
    blocks_of_words = unite_in_blocks(words, num_of_words)
    return blocks_of_words
