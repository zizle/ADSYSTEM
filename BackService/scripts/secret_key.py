# _*_ coding:utf-8 _*_
# @File  : secret_key.py
# @Time  : 2020-08-07 22:58
# @Author: zizle

import random
from hashlib import md5
md5_hash = md5("zizle".encode("utf-8"))
for i in range(1000):
    num = random.randint(0, 10000)
    md5_hash.update(str(num).encode("utf-8"))
# get last and last - 1 and combine
