# _*_ coding:utf-8 _*_
# @File  : contract_kei_ui.py
# @Time  : 2020-08-07 14:26
# @Author: zizle

from PySide2.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt, QMargins
from components.variety_tree import VarietyTree


class ContractKeiUI(QSplitter):
    """ 合约K线界面 """
    def __init__(self, *args, **kwargs):
        super(ContractKeiUI, self).__init__(*args, **kwargs)
        self.variety_tree = VarietyTree(self)
        self.variety_tree.selected_signal.connect(self.click_variety)
        self.addWidget(self.variety_tree)

        self.right_widget = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(QMargins(1, 1, 1, 1))
        opts_layout = QHBoxLayout()

        opts_layout.addWidget(QLabel("选择合约:", self))
        self.contract_combobox = QComboBox(self)
        opts_layout.addWidget(self.contract_combobox)
        opts_layout.addStretch()

        right_layout.addLayout(opts_layout)

        self.html_container = QWebEngineView(self)
        right_layout.addWidget(self.html_container)

        self.right_widget.setLayout(right_layout)
        self.addWidget(self.right_widget)

        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 8)
        self.setHandleWidth(1)

    def click_variety(self, variety_en):
        """ 点击选择了品种 """
        print(variety_en)
        # 发送请求获取当前品种所有交割月份合约

