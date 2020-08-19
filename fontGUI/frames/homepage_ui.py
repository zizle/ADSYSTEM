# _*_ coding:utf-8 _*_
# @File  : homepage_ui.py
# @Time  : 2020-07-19 15:12
# @Author: zizle
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QPainter, QPixmap


class HomepageUI(QWidget):
    """ 首页UI """
    def __init__(self, *args, **kwargs):
        super(HomepageUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        label = QLabel("期货数据分析", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color:rgb(200,20,20);font-size:15px")
        layout.addWidget(label)

        # self.is_logged_button = QPushButton("我已登录?", self)
        # layout.addWidget(self.is_logged_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap("images/home_bg.jpg"), QRect())

