# _*_ coding:utf-8 _*_
# @File  : empty_volume.py
# @Time  : 2020-08-11 21:18
# @Author: zizle
import json
from PySide2.QtWidgets import QApplication
from PySide2.QtNetwork import QNetworkRequest
from PySide2.QtCore import QUrl, QTimer
from PySide2.QtWebChannel import QWebChannel
from channel.position import PositionPageChannel
from configs import SERVER
from .empty_volume_ui import EmptyVolumeUI


class EmptyVolume(EmptyVolumeUI):

    def __init__(self, *args, **kwargs):
        super(EmptyVolume, self).__init__(*args, **kwargs)
        self.current_variety = None                                            # 当前选择的品种
        self.current_exchange = None                                           # 当前品种所属交易所
        self.current_source = "daily"                                          # 当前选择的数据源(日行情统计OR持仓排名)
        self.tips_animation_timer = QTimer(self)                               # 显示文字提示的timer
        self.tips_animation_timer.timeout.connect(self.animation_tip_text)

        self.position_line_title = "持仓分析"                                          # 分合约日线和主力合约
        self.web_container.load(QUrl("file:///pages/position_line.html"))
        # 设置与页面信息交互的通道
        channel_qt_obj = QWebChannel(self.web_container.page())                # 实例化qt信道对象,必须传入页面参数
        self.contact_channel = PositionPageChannel()                           # 页面信息交互通道
        self.web_container.page().setWebChannel(channel_qt_obj)
        channel_qt_obj.registerObject("pageContactChannel", self.contact_channel)

        self.variety_tree.selected_signal.connect(self.click_variety)          # 选择品种
        self.radio_button_group.buttonClicked.connect(self.change_daily_rank)  # 改变目标数据源
        self.confirm_button.clicked.connect(self.get_empty_volume_data)        # 确定查询数据生成图形

    def animation_tip_text(self):
        """ 动态展示查询文字提示 """
        tips = self.tip_button.text()
        tip_points = tips.split(' ')[1]
        if len(tip_points) > 2:
            self.tip_button.setText("正在查询数据 ")
        else:
            self.tip_button.setText("正在查询数据 " + "·" * (len(tip_points) + 1))

    def click_variety(self, variety_en, exchange_lib):
        """ 左侧选择品种 """
        self.current_variety = variety_en                                      # 赋值类属性
        self.current_exchange = exchange_lib
        self.contract_combobox.clear()                                         # 清空合约下拉选项,并请求当前品种的所有合约
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + "{}/{}/contracts/".format(self.current_exchange, self.current_variety)
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
        if radio_button.text() == "行情统计":
            self.current_source = "daily"
            self.rank_spinbox.hide()
        else:
            self.current_source = "rank"
            self.rank_spinbox.show()

    def get_empty_volume_data(self):
        """ 获取持仓分析数据 """
        self.tip_button.show()
        self.tips_animation_timer.start(400)

        source_text = "行情统计" if self.current_source == "daily" else "前{}排名".format(self.rank_spinbox.value())
        current_contract = self.contract_combobox.currentText()
        if current_contract == "主力合约":
            url = SERVER + "trend/{}-position/{}/{}/main-contract/".format(self.current_source, self.current_exchange, self.current_variety)
            self.position_line_title = "{}{}主力合约持仓分析".format(self.current_variety, source_text)
        else:
            url = SERVER + 'trend/{}-position/{}/{}/'.format(self.current_source, self.current_exchange, current_contract)
            self.position_line_title = "{}{}持仓分析".format(current_contract,source_text)
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.position_data_reply)

    def position_data_reply(self):
        """ 目标持仓数据返回 """
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        position_data = json.dumps(data["data"])
        reply.deleteLater()
        self.contact_channel.position_data.emit(position_data, self.position_line_title)  # 将数据传输到网页中绘图(字符串型,dict型无法接收)

        self.tips_animation_timer.stop()
        self.tip_button.setText("数据查询成功! ")


