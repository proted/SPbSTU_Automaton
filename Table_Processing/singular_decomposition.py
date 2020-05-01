import numpy as np
from math import fabs

'''sentences_list = [['полиц', 'основател', 'wikileaks'],
                  ['суд', 'сша', 'прот'],
                  ['церемон','вручен','нобелевск', 'прем', 'стран'],
                  ['великобритан', 'арестова', 'основател', 'wikileaks'],
                  ['церемон', 'вручен', 'нобелевск','прем'],
                  ['суд', 'основател', 'wikileaks'],
                  ['сша', 'стран', 'прот'],
                  ['полиц', 'великобритан', 'основател', 'wikileaks', 'арестова'],
                  ['вручен', 'нобелевск', 'прем']]'''

#sentences_list = [['добр', 'ден', 'сотрудник', 'зовут', 'анастас', 'мог', 'помоч', 'здравств', 'хотел', 'узна'], ['стоимост', 'чипс', 'дан', 'товар', 'сто', 'сто', 'рубл', 'поч', 'ценник', 'указа'], ['сто', 'сорок', 'рубл', 'наход', 'акц', 'законч', 'поч', 'сто', 'неправильн', 'ценник'], ['хотел', 'пода', 'жалоб', 'недовол', 'нам', 'очен', 'жал', 'принос', 'сво', 'извинен'], ['доставлен', 'неудобств', 'может', 'остав', 'жалоб', 'наш', 'сайт', 'мог', 'чем-т', 'помоч'], ['спасиб', 'досвидан', 'спасиб', 'звонок', 'хорош', 'дня']]




file_immitation = ['Трудоустройство: трудоустройств работ ваканс зарплат смен резюм',
'Жалоба: жалоб недовольств пода грубост обид разозл медлен неправильн',
'Наличие товара: налич товар полк ест магазин',
'Стоимость товара: скольк сто акц цен товар стоимост',
'Утеря вещей в магазине: магазин вещ забра найт нашл утеря потер сумк' ]


class FrequenciesMatrix(object):
    '''
    Класс для работы с матрицой частотности термов на предложение
    Для хранения частот используется матрица, в которой строкам отвечает терм, а столбцам - предложение
    '''

    def __init__(self, sentences):
        '''
        Создает частотную матрицу по списку предложений
        :param sentences: список предложений разбитых на слова
        '''
        # Составления списка из всех слов
        self.word_list = []
        for sentence in sentences:
            for word in sentence:
                if word not in self.word_list:
                    self.word_list.append(word)

        self.word_list.sort()  # Лексикографический порядок !!!НУЖНО УБЕДИТЬСЯ, ЧТО СОРТИРОВАТЬ СЛОВА ВЫГОДНО!!!
        self.word_hash = dict()
        for i in range(len(self.word_list)):
            self.word_hash[self.word_list[i]] = i

        self.freq_matrix = np.zeros((len(self.word_list), len(sentences)))  # Нулевая матрица mxn
        sentences_counter = 0
        for sentence in sentences:
            for word in sentence:
                self.freq_matrix[self.word_hash[word]][sentences_counter] += 1  # Увеличиваем вес слова в текщем предлож
            sentences_counter += 1  # Конец обработки предложения

    def def_k(self):
        '''
        Здесь могла бы быть ваша реклама
        :return: 2
        '''
        return 2


def load_topics(file):
    '''
    Пока принимает список строк с темами
    :param file: список строк с темами
    :return: словарь (тема: ключевые слова)
    '''
    res = dict()
    for group in file:
        topic, keywords = group.split(':')
        res[topic] = keywords.split()
    return res


def major_topics(weight_dict):
    '''
    Определяет основные темы разговора по их суммарным весам
    :param weight_dict: словарь (тема: вес)
    :return: список основных тем
    '''
    res_list = list()
    for key in weight_dict.keys():
        if weight_dict[key] > 0.4:
            res_list.append(key)
    return res_list


def topics(sentences_list):
    '''
    Основная функция модуля определения тематики разговора
    !!!ЧАСТЬ ЭТОЙ ФУНКЦИИ НУЖНО УПАКОВАТЬ В ОТДЕЛЬНЫЕ ПОДФУНКЦИИ!!!
    :param sentences_list: список предложений, разбитых по словам list(list(str()))
    :return: список тем разговора list(str())
    '''
    b = FrequenciesMatrix(sentences_list)
    U, S, Vt = np.linalg.svd(b.freq_matrix, full_matrices=False)
    
    #  Округление для наглядности
    U = np.round(U, 2).transpose()
    S = np.round(S, 2)
    Vt = np.round(Vt, 2)

    k = b.def_k()
    U = U[0:k]
    S = S[0:k]
    Vt = Vt[0:k]

    S1 = np.zeros((k, k))
    for i in range(k):
        S1[i][i] = S[i]

    # Восстановление матрицы без шумов, с учётом латентных семантических связей
    # Слово может не присутствовать в предложении, однако иметь в итоговой матрице в этом предложении вес
    U = U.transpose()
    U = U.dot(S1)
    res_matrix = U.dot(Vt)

    topics_list = load_topics(file_immitation)
    weights = dict()  # Словарь для итоговых весов каждой темы
    # Смысл уродского цикла ниже:
    # Для каждой темы из файла мы суммируем веса слов, которые относятся к этим темам и встретились в диалоге
    for topic in topics_list:
        for keyword in topics_list[topic]:
            try:
                str_num = b.word_hash[keyword]
                try:  # Тема уже встречалась в диалоге
                    weights[topic] += np.sum(res_matrix[str_num])
                except KeyError:  # Тема встретилась или была найдена впервые
                    weights[topic] = 0
            except KeyError:
                pass
    return major_topics(weights)
