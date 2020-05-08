from splitting import splitting
from singular_decomposition import topics


def topics_of_dialogue(text, ID):
    return topics(splitting(text, 10))
