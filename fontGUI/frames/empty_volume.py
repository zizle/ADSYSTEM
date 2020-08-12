# _*_ coding:utf-8 _*_
# @File  : empty_volume.py
# @Time  : 2020-08-11 21:18
# @Author: zizle
import json
from PySide2.QtWidgets import QApplication
from PySide2.QtNetwork import QNetworkRequest
from PySide2.QtCore import QUrl
from configs import SERVER
from .empty_volume_ui import EmptyVolumeUI


class EmptyVolume(EmptyVolumeUI):

    def __init__(self, *args, **kwargs):
        super(EmptyVolume, self).__init__(*args, **kwargs)
        self.current_variety = None                                            # 当前选择的品种
        self.current_exchange = None                                           # 当前品种所属交易所
        self.current_source = "daily"                                          # 当前选择的数据源(日行情统计OR持仓排名)
        self.variety_tree.selected_signal.connect(self.click_variety)          # 选择品种
        self.radio_button_group.buttonClicked.connect(self.change_daily_rank)  # 改变目标数据源
        self.confirm_button.clicked.connect(self.get_empty_volume_data)        # 确定查询数据生成图形

    def click_variety(self, variety_en, exchange_name):
        """ 左侧选择品种 """
        self.current_variety = variety_en                                      # 赋值类属性
        self.current_exchange = exchange_name
        self.contract_combobox.clear()                                         # 清空合约下拉选项,并请求当前品种的所有合约
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
        reply.deleteLater()
        self.contract_combobox.addItem("主力合约")
        for contract in data["contracts"]:
            self.contract_combobox.addItem(contract)
        reply.deleteLater()

    def change_daily_rank(self, radio_button):
        """ 目标数据源选择改变 """
        self.current_source = "daily" if radio_button.text() == "行情统计" else "rank"

    def get_empty_volume_data(self):
        """ 获取持仓分析数据 """
        current_contract = self.contract_combobox.currentText()
        print(current_contract, self.current_source, self.rank_spinbox.value())