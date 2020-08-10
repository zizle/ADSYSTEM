# _*_ coding:utf-8 _*_
# @File  : __init__.py.py
# @Time  : 2020-08-10 14:14
# @Author: zizle
from fastapi import APIRouter
from .variety import variety_router


basic_router = APIRouter()
basic_router.include_router(variety_router)
