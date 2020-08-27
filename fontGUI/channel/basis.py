# _*_ coding:utf-8 _*_
# @File  : basis.py
# @Time  : 2020-08-27 10:01
# @Author: zizle

""" 基差分析相关界面通讯 """

from PySide2.QtCore import QObject, Signal


class BasisPageChannel(QObject):
    basis_data = Signal(str, str)
