import numpy as np
from math import fabs


class FrequenciesMatrix(object):
    '''
    Класс для работы с матрицой частотности термов на предложение
    Для хранения частот используется матрица, в которой строкам отвечает терм, а столбцам - предложение
    '''

    def __init__(self, sentences):
        '''
        Создает частотную матрицу по списку предложений
        :param sentences: list(str())  -  список предложений разбитых на слова
        '''
        # Составления списка из всех слов
        self.word_list = []
        for sentence in sentences:
            for word in sentence:
                if word not in self.word_list:
                    self.word_list.append(word)

        self.word_list.sort()  # Лексикографический порядок
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
        Возвращает число строк, которые нужно оставить после сингулярного разложения
        return: int()  -  число значимых строк и столбцов
        '''
        return 2


def load_topics():
    '''
    Загружает темы из файла, имя которого определено константно, возвращает словарь тем из этого файла
    :param file: str()  -  имя файла, где содержатся темы с ключевыми словами
    :return: dict()  -  тема : список слов по этой теме
    '''
    file_name = "topics.txt"
    file = open(file_name, "r")
    res = dict()
    for group in file:
        topic, keywords = group.split(':')
        res[topic] = keywords.split()
    f.close()
    return res


def major_topics(weight_dict):
    '''
    Определяет основные темы разговора по их суммарным весам, возвращает отсортированный список тем с весом больше 0.4
    :param weight_dict: dict()  -  словарь тем, которые встретились в разговоре (тема : вес)
    :return: list(str())  -  отсортированный по весам список тем разговора, которые набрали вес >0.4
    '''
    res_list = list()
    for key in weight_dict.keys():
        if weight_dict[key] > 0.4:
            res_list.append((key, weight_dict[key]))
    res_list.sort(key=lambda i: i[1])
    sorted_list = list()
    for i in res_list:
        sorted_list.append(i[0])
    return sorted_list


def topics(sentences_list):
    '''
    Основная функция модуля определения тематики разговора
    :param sentences_list: list(list(str()))  -  список предложений, разбитых по словам (разговор)
    :return: list(str())  -  список тем разговора
    '''
    b = FrequenciesMatrix(sentences_list)
    U, S, Vt = np.linalg.svd(b.freq_matrix, full_matrices=False)

    #  Округление для наглядности
    U = np.round(U, 2).transpose()
    S = np.round(S, 2)
    Vt = np.round(Vt, 2)
    # Отсечение шумов
    k = b.def_k()
    U = U[0:k]
    S = S[0:k]
    Vt = Vt[0:k]
    # Функция СВД возвращает массив для диагональной матрицы, восстанавливаем матрицу из массива ниже
    S1 = np.zeros((k, k))
    for i in range(k):
        S1[i][i] = S[i]

    # Восстановление матрицы без шумов, с учётом латентных семантических связей
    # Слово может не присутствовать в предложении, однако иметь в итоговой матрице в этом предложении вес
    U = U.transpose()
    U = U.dot(S1)
    res_matrix = U.dot(Vt)

    topics_list = load_topics()
    weights = dict()  # Словарь для итоговых весов каждой темы
    # Смысл цикла ниже:
    # Для каждой темы из файла суммируем веса слов, которые относятся к этим темам и встретились в диалоге
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
