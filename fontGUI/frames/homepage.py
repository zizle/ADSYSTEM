# _*_ coding:utf-8 _*_
# @File  : homepage.py
# @Time  : 2020-07-19 15:14
# @Author: zizle
from .homepage_ui import HomepageUI


class Homepage(HomepageUI):
    """ 首页业务 """

    def __del__(self):
        print("~首页窗口析构了")



