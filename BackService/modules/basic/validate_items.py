# _*_ coding:utf-8 _*_
# @File  : validate_items.py
# @Time  : 2020-08-10 14:36
# @Author: zizle
from enum import Enum
from pydantic import BaseModel
#
# EXCHANGE_LIB = {"czce": "郑州商品交易所", "dce": "大连商品交易所",
#                 "cffex": "中国金融期货交易所",
#                 "shfe": "上海期货交易所", "ine": "上海国际能源中心"}


class ExchangeLib(Enum):
    shfe: str = "上海期货交易所"
    czce: str = "郑州商品交易所"
    dce: str = "大连商品交易所"
    cffex: str = "中国金融期货交易所"
    ine: str = "上海国际能源中心"


class VarietyGroup(Enum):
    finance: str = "金融股指"
    farm: str = "农副产品"
    chemical: str = "能源化工"
    metal: str = "金属产业"


class VarietyItem(BaseModel):
    """ 添加品种的验证项 """
    variety_name: str
    variety_en: str
    exchange_lib: ExchangeLib
    group_name: VarietyGroup
