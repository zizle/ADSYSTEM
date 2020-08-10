# _*_ coding:utf-8 _*_
# @File  : ADClient.py
# @Time  : 2020-07-19 11:31
# @Author: zizle

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView
from main_window import MainWindow

app = QApplication([])
client = MainWindow()
client.show()
sys.exit(app.exec_())
