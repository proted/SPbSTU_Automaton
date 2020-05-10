from splitting import splitting
from singular_decomposition import topics

#Функция определения темы. На входе строка с именем файла text (str: text) и ID записи в БД ID (int: ID). 
#Возвращает список тем (list).
def topics_of_dialogue(text, ID):
    return topics(splitting(text, 10))
