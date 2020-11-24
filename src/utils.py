import random
import string
from datetime import datetime, timedelta


def get_random_string(length: int):
    randlist = [random.choice(string.digits) for i in range(length)]
    return "".join(randlist)


def get_ttl_value(now: datetime, days: int) -> int:
    """
    与えられた現在日時に指定された日数を加え、unixtimeに変換して返す
    :param days:
    :param now:
    :return: ttl値(unixtime)
    """
    ttl = now + timedelta(days=days)
    return int(ttl.strftime("%s"))
