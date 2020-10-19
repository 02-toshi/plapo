import random
import string


def get_random_string(length: int):
    randlist = [random.choice(string.digits) for i in range(length)]
    return ''.join(randlist)
