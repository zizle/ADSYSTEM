# _*_ coding:utf-8 _*_
# @File  : exchange_spider_ui.py
# @Time  : 2020-07-22 20:47
# @Author: zizle

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel
from PySide2.QtCore import QMargins
from components.tree_widget import ExchangeLibTree


class ExchangeSpiderUI(QWidget):
    """ 数据抓取主页面 """
    def __init__(self, *args, **kwargs):
        super(ExchangeSpiderUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        layout.setContentsMargins(QMargins(2, 0, 2, 1))
        tree_widget_splitter = QSplitter(self)
        self.tree_widget = ExchangeLibTree(self)
        tree_widget_splitter.addWidget(self.tree_widget)

        l = QLabel("设置label", self)
        l.resize(self.width() * 0.8, self.height())
        tree_widget_splitter.addWidget(l)
        layout.addWidget(tree_widget_splitter)
        self.setLayout(layout)



