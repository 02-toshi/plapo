import random
import string


def get_random_string(length: int):
    randlist = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
    print(f"生成した文字列：{randlist}")
    return ''.join(randlist)
