# _*_ coding:utf-8 _*_
# @File  : kline.py
# @Time  : 2020-08-11 8:20
# @Author: zizle

""" 与K线网页交互的通道 """

from PySide2.QtCore import QObject, Signal, Slot


class KlinePageChannel(QObject):
    kline_data = Signal(str, str)
