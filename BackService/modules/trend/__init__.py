# _*_ coding:utf-8 _*_
# @File  : __init__.py.py
# @Time  : 2020-08-10 20:01
# @Author: zizle
""" 数据分析模块 """

from fastapi import APIRouter
from .k_line import kline_router
from .empty_volume import empty_volume_router

trend_router = APIRouter()
trend_router.include_router(kline_router)
trend_router.include_router(empty_volume_router)
