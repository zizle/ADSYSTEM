# _*_ coding:utf-8 _*_
# @File  : exchange_query.py
# @Time  : 2020-07-23 15:46
# @Author: zizle
import json
from PySide2.QtWidgets import QApplication, QTableWidgetItem
from PySide2.QtCore import Qt
from PySide2.QtNetwork import QNetworkRequest
from .exchange_query_ui import ExchangeQueryUI
from configs import SERVER


class ExchangeQuery(ExchangeQueryUI):
    """ 查询数据的业务 """
    _exchange_lib = {
        "cffex": "中国金融期货交易所",
        "shfe": "上海期货交易所",
        "czce": "郑州商品交易所",
        "dce": "大连商品交易所"
    }
    _actions = {
        "daily": "日交易数据",
        "rank": "日交易排名",
        "receipt": "每日仓单"
    }

    def __init__(self, *args, **kwargs):
        super(ExchangeQuery, self).__init__(*args, **kwargs)

        self.current_exchange = None
        self.current_action = None
        self.exchange_tree.selected_signal.connect(self.selected_action)       # 树控件点击事件
        self.exchange_tree.unselected_signal.connect(self.unselected_any)      # 没有选择项目
        self.query_button.clicked.connect(self.query_target_data)              # 查询合约详情数据
        self.query_variety_sum_button.clicked.connect(self.query_variety_sum)  # 查询品种合计数

    def is_allow_query(self):
        """ 是否允许查询判断函数 """
        self.tip_label.show()
        if self.current_exchange is None or self.current_action is None:
            self.tip_label.setText("左侧选择想要查询的数据类别再进行查询.")
            return False
        else:
            self.tip_label.setText("正在查询相关数据···")
            return True

    def selected_action(self, exchange, action):
        """ 目录树点击信号 """
        self.current_exchange = exchange
        self.current_action = action
        if self.current_action == "rank":
            self.rank_select.show()
        else:
            self.rank_select.hide()

    def unselected_any(self):
        """ 没有选择项目 """
        self.current_exchange = None
        self.current_action = None

    def query_target_data(self):
        """ 点击确定查询合约详情目标数据 """
        if not self.is_allow_query():
            return
        # 清除table
        self.show_table.clear()
        self.show_table.setRowCount(0)
        self.show_table.setColumnCount(0)
        # 查询数据进行展示
        current_date = self.query_date_edit.text()
        app = QApplication.instance()
        network_manger = getattr(app, "_network")

        url = SERVER + "exchange/" + self.current_exchange + "/" + self.current_action + "/?date=" + current_date
        request = QNetworkRequest(url=url)
        reply = network_manger.get(request)
        reply.finished.connect(self.query_result_reply)

    def query_variety_sum(self):
        """ 查询各品种的合计数 """
        if not self.is_allow_query():
            return
        # 清除table
        self.show_table.clear()
        self.show_table.setRowCount(0)
        self.show_table.setColumnCount(0)
        # 查询数据进行展示
        current_date = self.query_date_edit.text()
        app = QApplication.instance()
        network_manger = getattr(app, "_network")

        url = SERVER + "exchange/" + self.current_exchange + "/" + self.current_action + "/variety-sum/?date=" + current_date
        if self.rank_select.isEnabled():
            url += "&rank=" + str(self.rank_select.value())
        request = QNetworkRequest(url=url)
        reply = network_manger.get(request)
        reply.finished.connect(self.query_result_reply)

    def query_result_reply(self):
        """ 请求数据返回结果 """
        reply = self.sender()
        if reply.error():
            self.tip_label.setText("失败:{}".format(reply.error()))
            return
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        reply.deleteLater()
        self.tip_label.setText("查询成功!")
        self.show_table_fill_contents(data['content_keys'], data["result"])  # 数据表显示数据

    def show_table_fill_contents(self, headers, contents):
        """ 查询到的数据填到表格中 """
        self.show_table.setColumnCount(len(headers))
        self.show_table.setRowCount(len(contents))
        headers_keys = list()
        headers_labels = list()
        for key, value in headers.items():
            headers_keys.append(key)
            headers_labels.append(value)
        self.show_table.setHorizontalHeaderLabels(headers_labels)
        for row, row_item in enumerate(contents):
            self.show_table.setRowHeight(row, 20)
            for col, value_key in enumerate(headers_keys):
                item = QTableWidgetItem(str(row_item[value_key]))
                item.setTextAlignment(Qt.AlignCenter)
                self.show_table.setItem(row, col, item)
