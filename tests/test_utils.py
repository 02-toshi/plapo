"""utilsのテスト"""
from src import utils


def test_get_random_string():
    result = utils.get_random_string(10)
    print(result)
    assert len(result) == 10
