# _*_ coding:utf-8 _*_
# @File  : basis.py
# @Time  : 2020-08-26 16:31
# @Author: zizle
import json
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import QUrl, Qt, QTimer
from PySide2.QtNetwork import QNetworkRequest
from PySide2.QtWebChannel import QWebChannel
from configs import SERVER
from utils.constant import VARIETY_ZH
from channel.basis import BasisPageChannel
from .basis_ui import BasisUI


class Basis(BasisUI):
    def __init__(self, *args, **kwargs):
        super(Basis, self).__init__(*args, **kwargs)
        self.current_variety = None
        self.current_exchange = None
        self.basis_chart_title = ""

        self.chart_view.load(QUrl("file:///pages/basis.html"))

        # 设置与页面信息交互的通道
        channel_qt_obj = QWebChannel(self.chart_view.page())                     # 实例化qt信道对象,必须传入页面参数
        self.contact_channel = BasisPageChannel()                                   # 页面信息交互通道
        self.chart_view.page().setWebChannel(channel_qt_obj)
        channel_qt_obj.registerObject("pageContactChannel", self.contact_channel)   # 信道对象注册信道，只能注册一个

        self.tips_animation_timer = QTimer(self)  # 显示文字提示的timer
        self.tips_animation_timer.timeout.connect(self.animation_tip_text)

        self.variety_tree.selected_signal.connect(self.click_variety)   # 获取当前品种的所有合约
        self.query_button.clicked.connect(self.query_contract_basis)    # 获取合约基差数据

        self.query_month_combobox.currentTextChanged.connect(self.query_contract_basis)  # 日期范围变化

    def animation_tip_text(self):
        """ 动态展示查询文字提示 """
        tips = self.tip_label.text()
        tip_points = tips.split(' ')[1]
        if len(tip_points) > 2:
            self.tip_label.setText("正在查询相关数据 ")
        else:
            self.tip_label.setText("正在查询相关数据 " + "·" * (len(tip_points) + 1))

    def click_variety(self, variety_en, exchange_lib):
        """ 点击选择品种 """
        # 赋值属性
        self.current_variety = variety_en
        self.current_exchange = exchange_lib
        self.contract_combobox.clear()  # 清空合约选择下拉项
        # 发送请求获取当前品种所有交割月份合约
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + "{}/{}/contracts/".format(exchange_lib, variety_en)
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.variety_contracts_reply)

    def variety_contracts_reply(self):
        """ 当前品种下的合约返回 """
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        self.contract_combobox.addItem("主力合约")
        for contract in data["contracts"]:
            self.contract_combobox.addItem(contract)
        reply.deleteLater()

    def query_contract_basis(self):
        """ 获取合约的基差数据 """
        self.chart_data_table.clearContents()  # 清空表格数据内容
        self.chart_data_table.setRowCount(0)   # 行数清空

        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        contract = self.contract_combobox.currentText()
        query_month = self.query_month_combobox.currentData()
        if not contract:
            self.tip_label.setText("选择对应品种和合约后查询数据. ")
            return
        self.tips_animation_timer.start(400)  # 开启文字提示
        self.chart_view.setUpdatesEnabled(False)

        if contract == "主力合约":
            self.basis_chart_title = self.current_variety + "主力合约基差"
            url = SERVER + "trend/contract-basis/{}/{}/main-contract/?query_month={}".format(self.current_exchange, self.current_variety, query_month)
        else:
            self.basis_chart_title = self.contract_combobox.currentText() + "基差"
            url = SERVER + "trend/contract-basis/{}/{}/?query_month={}".format(self.current_exchange, contract, query_month)
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.basis_data_reply)

    def basis_data_reply(self):
        """ 合约基差数据返回 """
        reply = self.sender()
        if reply.error():
            self.tips_animation_timer.stop()
            self.tip_label.setText("查询数据失败:{} ".format(reply.error()))
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        basis_data = json.dumps(data["data"])
        reply.deleteLater()
        self.chart_view.setUpdatesEnabled(True)
        self.contact_channel.basis_data.emit(basis_data, self.basis_chart_title)  # 将数据传输到网页中绘图(字符串型,dict型无法接收)
        self.tip_label.setText("基差数据查询成功! ")
        self.tips_animation_timer.stop()
        # 将数据显示到表格中
        for row, row_item in enumerate(data["data"]):
            self.chart_data_table.insertRow(row)
            item0 = QTableWidgetItem(VARIETY_ZH.get(row_item["variety_en"], "未知"))
            item1 = QTableWidgetItem(row_item["contract"])
            item2 = QTableWidgetItem(row_item["date"])
            item3 = QTableWidgetItem(str(row_item["spot_price"]))
            item4 = QTableWidgetItem(str(row_item["close_price"]))
            item5 = QTableWidgetItem(str(row_item["spot_price"] - row_item["close_price"]))
            item0.setTextAlignment(Qt.AlignCenter)
            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            item3.setTextAlignment(Qt.AlignCenter)
            item4.setTextAlignment(Qt.AlignCenter)
            item5.setTextAlignment(Qt.AlignCenter)
            self.chart_data_table.setItem(row, 0, item0)
            self.chart_data_table.setItem(row, 1, item1)
            self.chart_data_table.setItem(row, 2, item2)
            self.chart_data_table.setItem(row, 3, item3)
            self.chart_data_table.setItem(row, 4, item4)
            self.chart_data_table.setItem(row, 5, item5)
