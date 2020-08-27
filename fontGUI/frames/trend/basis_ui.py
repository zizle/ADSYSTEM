# _*_ coding:utf-8 _*_
# @File  : basis_ui.py
# @Time  : 2020-08-26 16:26
# @Author: zizle

""" 合约基差分析 """

from PySide2.QtWidgets import (QWidget, QHBoxLayout, QLabel, QSplitter, QVBoxLayout, QComboBox, QPushButton,
                               QTableWidget, QFrame, QAbstractItemView)
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

        # 日期间隔选项
        self.query_month_combobox = QComboBox(self)
        self.query_month_combobox.addItem("近三月", 3)
        self.query_month_combobox.addItem("近六月", 6)
        self.query_month_combobox.addItem("近一年", 12)
        opts_layout.addWidget(self.query_month_combobox)

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
        self.chart_data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        self.chart_data_table.setFocusPolicy(Qt.NoFocus)  # 去选中时的虚线框
        self.chart_data_table.setAlternatingRowColors(True)  # 交替行颜色
        self.chart_data_table.setFrameShape(QFrame.NoFrame)
        self.chart_data_table.setColumnCount(6)
        self.chart_data_table.setHorizontalHeaderLabels(["品种", "合约", "日期", "现货价", "收盘价", "基差"])
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

        self.tip_label.setObjectName("tipLabel")
        self.chart_data_table.setObjectName("dataTable")
        self.setStyleSheet(
            "#tipLabel{border:none;color:rgb(230,50,50);font-weight:bold}"
            "#dataTable{selection-color:rgb(255,255,255);selection-background-color:rgb(51,143,255);alternate-background-color:rgb(245,250,248)}"
        )
