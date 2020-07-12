import re

operator = r"\(Speaker 0\)"
client = r"\(Speaker 1\)"
time_code = r"<[0-9.]*>"
min_delta = 0.01


def interrupting(text):
    '''
    Функция, считающая число перебиваний репликами шаблона "operator" реплик шаблона "client"
    Формат шаблона имени : (Name)
    Формат таймкода : <time>
    :param text: текст (str())
    :return: число перебиваний (int())
    '''
    ban = 0
    strings = text.split('\n')

    o_first = 0
    if re.match(client, strings[0]):  # Если первая реплика не оператора
        o_first += 1

    for i in range(o_first, len(strings)):
        try:
            o_time = re.findall(time_code, strings[i])  # Таймкоды оператора
            c_time = re.findall(time_code, strings[i - 1])  # Таймкоды клиента
        except IndexError:
            continue
        if abs(float(o_time[0][1: -1]) - float(c_time[1][1: -1])) <= min_delta:
            ban += 1
    return ban


def o_phrases(text):
    '''
    Удаляет фразы шаблона "client", таймкоды, и метки имени
    :param text: текст (str())
    :return: реплики шаблона "operator" (str())
    '''
    o_list = re.findall(operator + r".*\n*", text)
    t = str()
    for i in o_list:
        i = re.sub(time_code, "", i)  # Удаляет таймкоды
        i = re.sub(operator+ " :  ", "", i)  # Удаляет метки имени
        t += i
    return t
