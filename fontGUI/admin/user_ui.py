# _*_ coding:utf-8 _*_
# @File  : user_ui.py
# @Time  : 2020-07-20 22:11
# @Author: zizle

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QTableWidget
from PySide2.QtCore import QMargins, Qt


class UserUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(UserUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        layout.setContentsMargins(QMargins(3, 3, 3, 3))

        opts_layout = QHBoxLayout()
        opts_layout.addWidget(QLabel("用户角色:", self))
        self.user_role_combobox = QComboBox(self)
        opts_layout.addWidget(self.user_role_combobox)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("搜索(关键字按Enter搜索)")
        self.search_input.setAlignment(Qt.AlignCenter)
        opts_layout.addWidget(self.search_input)

        layout.addLayout(opts_layout)

        self.user_table = QTableWidget(self)
        layout.addWidget(self.user_table)

        self.setLayout(layout)
