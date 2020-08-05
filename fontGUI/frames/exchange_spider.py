# _*_ coding:utf-8 _*_
# @File  : exchange_spider.py
# @Time  : 2020-07-22 21:00
# @Author: zizle

from .exchange_spider_ui import ExchangeSpiderUI


class ExchangeSpider(ExchangeSpiderUI):
    """ 数据抓取业务 """
    def __init__(self, *args, **kwargs):
        super(ExchangeSpider, self).__init__(*args, **kwargs)
        self.tree_widget.selected_signal.connect(self.selected_action)  # 树控件点击事件

    def __del__(self):
        print("~数据抓取窗口析构了")

    def selected_action(self, exchange, action):
        """ 树控件菜单点击传出信号 """
        print(exchange, action)



