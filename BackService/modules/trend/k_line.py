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
        raise HTTPException(detail="Invalidate Contract!", status_code=400)
    # 查询数据库获取数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,`contract`,`open_price`,`close_price`,`highest`,`lowest` "
            "FROM {}_daily "
            "WHERE `contract`=%s AND `open_price`<>0 AND `close_price`<>0 AND `highest`<>0 AND `lowest`<>0 "
            "ORDER BY `date`;".format(exchange.name),
            contract
        )
        data = cursor.fetchall()
    return {"message": "查询成功!", "data": data}


@kline_router.get("/kline/main-contract/", summary="获取某品种的主力合约K线数据")
async def variety_main_contract(variety_en: str = Query(...), exchange: ExchangeLib = Query(...)):
    if not re.match(r"^[A-Z]{1,2}$", variety_en):
        raise HTTPException(detail="Invalidate Variety_EN!", status_code=400)
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.open_price,t.close_price,t.highest,t.lowest "
            "FROM {}_daily AS t,"
            "(SELECT max(empty_volume) AS max_empty_volume FROM {}_daily WHERE `variety_en`=%s GROUP BY `date`) AS main_contract "
            "WHERE t.empty_volume=main_contract.max_empty_volume AND t.variety_en=%s "
            "ORDER BY t.date;".format(exchange.name, exchange.name),
            (variety_en, variety_en)
        )
        data = cursor.fetchall()
    for i in data:
        print(i)
    return {"message": "查询主力合约数据成功!", "data": data}
