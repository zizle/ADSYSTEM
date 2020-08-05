# _*_ coding:utf-8 _*_
# @File  : homepage_ui.py
# @Time  : 2020-07-19 15:12
# @Author: zizle
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide2.QtCore import Qt


class HomepageUI(QWidget):
    """ 首页UI """
    def __init__(self, *args, **kwargs):
        super(HomepageUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        label = QLabel("交易所数据计算查询.", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color:rgb(200,20,20);font-size:15px")
        layout.addWidget(label)
        self.setLayout(layout)

