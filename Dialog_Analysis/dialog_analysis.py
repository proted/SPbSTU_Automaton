from spliting import splitting
from singular_decomposition import topics


def topics_of_dialogue(text):
    return topics(splitting(text, 10))


print(topics_of_dialogue('test.txt'))
