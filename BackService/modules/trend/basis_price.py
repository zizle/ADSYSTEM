# _*_ coding:utf-8 _*_
# @File  : basis_price.py
# @Time  : 2020-08-26 17:02
# @Author: zizle

""" 基差分析数据接口 """

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from db.mysql_z import MySqlZ
from utils.contract import verify_contract, verify_variety
from utils.characters import split_number_en

basis_router = APIRouter()


@basis_router.get("/contract-basis/dce/{contract}/", summary="大商所合约的基差")
async def dce_contract_basis(
        contract: str = Depends(verify_contract),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    variety_en, _ = split_number_en(contract)
    # 查询数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,dcedtb.variety_en, dcedtb.contract,dcedtb.close_price, dcedtb.settlement "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN dce_daily AS dcedtb "
            "ON vsptb.variety_en=dcedtb.variety_en AND dcedtb.contract=%s AND vsptb.date=dcedtb.date "
            "AND vsptb.date>=%s AND vsptb.date<=%s;",
            (contract, start_date, end_date)
        )

        data = cursor.fetchall()

    return {"message": "大商所{}现货与期货价数据查询成功!".format(contract), "data": data}


@basis_router.get('/contract-basis/dce/{variety_en}/main-contract/', summary="大商所主力合约基差")
async def dce_main_contract_basis(
        variety_en: str = Depends(verify_variety),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,mctb.variety_en,mctb.contract,mctb.close_price "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN "
            "(SELECT middletb.date,middletb.variety_en,middletb.contract,middletb.close_price "
            "FROM (SELECT `date`,variety_en,contract,close_price FROM dce_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 999999999) AS middletb "
            "GROUP BY middletb.date) AS mctb "
            "ON vsptb.date=mctb.date AND vsptb.variety_en=mctb.variety_en AND vsptb.date>=%s AND vsptb.date<=%s;",
            (variety_en, start_date, end_date)
        )
        data = cursor.fetchall()
    return {"message": "大商所{}主力合约现货与期货价数据查询成功!".format(variety_en), "data": data}


@basis_router.get("/contract-basis/czce/{contract}/", summary="郑商所合约的基差")
async def czce_contract_basis(
        contract: str = Depends(verify_contract),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    variety_en, _ = split_number_en(contract)
    # 查询数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,dcedtb.variety_en, dcedtb.contract,dcedtb.close_price, dcedtb.settlement "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN czce_daily AS dcedtb "
            "ON vsptb.variety_en=dcedtb.variety_en AND dcedtb.contract=%s AND vsptb.date=dcedtb.date "
            "AND vsptb.date>=%s AND vsptb.date<=%s;",
            (contract, start_date, end_date)
        )

        data = cursor.fetchall()

    return {"message": "郑商所{}现货与期货价数据查询成功!".format(contract), "data": data}


@basis_router.get('/contract-basis/czce/{variety_en}/main-contract/', summary="郑商所主力合约基差")
async def dce_main_contract_basis(
        variety_en: str = Depends(verify_variety),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,mctb.variety_en,mctb.contract,mctb.close_price "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN "
            "(SELECT middletb.date,middletb.variety_en,middletb.contract,middletb.close_price "
            "FROM (SELECT `date`,variety_en,contract,close_price FROM czce_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 999999999) AS middletb "
            "GROUP BY middletb.date) AS mctb "
            "ON vsptb.date=mctb.date AND vsptb.variety_en=mctb.variety_en AND vsptb.date>=%s AND vsptb.date<=%s;",
            (variety_en, start_date, end_date)
        )
        data = cursor.fetchall()
    return {"message": "郑商所{}主力合约现货与期货价数据查询成功!".format(variety_en), "data": data}


@basis_router.get("/contract-basis/shfe/{contract}/", summary="上期所合约的基差")
async def shfe_contract_basis(
        contract: str = Depends(verify_contract),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    variety_en, _ = split_number_en(contract)
    # 查询数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,dcedtb.variety_en, dcedtb.contract,dcedtb.close_price, dcedtb.settlement "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN shfe_daily AS dcedtb "
            "ON vsptb.variety_en=dcedtb.variety_en AND dcedtb.contract=%s AND vsptb.date=dcedtb.date "
            "AND vsptb.date>=%s AND vsptb.date<=%s;",
            (contract, start_date, end_date)
        )

        data = cursor.fetchall()

    return {"message": "上期所{}现货与期货价数据查询成功!".format(contract), "data": data}


@basis_router.get('/contract-basis/shfe/{variety_en}/main-contract/', summary="上期所主力合约基差")
async def shfe_main_contract_basis(
        variety_en: str = Depends(verify_variety),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,mctb.variety_en,mctb.contract,mctb.close_price "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN "
            "(SELECT middletb.date,middletb.variety_en,middletb.contract,middletb.close_price "
            "FROM (SELECT `date`,variety_en,contract,close_price FROM shfe_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 999999999) AS middletb "
            "GROUP BY middletb.date) AS mctb "
            "ON vsptb.date=mctb.date AND vsptb.variety_en=mctb.variety_en AND vsptb.date>=%s AND vsptb.date<=%s;",
            (variety_en, start_date, end_date)
        )
        data = cursor.fetchall()
    return {"message": "上期所{}主力合约现货与期货价数据查询成功!".format(variety_en), "data": data}


@basis_router.get("/contract-basis/cffex/{contract}/", summary="中金所合约的基差")
async def cffex_contract_basis(
        contract: str = Depends(verify_contract),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    variety_en, _ = split_number_en(contract)
    # 查询数据
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,dcedtb.variety_en, dcedtb.contract,dcedtb.close_price, dcedtb.settlement "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN cffex_daily AS dcedtb "
            "ON vsptb.variety_en=dcedtb.variety_en AND dcedtb.contract=%s AND vsptb.date=dcedtb.date "
            "AND vsptb.date>=%s AND vsptb.date<=%s;",
            (contract, start_date, end_date)
        )

        data = cursor.fetchall()

    return {"message": "中金所{}现货与期货价数据查询成功!".format(contract), "data": data}


@basis_router.get('/contract-basis/cffex/{variety_en}/main-contract/', summary="中金所主力合约基差")
async def cffex_main_contract_basis(
        variety_en: str = Depends(verify_variety),
        query_month: int = Query(3)
):
    today = datetime.today()
    start_date = (today + timedelta(days=-(query_month * 30))).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT vsptb.date,vsptb.spot_price,vsptb.price_increase,mctb.variety_en,mctb.contract,mctb.close_price "
            "FROM variety_spot_price AS vsptb "
            "INNER JOIN "
            "(SELECT middletb.date,middletb.variety_en,middletb.contract,middletb.close_price "
            "FROM (SELECT `date`,variety_en,contract,close_price FROM cffex_daily WHERE variety_en=%s ORDER BY empty_volume DESC limit 999999999) AS middletb "
            "GROUP BY middletb.date) AS mctb "
            "ON vsptb.date=mctb.date AND vsptb.variety_en=mctb.variety_en AND vsptb.date>=%s AND vsptb.date<=%s;",
            (variety_en, start_date, end_date)
        )
        data = cursor.fetchall()
    return {"message": "中金所{}主力合约现货与期货价数据查询成功!".format(variety_en), "data": data}
