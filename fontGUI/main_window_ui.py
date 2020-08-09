# _*_ coding:utf-8 _*_
# @File  : main_window_ui.py
# @Time  : 2020-07-19 11:36
# @Author: zizle

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt, QMargins
from PySide2.QtGui import QIcon


class UserBarUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(UserBarUI, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(QMargins(0, 0, 5, 0))
        self.login_button = QPushButton("点击登录", self)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setIcon(QIcon("icons/login.png"))
        self.login_button.setFixedWidth(88)
        setattr(self.login_button, "username", "")

        layout.addWidget(self.login_button)
        self.logout_button = QPushButton("退出", self)
        self.logout_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.logout_button)
        self.setLayout(layout)
        self.logout_button.hide()
        self.login_button.setObjectName("loginButton")
        self.logout_button.setObjectName("logoutButton")
        # loginButton::menu-indicator{image:none;}
        self.setStyleSheet(
            "#loginButton,#logoutButton{border:none;height:22px}"
            "#loginButton:hover{color:rgb(100,160,210)}"
        )


class MainWindowUI(QMainWindow):
    """ 主窗口UI """

    def __init__(self, *args, **kwargs):
        super(MainWindowUI, self).__init__(*args, **kwargs)
        self.resize(1080, 720)
        self.setWindowTitle("期货数据分析系统")
        self.setWindowIcon(QIcon("icons/app.png"))
        self.menu_bar = self.menuBar()
        self.use_bar = UserBarUI(parent=self.menu_bar)
        self.menu_bar.setCornerWidget(self.use_bar, corner=Qt.TopRightCorner)
