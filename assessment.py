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


#Функция проверяет разговор на наличие перебиваний, нецензурной лексики и слов-паразитов.
#На входе строка с именем файла.
def assessment(file):
    text = read_file(file)
    interruptions = interrupting(text)
    text = o_phrases(text)
    obsc = search_phrases(text, obscene)
    par = search_phrases(text, parasites)
