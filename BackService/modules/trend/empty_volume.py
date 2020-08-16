# _*_ coding:utf-8 _*_
# @File  : empty_volume.py
# @Time  : 2020-08-16 21:51
# @Author: zizle

""" 持仓量分析 """

from fastapi import APIRouter, Depends, Query
from utils.contract import verify_contract, verify_variety
from db.mysql_z import MySqlZ

empty_volume_router = APIRouter()


@empty_volume_router.get("/daily-position/dce/{contract}/", summary="郑商所合日行情合约持仓量")
async def dce_daily_position(contract: str = Depends(verify_contract)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,contract,trade_volume,empty_volume "
            "FROM dce_daily "
            "WHERE contract=%s "
            "ORDER BY `date`;",
            (contract,)
        )
        data = cursor.fetchall()
        return {"message": "查询郑商所日行情的{}持仓数据成功!".format(contract), "data": data}


@empty_volume_router.get("/daily-position/dce/{variety_en}/main-contract/")
async def dce_daily_position_main_contract(variety_en: str = Depends(verify_variety)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT t.date,t.variety_en,t.contract,t.trade_volume,t.empty_volume "
            "FROM (SELECT `date`,variety_en,contract,trade_volume,empty_volume "
            "FROM dce_daily WHERE variety_en=%s "
            "ORDER BY empty_volume DESC limit 999999999) AS t "
            "GROUP BY t.date;",
            (variety_en,)
        )
        data = cursor.fetchall()
    return {"message": "郑商所日行情的主力合约持仓数据!", "data": data}


@empty_volume_router.get("/rank-position/dce/{contract}/", summary="郑商所合约排名合计持仓量")
async def dce_rank_position(contract: str = Depends(verify_contract), rank: int = Query(20, ge=1, le=20)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `date`,variety_en,contract,"
            "sum(trade) AS total_trade, "
            "sum(long_position) AS total_long_position, "
            "sum(short_position) AS total_short_position,"
            "(sum(long_position) - sum(short_position)) AS net_position "
            "FROM dce_rank "
            "WHERE contract='%s' AND `rank`>=1 AND `rank`<=%d "
            "GROUP BY `date` "
            "ORDER BY `date`;" % (contract, rank),
        )
        data = cursor.fetchall()
        return {"message": "郑商所{}合约排名合计持仓量!".format(contract), "data": data}


@empty_volume_router.get("/rank-position/dce/{variety_en}/main-contract/")
async def dce_rank_position_main_contract(
        variety_en: str = Depends(verify_variety),
        rank: int = Query(20, ge=1, le=20)
):
    with MySqlZ() as cursor:
        cursor.execute(
            "select ranktb.date,ranktb.variety_en,ranktb.contract,"
            "sum(ranktb.trade) AS total_trade,"
            "sum(long_position) AS total_long_position,"
            "sum(short_position) AS total_short_position,"
            "(sum(long_position) - sum(short_position)) AS net_position "
            "from dce_rank as ranktb "
            "inner join "
            "(select date,variety_en,contract,empty_volume "
            "from dce_daily where variety_en=%s order by empty_volume desc limit 99999999) as t "
            "on ranktb.contract=t.contract AND ranktb.date=t.date AND ranktb.rank>=1 AND ranktb.rank<=%s "
            "group by ranktb.date;",
            (variety_en, rank)
        )
        data = cursor.fetchall()
    return {"message": "郑商所主力合约排名前{}持仓数据!".format(rank), "data": data}
