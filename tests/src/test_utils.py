"""utilsのテスト"""
from datetime import datetime

from src import utils


def test_get_random_string():
    result = utils.get_random_string(10)
    assert len(result) == 10


def test_get_ttl_value():
    test_now = datetime(2020, 11, 22, 0, 0, 0)
    test_tomorrow = datetime(2020, 11, 23, 0, 0, 0)
    test_tomorrow_ttl = int(test_tomorrow.strftime("%s"))

    ttl = utils.get_ttl_value(test_now, 1)
    assert ttl == test_tomorrow_ttl
