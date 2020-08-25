# _*_ coding:utf-8 _*_
# @File  : spot_price.py
# @Time  : 2020-08-25 15:01
# @Author: zizle
import re
import json
from datetime import datetime
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtGui import QBrush, QColor
from PySide2.QtNetwork import QNetworkRequest
from .spot_price_ui import SpotPriceUI
from utils.constant import VARIETY_EN
from configs import SERVER


class SpotPrice(SpotPriceUI):
    def __init__(self, *args, **kwargs):
        super(SpotPrice, self).__init__(*args, **kwargs)
        self.final_data = list()   # 最终现货数据
        self.today_str = ""
        self.analysis_button.clicked.connect(self.extract_spot_source_price)  # 提取数据
        self.commit_button.clicked.connect(self.commit_spot_data)             # 上传提交数据

    def extract_spot_source_price(self):
        """ 提取现货数据 """
        self.final_data.clear()
        current_date = self.current_date.text()
        self.today_str = datetime.strptime(current_date, "%Y-%m-%d").strftime("%Y%m%d")
        source_str = self.source_edit.text().strip()
        if not source_str:
            self.tip_label.setText("请输入源数据再进行提取! ")
            return
        self.tip_label.setText("正在提取数据... ")
        variety_item_list = re.split(r'[;；]+', source_str)  # 根据分号切割
        for row, variety_item in enumerate(variety_item_list):
            data_list = re.split(r'[:,：，]+', variety_item)
            variety_dict = {
                "date": self.today_str,
                "variety_en": VARIETY_EN.get(data_list[0], "未知"),
                "spot_price": float(data_list[1]),
                "price_increase": float(data_list[2])
            }

            self.preview_table.insertRow(row)
            item0 = QTableWidgetItem(variety_dict["date"])
            self.preview_table.setItem(row, 0, item0)
            item1 = QTableWidgetItem(data_list[0])
            self.preview_table.setItem(row, 1, item1)
            item2 = QTableWidgetItem(variety_dict["variety_en"])
            self.preview_table.setItem(row, 2, item2)
            item3 = QTableWidgetItem(str(variety_dict["spot_price"]))
            self.preview_table.setItem(row, 3, item3)
            item4 = QTableWidgetItem(str(variety_dict["price_increase"]))
            self.preview_table.setItem(row, 4, item4)
            if variety_dict["variety_en"] == "未知":
                item0.setForeground(QBrush(QColor(250, 100, 100)))
                item1.setForeground(QBrush(QColor(250, 100, 100)))
                item2.setForeground(QBrush(QColor(250, 100, 100)))
                item3.setForeground(QBrush(QColor(250, 100, 100)))
                item4.setForeground(QBrush(QColor(250, 100, 100)))

            self.final_data.append(variety_dict)

        self.tip_label.setText("数据提取完成! ")

    def commit_spot_data(self):
        """ 提交数据 """
        self.tip_label.setText("正在上传数据到服务器...")
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + "spot/price/?date=" + self.today_str
        request = QNetworkRequest(url=url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json;charset=utf-8")

        reply = network_manager.post(request, json.dumps(self.final_data).encode("utf-8"))
        reply.finished.connect(self.save_spot_price_reply)

    def save_spot_price_reply(self):
        """ 保存数据返回 """
        reply = self.sender()
        data = reply.readAll().data()
        reply.deleteLater()
        if reply.error():
            self.tip_label.setText("保存{}现货动态数据数据库失败:\n{}".format(self.today_str, reply.error()))
        else:
            data = json.loads(data.decode("utf-8"))
            self.tip_label.setText(data["message"])




