# _*_ coding:utf-8 _*_
# @File  : param_items.py
# @Time  : 2020-07-24 8:02
# @Author: zizle
from collections import OrderedDict
from enum import Enum


class ExchangeName(Enum):
    """ exchange_name 参数枚举 """
    shfe = "shfe"
    czce = "czce"
    cffex = "cffex"
    dce = "dce"


class CategoryName(Enum):
    """ category_name 参数枚举"""
    daily = "daily"
    rank = "rank"
    receipt = "receipt"


QUERY_OPTIONS = {
    "czce": {
        "daily": {
            "detail_query": "SELECT * FROM `czce_daily` WHERE `date`={};",
            "detail_keys": OrderedDict({
                "id": "ID", "date": "日期", "contract": "合约", "pre_settlement": "前结算", "open_price": "开盘价", "highest": "最高价",
                "lowest": "最低价", "close_price": "收盘价", "zd_1": "涨跌1", "zd_2": "涨跌2", "trade_volume": "成交量", "empty_volume": "空盘量",
                "increase_volume": "增减量", "trade_price": "成交额", "delivery_price": "交割结算价"
            }),
            "sum_query": "SELECT `date`,variety_en,sum(trade_volume) as total_trade_volume," \
                         "sum(empty_volume) as total_empty_volume, sum(increase_volume) as total_increase_volume " \
                         "FROM `czce_daily` WHERE `date`={} GROUP BY variety_en;",
            "sum_keys": OrderedDict({
                "date": "日期", "variety_en": "品种", "total_trade_volume": "成交量合计(手)",
                "total_empty_volume": "空盘量合计", "total_increase_volume": "增减量合计"
            }),
        },
        "receipt": {
            "detail_query": "SELECT * FROM `czce_receipt` WHERE `date`={};",
            "detail_keys": OrderedDict({
                "id": "ID", "date": "日期", "variety": "品种", "variety_en": "代码", "warehouse": "仓库简称", "receipt": "仓单",
                "increase": "增减", "premium_discount": "升贴水"
            }),
            "sum_query": "SELECT `date`, `variety`, `variety_en`, sum(receipt) AS total_receipt,"
                         "sum(increase) AS total_increase FROM `czce_receipt` WHERE `date`={} GROUP BY `variety_en`;",
            "sum_keys": OrderedDict({
                "date": "日期", "variety": "品种", "variety_en": "代码", "total_receipt": "仓单合计", "total_increase": "增减合计"
            })
        }
    },

}
