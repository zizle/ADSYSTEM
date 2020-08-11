# _*_ coding:utf-8 _*_
# @File  : contract_option.py
# @Time  : 2020-08-11 21:11
# @Author: zizle

""" 合约选择控件 """
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton


class ContractSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super(ContractSelector, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("选择合约:", self))
        self.contract_combobox = QComboBox(self)
        layout.addWidget(self.contract_combobox)
        self.confirm_button = QPushButton("确定", self)
        layout.addWidget(self.confirm_button)
        layout.addStretch()
        self.setLayout(layout)

        self.contract_combobox.setMinimumWidth(80)
        self.setMaximumHeight(60)

    def clear(self):
        """ 清空选项 """
        self.contract_combobox.clear()

    def set_contracts(self, contracts: list):
        self.contract_combobox.addItem("主力合约")
        for contract_item in contracts:
            self.contract_combobox.addItem(contract_item)


