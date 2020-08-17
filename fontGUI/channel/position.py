# _*_ coding:utf-8 _*_
# @File  : position.py
# @Time  : 2020-08-17 9:53
# @Author: zizle
""" 与持仓分析网页交互的通道 """

from PySide2.QtCore import QObject, Signal, Slot


class PositionPageChannel(QObject):
    position_data = Signal(str, str)
