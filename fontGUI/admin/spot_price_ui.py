# _*_ coding:utf-8 _*_
# @File  : spot_price_ui.py
# @Time  : 2020-08-25 14:56
# @Author: zizle


from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QDateEdit
from PySide2.QtCore import QDate


class SpotPriceUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(SpotPriceUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        # 现货价格源数据
        source_layout = QHBoxLayout()
        self.current_date = QDateEdit(self)
        self.current_date.setDisplayFormat("yyyy-MM-dd")
        self.current_date.setDate(QDate.currentDate())
        self.current_date.setCalendarPopup(True)
        source_layout.addWidget(self.current_date)

        source_layout.addWidget(QLabel("源数据:", self))
        self.source_edit = QLineEdit(self)
        source_layout.addWidget(self.source_edit)
        layout.addLayout(source_layout)
        # 分析
        analysis_layout = QHBoxLayout()
        self.analysis_button = QPushButton("提取数据", self)
        analysis_layout.addWidget(self.analysis_button)

        self.tip_label = QLabel("输入源数据后,点击分析数据进行数据提取.", self)
        analysis_layout.addWidget(self.tip_label)
        analysis_layout.addStretch()
        layout.addLayout(analysis_layout)

        # 预览数据的表格
        self.preview_table = QTableWidget(self)
        self.preview_table.setColumnCount(5)
        self.preview_table.setHorizontalHeaderLabels(["日期", "品种", "交易代码", "现货价", "增减"])
        layout.addWidget(self.preview_table)

        # 提交按钮
        commit_layout = QHBoxLayout()
        commit_layout.addStretch()
        self.commit_button = QPushButton("确认提交", self)
        commit_layout.addWidget(self.commit_button)
        layout.addLayout(commit_layout)

        self.setLayout(layout)


