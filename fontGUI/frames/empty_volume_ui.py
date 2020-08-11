# _*_ coding:utf-8 _*_
# @File  : empty_volume_ui.py
# @Time  : 2020-08-11 21:06
# @Author: zizle

""" 持仓分析界面 """
from PySide2.QtWidgets import QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt, QMargins
from components.variety_tree import VarietyTree


class EmptyVolumeUI(QSplitter):
    def __init__(self, *args, **kwargs):
        super(EmptyVolumeUI, self).__init__(*args, **kwargs)
        self.variety_tree = VarietyTree(self)

        self.addWidget(self.variety_tree)

        self.right_widget = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(QMargins(1, 1, 1, 1))
        opts_layout = QHBoxLayout()

        opts_layout.addWidget(QLabel("选择合约:", self))
        self.contract_combobox = QComboBox(self)
        opts_layout.addWidget(self.contract_combobox)

        self.confirm_button = QPushButton("确定", self)
        opts_layout.addWidget(self.confirm_button)
        opts_layout.addStretch()

        right_layout.addLayout(opts_layout)

        self.web_container = QWebEngineView(self)
        right_layout.addWidget(self.web_container)

        self.right_widget.setLayout(right_layout)
        self.addWidget(self.right_widget)

        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 8)
        self.setHandleWidth(1)
        self.contract_combobox.setMinimumWidth(80)