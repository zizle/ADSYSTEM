# _*_ coding:utf-8 _*_
# @File  : contract_kei.py
# @Time  : 2020-08-07 14:26
# @Author: zizle
import json
from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout
from PySide2.QtNetwork import QNetworkRequest
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtCore import QUrl
from channel.kline import KlinePageChannel
from configs import SERVER
from .contract_kei_ui import ContractKeiUI


class ContractKei(ContractKeiUI):
    """ 合约K先业务"""
    current_variety = None
    current_exchange = None

    def __init__(self, *args, **kwargs):
        super(ContractKei, self).__init__(*args, **kwargs)
        self.web_container.load(QUrl("file:///pages/kline.html"))
        # 设置与页面信息交互的通道
        channel_qt_obj = QWebChannel(self.web_container.page())                    # 实例化qt信道对象,必须传入页面参数
        self.contact_channel = KlinePageChannel()                                  # 页面信息交互通道
        self.web_container.page().setWebChannel(channel_qt_obj)
        channel_qt_obj.registerObject("pageContactChannel", self.contact_channel)  # 信道对象注册信道，只能注册一个

        self.variety_tree.selected_signal.connect(self.click_variety)              # 选择品种请求当前品种的合约
        self.confirm_button.clicked.connect(self.get_kline_data)                   # 确定获取品种下的K线数据
        self.main_contract.clicked.connect(self.get_main_contract_kline_data)      # 获取主力合约K线数据

    def click_variety(self, variety_en, exchange_name):
        """ 点击选择了品种 """
        # 赋值类属性
        self.current_variety = variety_en
        self.current_exchange = exchange_name
        self.contract_combobox.clear()  # 清空合约选择下拉项
        # 发送请求获取当前品种所有交割月份合约
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + "contracts/?variety_en={}&exchange={}".format(variety_en, exchange_name)
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
        for contract in data["contracts"]:
            self.contract_combobox.addItem(contract)
        reply.deleteLater()

    def get_kline_data(self):
        """ 获取当前品种当前合约下的K线数据 """
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        contract = self.contract_combobox.currentText()
        url = SERVER + "trend/kline/?contract={}&exchange={}".format(contract, self.current_exchange)
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.kline_data_reply)

    def kline_data_reply(self):
        """ K线数据返回 """
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        kline_data = json.dumps(data["data"])
        reply.deleteLater()
        title = self.contract_combobox.currentText() + "日K线图"
        self.contact_channel.kline_data.emit(kline_data, title)  # 将数据传输到网页中绘图(字符串型,dict型无法接收)

    def get_main_contract_kline_data(self):
        """ 获取品种主力合约K线数据 """
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + "trend/kline/main-contract/?variety_en={}&exchange={}".format(self.current_variety, self.current_exchange)
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.main_contract_kline_data_reply)

    def main_contract_kline_data_reply(self):
        """ 主力合约K线数据返回 """
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        kline_data = json.dumps(data["data"])
        reply.deleteLater()
        title = self.current_variety + "主力合约K线图"
        self.contact_channel.kline_data.emit(kline_data, title)  # 将数据传输到网页中绘图(字符串型,dict型无法接收)

