from spliting import splitting
from singular_decomposition import topics


def topics_of_dialogue(text):
    """
    :param text: str - имя файла
    :return: list - список тем
    """
    return topics(splitting(text, 10))
