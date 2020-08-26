# _*_ coding:utf-8 _*_
# @File  : basis_ui.py
# @Time  : 2020-08-26 16:26
# @Author: zizle

""" 合约基差分析 """

from PySide2.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSplitter, QVBoxLayout, QComboBox, QPushButton,
                               QTableWidget, QFrame)
from PySide2.QtCore import Qt, QMargins
from PySide2.QtWebEngineWidgets import QWebEngineView
from components.variety_tree import VarietyTree


class BasisUI(QSplitter):
    def __init__(self, *args, **kwargs):
        super(BasisUI, self).__init__(*args, **kwargs)
        main_layout = QHBoxLayout()
        self.variety_tree = VarietyTree(self)
        main_layout.addWidget(self.variety_tree)

        self.right_widget = QWidget(self)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(QMargins(1, 1, 1, 1))

        opts_layout = QHBoxLayout()
        opts_layout.addWidget(QLabel("合约:", self))
        self.contract_combobox = QComboBox(self)
        self.contract_combobox.setMinimumWidth(80)
        opts_layout.addWidget(self.contract_combobox)
        self.query_button = QPushButton("查询", self)
        opts_layout.addWidget(self.query_button)

        self.tip_label = QLabel('选择对应品种和合约后查询数据. ', self)
        opts_layout.addWidget(self.tip_label)
        opts_layout.addStretch()

        right_layout.addLayout(opts_layout)

        self.show_splitter = QSplitter(orientation=Qt.Vertical)
        # 图形容器
        self.chart_view = QWebEngineView(self)
        self.chart_view.setMinimumHeight(int(self.height() * 0.518))
        self.show_splitter.addWidget(self.chart_view)
        # 数据展示
        self.chart_data_table = QTableWidget(self)
        self.chart_data_table.setFrameShape(QFrame.NoFrame)
        self.show_splitter.addWidget(self.chart_data_table)
        self.show_splitter.setStretchFactor(0, 6)
        self.show_splitter.setStretchFactor(1, 4)
        self.show_splitter.setHandleWidth(2)

        right_layout.addWidget(self.show_splitter)

        self.right_widget.setLayout(right_layout)

        main_layout.addWidget(self.right_widget)

        self.setLayout(main_layout)

        self.setStretchFactor(0, 3)
        self.setStretchFactor(1, 7)
        self.setHandleWidth(1)
