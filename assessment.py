from interrupting import interrupting
from interrupting import o_phrases
from search_words import search_phrases
from search_words import search_words


def read_file(file):
    '''
    # Чтение файла
    :param file: str  -  имя файла
    :return: str  -  содержимое файла
    '''
    fp = open(file, 'r', encoding='windows-1251')
    text = fp.read()
    fp.close()
    return text


def create_log(res, id):
    '''
    Создаёт файл с результатами проверки
    :param res: dict  -  результаты функций (имя функции : результат)
    :param id: str  -  id разговора
    :return: str  -  имя файла
    '''
    name = "desc_" + str(id)
    file = open(name, "w")
    for key in res.keys():
        file.write(str(key) + str(res[key]) + '\n')
    file.close()
    return name


def assessment(file, id):
    '''
    Функция проверяет разговор на наличие перебиваний, нецензурной лексики и слов-паразитов.
    :param file: str  -  имя файла с записью разговора
    :param id: str  -  id разговора
    :return: str  -  имя файла, в котором находятся результаты проверяющих функций
    '''
    res = dict()
    text = read_file(file)
    interruptions = interrupting(text)
    text = o_phrases(text)
    res['слова парзиты'] = search_phrases(text, read_file('parasites.txt').split('\n'), 3)
    res['вежливость'] = search_phrases(text, read_file('polite.txt'), 0)
    res['обязательно'] = search_phrases(text, read_file('required.txt'), 1)
    res['мат'] = search_words(text, read_file('obscene.txt').split('\n'), 0)
    return create_log(res, id)


def number():
    return 9