# _*_ coding:utf-8 _*_
# @File  : empty_volume_ui.py
# @Time  : 2020-08-11 21:06
# @Author: zizle

""" 持仓分析界面 """
from PySide2.QtWidgets import (QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QButtonGroup,
                               QRadioButton, QSpinBox, QFrame)
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

        # 选择分析的目标数据类别
        self.radio_button_group = QButtonGroup(self)
        radio_button_1 = QRadioButton("行情统计", self)
        radio_button_1.setChecked(True)
        self.radio_button_group.addButton(radio_button_1)
        radio_button_2 = QRadioButton("排名持仓", self)
        self.radio_button_group.addButton(radio_button_2)
        opts_layout.addWidget(radio_button_1)
        opts_layout.addWidget(radio_button_2)
        self.rank_spinbox = QSpinBox(self)
        self.rank_spinbox.setPrefix("前 ")
        self.rank_spinbox.setSuffix(" 名")
        self.rank_spinbox.setRange(1, 20)
        self.rank_spinbox.setValue(20)
        self.rank_spinbox.hide()
        opts_layout.addWidget(self.rank_spinbox)
        # 分割线
        vertical_line = QFrame(self)
        vertical_line.setFrameShape(QFrame.VLine)
        opts_layout.addWidget(vertical_line)

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