# _*_ coding:utf-8 _*_
# @File  : contract_kei_ui.py
# @Time  : 2020-08-07 14:26
# @Author: zizle

from PySide2.QtWidgets import QWidget
from PySide2.QtWebEngineWidgets import QWebEngineView


class ContractKeiUI(QWidget):
    """ 合约K线界面 """
    def __init__(self, *args, **kwargs):
        super(ContractKeiUI, self).__init__(*args, **kwargs)
