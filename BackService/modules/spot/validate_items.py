# _*_ coding:utf-8 _*_
# @File  : validate_items.py
# @Time  : 2020-08-25 16:31
# @Author: zizle
from pydantic import BaseModel


class SpotPriceItem(BaseModel):
    date: str
    variety_en: str
    spot_price: float
    price_increase: float


class ModifySpotItem(SpotPriceItem):
    id: int
