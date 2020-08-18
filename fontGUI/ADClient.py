# _*_ coding:utf-8 _*_
# @File  : ADClient.py
# @Time  : 2020-07-19 11:31
# @Author: zizle

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import QCoreApplication, Qt
from main_window import MainWindow
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
QGuiApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)

app = QApplication([])
client = MainWindow()
client.show()
sys.exit(app.exec_())
