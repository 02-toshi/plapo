import random
import string

from numpy.core import number


def get_random_string(length: int):
    randlist = [random.choice(string.digits) for i in range(length)]
    return "".join(randlist)


def get_ttl_value(days: int) -> number:
    """
    日数を指定するとunixtimeに変換してttl値を返す

    :param days:
    :return: ttl値(unixtime)
    """
    # TODO: 実装書く
    return
