# _*_ coding:utf-8 _*_
# @File  : k_line.py
# @Time  : 2020-08-10 20:01
# @Author: zizle

""" K 线"""
import re
from fastapi import APIRouter, Query, HTTPException
from modules.basic.validate_items import ExchangeLib
from db.mysql_z import MySqlZ

kline_router = APIRouter()


@kline_router.get("/kline/", summary="获取某合约的k线数据")
async def variety_contract(contract: str = Query(...), exchange: ExchangeLib = Query(...)):
    if not re.match(r"^[A-Z0-9]{5,6}$", contract):
        raise HTTPException(detail="Got an error contract!", status_code=400)
    # 查询数据库获取数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,`contract`,`open_price`,`close_price`,`highest`,`lowest` "
            "FROM {}_daily WHERE `contract`=%s "
            "ORDER BY `date`;".format(exchange.name),
            contract
        )
        data = cursor.fetchall()
    return {"message": "查询成功!", "data": data}
