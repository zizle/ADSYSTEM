# _*_ coding:utf-8 _*_
# @File  : basis.py
# @Time  : 2020-08-26 16:31
# @Author: zizle
import json
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtNetwork import QNetworkRequest
from .basis_ui import BasisUI
from configs import SERVER


class Basis(BasisUI):
    def __init__(self, *args, **kwargs):
        super(Basis, self).__init__(*args, **kwargs)
        self.current_variety = None
        self.current_exchange = None
        self.basis_chart_title = ""

        self.chart_view.load(QUrl("file:///pages/basis.html"))

        self.variety_tree.selected_signal.connect(self.click_variety)   # 获取当前品种的所有合约
        self.query_button.clicked.connect(self.query_contract_basis)    # 获取合约基差数据

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
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        contract = self.contract_combobox.currentText()

        if contract == "主力合约":
            self.basis_chart_title = self.current_variety + "主力合约基差"
            url = SERVER + "trend/contract-basis/{}/{}/main-contract/".format(self.current_exchange, self.current_variety)
        else:
            self.basis_chart_title = self.contract_combobox.currentText() + "基差"
            url = SERVER + "trend/contract-basis/{}/{}/".format(self.current_exchange, contract)
        print(url)
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.basis_data_reply)

    def basis_data_reply(self):
        """ 合约基差数据返回 """
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        print(data)
        basis_data = json.dumps(data["data"])

        reply.deleteLater()
        # self.web_container.setUpdatesEnabled(True)
        # self.contact_channel.kline_data.emit(kline_data, self.kline_title)  # 将数据传输到网页中绘图(字符串型,dict型无法接收)
        # self.tip_button.setText("查询成功! ")
        # self.tips_animation_timer.stop()