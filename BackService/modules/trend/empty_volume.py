# _*_ coding:utf-8 _*_
# @File  : empty_volume.py
# @Time  : 2020-08-16 21:51
# @Author: zizle

""" 持仓量分析
trade_volume: 成交量
empty_volume: 行情持仓为持仓量;统计持仓为净持仓量
close_price: 收盘价
"""

from fastapi import APIRouter, Depends, Query
from utils.contract import verify_contract, verify_variety
from db.mysql_z import MySqlZ

empty_volume_router = APIRouter()

""" 大商所 """


@empty_volume_router.get("/daily-position/dce/{contract}/", summary="大商所合日行情合约持仓量")
async def dce_daily_position(contract: str = Depends(verify_contract)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,contract,trade_volume,empty_volume,close_price "
            "FROM dce_daily "
            "WHERE contract=%s "
            "ORDER BY `date`;",
            (contract,)
        )
        data = cursor.fetchall()
        return {"message": "大商所日行情的{}持仓数据!".format(contract), "data": data}


@empty_volume_router.get("/daily-position/dce/{variety_en}/main-contract/", summary="大商所日行情主力合约持仓量")
async def dce_daily_position_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.trade_volume,t.empty_volume,t.close_price "
            "FROM (SELECT `date`,variety_en,contract,trade_volume,empty_volume,close_price "
            "FROM dce_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "大商所日行情的主力合约持仓数据!", "data": data}


@empty_volume_router.get("/rank-position/dce/{contract}/", summary="大商所合约排名合计持仓量")
async def dce_rank_position(contract: str = Depends(verify_contract), rank: int = Query(20, ge=1, le=20)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,close_price,contract FROM dce_daily WHERE contract=%s;", contract
        )
        price_data = cursor.fetchall()
        cursor.execute(
            "SELECT `date`,contract,"
            "SUM(trade) AS trade_volume,"
            "(SUM(long_position)-SUM(short_position)) AS empty_volume "
            "FROM dce_rank WHERE contract=%s AND rank>=1 AND rank<=%s "
            "GROUP BY `date`;",
            (contract, rank)
        )
        position_data = cursor.fetchall()
    for rank_item in position_data:
        rank_item['close_price'] = ''
        for daily_item in price_data:
            if daily_item['date'] == rank_item['date']:
                rank_item['close_price'] = daily_item['close_price']
                break
    return {"message": "大商所{}合约排名合计持仓量!".format(contract), "data": position_data}


@empty_volume_router.get("/rank-position/dce/{variety_en}/main-contract/", summary="大商所主力合约持仓排名持仓量")
async def dce_rank_position_main_contract(
        variety_en: str = Depends(verify_variety),
        rank: int = Query(20, ge=1, le=20)
):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT ranktb.date,ranktb.variety_en,ranktb.contract,"
            "SUM(ranktb.trade) AS trade_volume,"
            "(SUM(ranktb.long_position) - SUM(ranktb.short_position)) AS empty_volume,"
            "mctb.close_price AS close_price "
            "FROM dce_rank AS ranktb "
            "INNER JOIN "
            "(SELECT t.date,t.contract,t.close_price FROM (SELECT `date`,variety_en,contract,empty_volume,close_price "
            "FROM dce_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 99999999) AS t "
            "GROUP BY t.date) AS mctb "
            "ON ranktb.contract=mctb.contract AND ranktb.date=mctb.date "
            "WHERE ranktb.rank>=1 AND ranktb.rank<=%s "
            "GROUP BY ranktb.date;",
            (variety_en, rank)
        )
        data = cursor.fetchall()
    return {"message": "大商所主力合约排名前{}持仓数据!".format(rank), "data": data}


""" 郑商所 """


@empty_volume_router.get("/daily-position/czce/{contract}/", summary="郑商所合日行情合约持仓量")
async def czce_daily_position(contract: str = Depends(verify_contract)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,contract,trade_volume,empty_volume,close_price "
            "FROM czce_daily "
            "WHERE contract=%s "
            "ORDER BY `date`;",
            (contract,)
        )
        data = cursor.fetchall()
        return {"message": "郑商所日行情的{}持仓数据!".format(contract), "data": data}


@empty_volume_router.get("/daily-position/czce/{variety_en}/main-contract/", summary="郑商所日行情主力合约持仓量")
async def czce_daily_position_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.trade_volume,t.empty_volume,t.close_price "
            "FROM (SELECT `date`,variety_en,contract,trade_volume,empty_volume,close_price "
            "FROM czce_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "大商所日行情的主力合约持仓数据!", "data": data}


