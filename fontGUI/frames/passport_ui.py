# _*_ coding:utf-8 _*_
# @File  : login.py
# @Time  : 2020-07-20 9:03
# @Author: zizle

from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QTabWidget, QLineEdit, QVBoxLayout, QPushButton
from PySide2.QtCore import Qt, Signal


class ImageCodeLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
        ev.accept()


class PassportPageUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(PassportPageUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tab = QTabWidget(self)
        layout.addWidget(self.tab, alignment=Qt.AlignCenter)

        """ 登录页 """
        self.login_page = QWidget(self)
        layout = QGridLayout()

        layout.addWidget(QLabel("<div>手&nbsp;机:</div>", self), 0, 0, 1, 2)
        self.login_phone = QLineEdit(self)
        layout.addWidget(self.login_phone, 0, 1, 1, 2)

        layout.addWidget(QLabel("<div>密&nbsp;码:</div>", self), 1, 0, 1, 2)
        self.login_password = QLineEdit(self)
        layout.addWidget(self.login_password, 1, 1, 1, 2)

        layout.addWidget(QLabel("验证码:", self), 2, 0)
        self.login_code = QLineEdit(self)
        layout.addWidget(self.login_code, 2, 1)

        self.login_code_image = ImageCodeLabel("获取中..", self)
        self.login_code_image.setFixedWidth(60)
        self.login_code_image.setScaledContents(True)
        layout.addWidget(self.login_code_image, 2, 2)

        self.login_button = QPushButton("登录", self)
        layout.addWidget(self.login_button, 3, 0, 1, 3)

        self.login_page.setLayout(layout)

        """ 注册页 """
        self.register_page = QWidget(self)

        layout = QGridLayout()
        layout.addWidget(QLabel("手机:", self), 0, 0)
        self.register_phone = QLineEdit(self)
        layout.addWidget(self.register_phone, 0, 1, 1, 2)

        layout.addWidget(QLabel("昵称:", self), 1, 0)
        self.register_nickname = QLineEdit(self)
        layout.addWidget(self.register_nickname, 1, 1, 1, 2)

        layout.addWidget(QLabel("密码:", self), 2, 0)
        self.register_password_1 = QLineEdit(self)
        layout.addWidget(self.register_password_1, 2, 1, 1, 2)

        layout.addWidget(QLabel("确认密码:", self), 3, 0)
        self.register_password_2 = QLineEdit(self)
        layout.addWidget(self.register_password_2, 3, 1, 1, 2)

        layout.addWidget(QLabel("验证码:", self), 4, 0)
        self.register_code = QLineEdit(self)
        layout.addWidget(self.register_code, 4, 1)

        self.register_code_image = ImageCodeLabel("获取中..", self)
        self.register_code_image.setFixedWidth(60)
        self.register_code_image.setScaledContents(True)
        layout.addWidget(self.register_code_image, 4, 2)

        self.register_button = QPushButton("注册", self)
        layout.addWidget(self.register_button, 5, 0, 1, 3)

        self.register_page.setLayout(layout)

        self.tab.addTab(self.login_page, "用户登录")
        self.tab.addTab(self.register_page, "用户注册")

        self.tab.setFixedSize(300, 200)
        self.tab.setObjectName("passportTab")
        self.tab.tabBar().setObjectName("tabBar")
        self.tab.tabBar().setCursor(Qt.PointingHandCursor)
        # passportTab::pane{border:none}
        self.setStyleSheet("""
        #passportTab::pane{border:none}
        #passportTab::tab-bar{alignment:left}
        #tabBar::tab{min-width:30ex;min-height:10ex;border:none}
        #tabBar::tab:hover{background-color:rgb(255,255,255,100)}
        #tabBar::tab:selected{color:green;}
        """)
