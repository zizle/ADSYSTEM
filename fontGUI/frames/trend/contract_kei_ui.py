# _*_ coding:utf-8 _*_
# @File  : contract_kei_ui.py
# @Time  : 2020-08-07 14:26
# @Author: zizle

from PySide2.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt, QMargins, QUrl
from components.variety_tree import VarietyTree


class ContractKeiUI(QSplitter):
    """ 合约K线界面 """
    def __init__(self, *args, **kwargs):
        super(ContractKeiUI, self).__init__(*args, **kwargs)
        main_layout = QHBoxLayout()  # 使用主layout,让控件自适应窗口改变大小
        main_layout.setSpacing(0)

        self.variety_tree = VarietyTree(self)
        main_layout.addWidget(self.variety_tree)

        self.right_widget = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(QMargins(1, 1, 1, 1))
        opts_layout = QHBoxLayout()

        opts_layout.addWidget(QLabel("选择合约:", self))
        self.contract_combobox = QComboBox(self)
        opts_layout.addWidget(self.contract_combobox)

        self.confirm_button = QPushButton("确定", self)
        opts_layout.addWidget(self.confirm_button)

        self.tip_button = QPushButton("正在查询数据 ", self)
        self.tip_button.hide()
        opts_layout.addWidget(self.tip_button)

        opts_layout.addStretch()

        right_layout.addLayout(opts_layout)

        self.web_container = QWebEngineView(self)
        right_layout.addWidget(self.web_container)

        self.right_widget.setLayout(right_layout)
        main_layout.addWidget(self.right_widget)

        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 8)
        self.setHandleWidth(1)
        self.contract_combobox.setMinimumWidth(80)
        self.setLayout(main_layout)
        self.tip_button.setObjectName("tipButton")
        self.setStyleSheet("#tipButton{border:none;color:rgb(230,50,50);font-weight:bold}")
