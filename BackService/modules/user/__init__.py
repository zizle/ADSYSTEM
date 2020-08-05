# _*_ coding:utf-8 _*_
# @File  : __init__.py.py
# @Time  : 2020-07-19 10:08
# @Author: zizle

from fastapi import APIRouter
from .passport import passport_router


user_router = APIRouter()
user_router.include_router(passport_router)
