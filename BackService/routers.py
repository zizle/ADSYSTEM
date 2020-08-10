# _*_ coding:utf-8 _*_
# @File  : routers.py
# @Time  : 2020-07-19 10:15
# @Author: zizle

from fastapi import APIRouter
from modules.basic import basic_router
from modules.user import user_router
from modules.exchange_lib import exchange_router
from modules.update import update_router
from modules.trend import trend_router

router = APIRouter()
router.include_router(basic_router, tags=["基础信息"])
router.include_router(user_router, tags=["用户"])
router.include_router(exchange_router, tags=["交易所数据"])
router.include_router(trend_router, prefix="/trend", tags=["数据分析"])
router.include_router(update_router, tags=["系统更新"])

