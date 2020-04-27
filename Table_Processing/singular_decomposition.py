import numpy as np
from math import fabs

sentences_list = [['полиц', 'основател', 'WikiLeaks'],
                  ['суд', ' США', 'прот'],
                  ['Церемон','вручен','нобелевск', 'прем', 'стран'],
                  ['Великобритан', 'арестова', 'основател', 'Wikileaks'],
                  ['церемон', 'вручен', 'нобелевск','прем'],
                  ['суд', 'основател', 'Wikileaks'],
                  ['США', 'стран', 'прот'],
                  ['полиц', 'великобритан', 'основател', 'WikiLeaks', 'арестова'],
                  ['вручен', 'нобелевск', 'прем']]



class DynamicMatrix():
    '''
    Класс динамической матрицы размера m строк, n столбцов
    '''
    def __init__(self, m, n):
        '''
        Создает нулевую матрицу mxn
        :param m: число строк
        :param n: число столбцов
        '''
        self.matrix = list()
        self.m = m
        self.n = n
        for i in range(m):
            for i in range(n):
                self.matrix.append([0])

    def inc(self, i, j):
        '''
        Инкремент элемента (i,j)
        :param i: номер строки
        :param j: номер столбца
        :return: None
        '''
        self.matrix[i][j] += 1

    def append_str(self):
        '''
        Добавляет строку в матрицу
        :return: None
        '''
        for col in self.matrix:
            col.append(0)
        self.m += 1


class FrequenciesMatrix(object):
    '''
    Класс для работы с матрицой частотности термов на предложение
    Для хранения частот используется матрица, в которой строкам отвечает терм, а столбцам - предложение
    '''
    __word_counter = 0
    __hash_list = dict()

    def __init__(self, sentences):
        '''
        Создает частотную матрицу по списку предложений
        :param sentences: список предложений разбитых на слова
        '''
        self.keys = dict()  # Обратные ключи, чтобы восстановить из номера строки слово  !!УБРАТЬ ЭТО!!
        table = DynamicMatrix(1, len(sentences))  # Заготовка матрицы по количеству предложений
        sentences_counter = 0

        for sentence in sentences:
            for word in sentence:
                word_position = self.__hash(word)

                if word_position == -1:  # Значит слово ещё не встречалось
                    word_position = self.__word_counter
                    self.keys[self.__word_counter] = word
                    table.append_str()
                    self.__word_counter += 1
                table.inc(sentences_counter, word_position)

            sentences_counter += 1  # Конец обработки предложения

        self.freq_matrix = np.array(table.matrix).transpose()

    def __hash(self, word):
        '''
        Функция, сопоставляющяя слову его номер строки
        :param word: слово
        :return: номер строки
        '''
        try:
            # Слово уже встречалось и номер его строки есть в словаре _hash_list
            return self.__hash_list[word]
        except KeyError:
            # Слово ещё не встречалось
            self.__hash_list[word] = self.__word_counter
            return -1


b = FrequenciesMatrix(sentences_list)
b.freq_matrix = b.freq_matrix[0: -1]  # КОСТЫЛЬ Не критический
U, S, Vt = np.linalg.svd(b.freq_matrix, full_matrices=True)
# Ниже заготовочка для "построения графика" в к-мерном пространстве
k = 2
U = U[0:k]
Vt.transpose()
Vt = Vt[0:k]
Vt.transpose()
# Остались к строк и столбцов, все слова выражаются к компонентами, нужно найти предложение, к которой слово ближе всего
