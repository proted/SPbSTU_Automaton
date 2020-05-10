from interrupting import interrupting
from interrupting import o_phrases
from searh_words import search_phrases
from searh_words import obscene
from searh_words import parasites

#Чтение файла. На входе строка с именем файла. На выходе строка текста из файла.
def read_file(file):
     fp = open(file, 'r', encoding='windows-1251')
     text = fp.read()
     fp.close()
     return text


#Принимает словарь res с результатами проверок и id разговора, возвращает имя файла, в который записан результат
def create_log(res, id):
    name = "desc_"+id
    file = open(name, "w")
    for key in res.keys():
        file.write(str(key) + str(res[key]) + '\n')
    file.close()
    return name


#Функция проверяет разговор на наличие перебиваний, нецензурной лексики и слов-паразитов.
#На входе строка с именем файла.
def assessment(file, id):
    res = dict()
    text = read_file(file)
    interruptions = interrupting(text)
    text = o_phrases(text)
    res['мат'] = search_phrases(text, obscene)
    res['слова парзиты'] = search_phrases(text, parasites)
    return create_log(res, id)
