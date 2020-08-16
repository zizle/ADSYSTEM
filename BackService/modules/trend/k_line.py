# _*_ coding:utf-8 _*_
# @File  : k_line.py
# @Time  : 2020-08-10 20:01
# @Author: zizle

""" K 线 把各交易所的分开写,易于后期拓展 """

from fastapi import APIRouter, Depends
from db.mysql_z import MySqlZ
from utils.contract import verify_variety, verify_contract

kline_router = APIRouter()


@kline_router.get("/kline/dce/{contract}/", summary="获取大连商品交易所合约的k线数据")
async def dce_variety_contract(contract: str = Depends(verify_contract)):
    # 查询数据库获取数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,`contract`,`open_price`,`close_price`,`highest`,`lowest` "
            "FROM dce_daily "
            "WHERE `contract`=%s AND `open_price`<>0 AND `close_price`<>0 AND `highest`<>0 AND `lowest`<>0 "
            "ORDER BY `date`;",
            contract
        )
        data = cursor.fetchall()
    return {"message": "查询大商所{}K线数据成功!".format(contract), "data": data}


@kline_router.get("/kline/czce/{contract}/", summary="获取郑州商品交易所合约的k线数据")
async def czce_variety_contract(contract: str = Depends(verify_contract)):
    # 查询数据库获取数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,`contract`,`open_price`,`close_price`,`highest`,`lowest` "
            "FROM czce_daily "
            "WHERE `contract`=%s AND `open_price`<>0 AND `close_price`<>0 AND `highest`<>0 AND `lowest`<>0 "
            "ORDER BY `date`;",
            contract
        )
        data = cursor.fetchall()
    return {"message": "查询郑商所{}K线数据成功!".format(contract), "data": data}


@kline_router.get("/kline/shfe/{contract}/", summary="获取上海期货交易所合约的k线数据")
async def shfe_variety_contract(contract: str = Depends(verify_contract)):
    # 查询数据库获取数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,`contract`,`open_price`,`close_price`,`highest`,`lowest` "
            "FROM shfe_daily "
            "WHERE `contract`=%s AND `open_price`<>0 AND `close_price`<>0 AND `highest`<>0 AND `lowest`<>0 "
            "ORDER BY `date`;",
            contract
        )
        data = cursor.fetchall()
    return {"message": "查询上期所{}K线数据成功!".format(contract), "data": data}


@kline_router.get("/kline/cffex/{contract}/", summary="获取中国金融期货交易所合约的k线数据")
async def cffex_variety_contract(contract: str = Depends(verify_contract)):
    # 查询数据库获取数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,`contract`,`open_price`,`close_price`,`highest`,`lowest` "
            "FROM cffex_daily "
            "WHERE `contract`=%s AND `open_price`<>0 AND `close_price`<>0 AND `highest`<>0 AND `lowest`<>0 "
            "ORDER BY `date`;",
            contract
        )
        data = cursor.fetchall()
    return {"message": "查询中金所{}K线数据成功!".format(contract), "data": data}


@kline_router.get("/kline/dce/{variety_en}/main-contract/", summary="获取大商所主力合约K线数据")
async def dce_variety_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.open_price,t.close_price,t.highest,t.lowest "
            "FROM (SELECT `date`,variety_en,contract,open_price,close_price,highest,lowest "
            "FROM dce_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "查询大商所{}主力合约数据成功!".format(variety_en), "data": data}


@kline_router.get("/kline/czce/{variety_en}/main-contract/", summary="获取郑商所主力合约K线数据")
async def czce_variety_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.open_price,t.close_price,t.highest,t.lowest "
            "FROM (SELECT `date`,variety_en,contract,open_price,close_price,highest,lowest "
            "FROM czce_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "查询郑商所{}主力合约数据成功!".format(variety_en), "data": data}


@kline_router.get("/kline/shfe/{variety_en}/main-contract/", summary="获取上期所主力合约K线数据")
async def shfe_variety_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.open_price,t.close_price,t.highest,t.lowest "
            "FROM (SELECT `date`,variety_en,contract,open_price,close_price,highest,lowest "
            "FROM shfe_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "查询上期所{}主力合约数据成功!".format(variety_en), "data": data}


@kline_router.get("/kline/cffex/{variety_en}/main-contract/", summary="获取中金所主力合约K线数据")
async def cffex_variety_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.open_price,t.close_price,t.highest,t.lowest "
            "FROM (SELECT `date`,variety_en,contract,open_price,close_price,highest,lowest "
            "FROM cffex_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "查询中金所{}主力合约数据成功!".format(variety_en), "data": data}
