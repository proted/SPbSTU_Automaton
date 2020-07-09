import re
from nltk import word_tokenize
from splitting import stemming

def search_phrases(text, ness_phrases, border):
    """
    :param text: str - текст
    :param ness_phrases: list(str) - список проверочных фраз
    :param border: int - количество фраз, после которого выдается бан
    :return: int - 1 - если слова найдены в необходимом количестве, 0 - если не найдены
    """
    num = 0
    for phrase in ness_phrases:
        pattern = phrase
        res = re.findall(pattern, text)
        if len(res) != 0:
            if num > border:
                print(num)
                return 1
            num = num + len(res)
    print(num)
    if num > border:
        return 1
    else:
        return 0

def search_words(text, ness_words, border):
    """
    :param text: str - текст
    :param ness_words: list(str) - список проверочных слов
    :param border: int - количество слов, после которого выдается бан
    :return: int - 1 - если слова найдены в необходимом количестве, 0 - если не найдены
    """
    text = word_tokenize(text, "russian")
    text = stemming(text)
    num = 0
    for word in ness_words:
        if word in text:
            if num > border:
                print(num)
                return 1
            num = num + 1
    print(num)
    if num > border:
        return 1
    else:
        return 0
