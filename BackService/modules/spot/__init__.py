# _*_ coding:utf-8 _*_
# @File  : __init__.py.py
# @Time  : 2020-08-25 16:08
# @Author: zizle
from fastapi import APIRouter
from .spot_price import price_router

spot_router = APIRouter()
spot_router.include_router(price_router)