@empty_volume_router.get("/rank-position/czce/{contract}/", summary="郑商所合约排名合计持仓量")
async def czce_rank_position(contract: str = Depends(verify_contract), rank: int = Query(20, ge=1, le=20)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,close_price,contract FROM czce_daily WHERE contract=%s;", contract
        )
        price_data = cursor.fetchall()
        cursor.execute(
            "SELECT `date`,contract,"
            "SUM(trade) AS trade_volume,"
            "(SUM(long_position)-SUM(short_position)) AS empty_volume "
            "FROM czce_rank WHERE contract=%s AND rank>=1 AND rank<=%s "
            "GROUP BY `date`;",
            (contract, rank)
        )
        position_data = cursor.fetchall()
    for rank_item in position_data:
        rank_item['close_price'] = ''
        for daily_item in price_data:
            if daily_item['date'] == rank_item['date']:
                rank_item['close_price'] = daily_item['close_price']
                break
    return {"message": "郑商所{}合约排名合计持仓量!".format(contract), "data": position_data}


@empty_volume_router.get("/rank-position/czce/{variety_en}/main-contract/", summary="郑商所主力合约持仓排名持仓量")
async def czce_rank_position_main_contract(
        variety_en: str = Depends(verify_variety),
        rank: int = Query(20, ge=1, le=20)
):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT ranktb.date,ranktb.variety_en,ranktb.contract,"
            "SUM(ranktb.trade) AS trade_volume,"
            "(SUM(ranktb.long_position) - SUM(ranktb.short_position)) AS empty_volume,"
            "mctb.close_price AS close_price "
            "FROM czce_rank AS ranktb "
            "INNER JOIN "
            "(SELECT t.date,t.contract,t.close_price FROM (SELECT `date`,variety_en,contract,empty_volume,close_price "
            "FROM czce_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 99999999) AS t "
            "GROUP BY t.date) AS mctb "
            "ON ranktb.contract=mctb.contract AND ranktb.date=mctb.date "
            "WHERE ranktb.rank>=1 AND ranktb.rank<=%s "
            "GROUP BY ranktb.date;",
            (variety_en, rank)
        )
        data = cursor.fetchall()
    return {"message": "郑商所主力合约排名前{}持仓数据!".format(rank), "data": data}


""" 上期所 """


@empty_volume_router.get("/daily-position/shfe/{contract}/", summary="上期所合日行情合约持仓量")
async def shfe_daily_position(contract: str = Depends(verify_contract)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,contract,trade_volume,empty_volume,close_price "
            "FROM shfe_daily "
            "WHERE contract=%s "
            "ORDER BY `date`;",
            (contract,)
        )
        data = cursor.fetchall()
        return {"message": "上期所日行情的{}持仓数据!".format(contract), "data": data}


@empty_volume_router.get("/daily-position/shfe/{variety_en}/main-contract/", summary="上期所日行情主力合约持仓量")
async def shfe_daily_position_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.trade_volume,t.empty_volume,t.close_price "
            "FROM (SELECT `date`,variety_en,contract,trade_volume,empty_volume,close_price "
            "FROM shfe_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "上期所日行情的主力合约持仓数据!", "data": data}


@empty_volume_router.get("/rank-position/shfe/{contract}/", summary="上期所合约排名合计持仓量")
async def shfe_rank_position(contract: str = Depends(verify_contract), rank: int = Query(20, ge=1, le=20)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,close_price,contract FROM shfe_daily WHERE contract=%s;", contract
        )
        price_data = cursor.fetchall()
        cursor.execute(
            "SELECT `date`,contract,"
            "SUM(trade) AS trade_volume,"
            "(SUM(long_position)-SUM(short_position)) AS empty_volume "
            "FROM shfe_rank WHERE contract=%s AND rank>=1 AND rank<=%s "
            "GROUP BY `date`;",
            (contract, rank)
        )
        position_data = cursor.fetchall()
    for rank_item in position_data:
        rank_item['close_price'] = ''
        for daily_item in price_data:
            if daily_item['date'] == rank_item['date']:
                rank_item['close_price'] = daily_item['close_price']
                break
    return {"message": "上期所{}合约排名合计持仓量!".format(contract), "data": position_data}


