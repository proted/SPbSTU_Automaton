from splitting import splitting
from singular_decomposition import topics
from assessment import number
from assessment import assessment



def analysis(text, id):
    """
    :param text: str - имя файла
    :param id:str  -  id разговора
    :return: tuple - оценка, лог, темы
    """
    result = number(), assessment(text, id), topics(splitting(text, 10))
    return result


print(analysis("testbad.txt", "rje"))