@empty_volume_router.get("/rank-position/shfe/{variety_en}/main-contract/", summary="上期所主力合约持仓排名持仓量")
async def shfe_rank_position_main_contract(
        variety_en: str = Depends(verify_variety),
        rank: int = Query(20, ge=1, le=20)
):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT ranktb.date,ranktb.variety_en,ranktb.contract,"
            "SUM(ranktb.trade) AS trade_volume,"
            "(SUM(ranktb.long_position) - SUM(ranktb.short_position)) AS empty_volume,"
            "mctb.close_price AS close_price "
            "FROM shfe_rank AS ranktb "
            "INNER JOIN "
            "(SELECT t.date,t.contract,t.close_price FROM (SELECT `date`,variety_en,contract,empty_volume,close_price "
            "FROM shfe_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 99999999) AS t "
            "GROUP BY t.date) AS mctb "
            "ON ranktb.contract=mctb.contract AND ranktb.date=mctb.date "
            "WHERE ranktb.rank>=1 AND ranktb.rank<=%s "
            "GROUP BY ranktb.date;",
            (variety_en, rank)
        )
        data = cursor.fetchall()
    # mctb: main contract table
    return {"message": "上期所主力合约排名前{}持仓数据!".format(rank), "data": data}


""" 中金所 """


@empty_volume_router.get("/daily-position/cffex/{contract}/", summary="中金所合日行情合约持仓量")
async def cffex_daily_position(contract: str = Depends(verify_contract)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,contract,trade_volume,empty_volume,close_price "
            "FROM cffex_daily "
            "WHERE contract=%s "
            "ORDER BY `date`;",
            (contract,)
        )
        data = cursor.fetchall()
        return {"message": "中金所日行情的{}持仓数据!".format(contract), "data": data}


@empty_volume_router.get("/daily-position/cffex/{variety_en}/main-contract/", summary="中金所日行情主力合约持仓量")
async def cffex_daily_position_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.trade_volume,t.empty_volume,t.close_price "
            "FROM (SELECT `date`,variety_en,contract,trade_volume,empty_volume,close_price "
            "FROM cffex_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "中金所日行情的主力合约持仓数据!", "data": data}


@empty_volume_router.get("/rank-position/cffex/{contract}/", summary="中金所合约排名合计持仓量")
async def cffex_rank_position(contract: str = Depends(verify_contract), rank: int = Query(20, ge=1, le=20)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,close_price,contract FROM cffex_daily WHERE contract=%s;", contract
        )
        price_data = cursor.fetchall()
        cursor.execute(
            "SELECT `date`,contract,"
            "SUM(trade) AS trade_volume,"
            "(SUM(long_position)-SUM(short_position)) AS empty_volume "
            "FROM cffex_rank WHERE contract=%s AND rank>=1 AND rank<=%s "
            "GROUP BY `date`;",
            (contract, rank)
        )
        position_data = cursor.fetchall()
    for rank_item in position_data:
        rank_item['close_price'] = ''
        for daily_item in price_data:
            if daily_item['date'] == rank_item['date']:
                rank_item['close_price'] = daily_item['close_price']
                break
    return {"message": "中金所{}合约排名合计持仓量!".format(contract), "data": position_data}


@empty_volume_router.get("/rank-position/cffex/{variety_en}/main-contract/", summary="中金所主力合约持仓排名持仓量")
async def cffex_rank_position_main_contract(
        variety_en: str = Depends(verify_variety),
        rank: int = Query(20, ge=1, le=20)
):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT ranktb.date,ranktb.variety_en,ranktb.contract,"
            "SUM(ranktb.trade) AS trade_volume,"
            "(SUM(ranktb.long_position) - SUM(ranktb.short_position)) AS empty_volume,"
            "mctb.close_price AS close_price "
            "FROM cffex_rank AS ranktb "
            "INNER JOIN "
            "(SELECT t.date,t.contract,t.close_price FROM (SELECT `date`,variety_en,contract,empty_volume,close_price "
            "FROM cffex_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 99999999) AS t "
            "GROUP BY t.date) AS mctb "
            "ON ranktb.contract=mctb.contract AND ranktb.date=mctb.date "
            "WHERE ranktb.rank>=1 AND ranktb.rank<=%s "
            "GROUP BY ranktb.date;",
            (variety_en, rank)
        )
        data = cursor.fetchall()
    return {"message": "中金所主力合约排名前{}持仓数据!".format(rank), "data": data}
