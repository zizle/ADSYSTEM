# _*_ coding:utf-8 _*_
# @File  : variety.py
# @Time  : 2020-08-10 14:14
# @Author: zizle
import re
from collections import OrderedDict
from fastapi import APIRouter, Query, Body, HTTPException
from db.mysql_z import MySqlZ
from db.redis_z import RedisZ
from pymysql.err import IntegrityError, ProgrammingError
from .validate_items import VarietyGroup, ExchangeLib, VarietyItem

variety_router = APIRouter()


@variety_router.get("/variety/all/", summary="获取所有分组及旗下的品种")
async def basic_variety_all():
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `id`,`create_time`,`variety_name`,`variety_en`,`group_name`, `exchange_lib` "
            "FROM `basic_variety` "
            "WHERE `is_active`=1 "
            "ORDER BY `sorted` DESC;",
        )
        all_varieties = cursor.fetchall()
    varieties = OrderedDict()
    for variety_item in all_varieties:
        variety_item['exchange_name'] = ExchangeLib[variety_item['exchange_lib']]
        variety_item['group_name'] = VarietyGroup[variety_item['group_name']]
        if variety_item['group_name'] not in varieties:
            varieties[variety_item['group_name']] = list()
        varieties[variety_item['group_name']].append(variety_item)
    return {"message": "查询品种信息成功!", "varieties": varieties}


@variety_router.get("/variety/", summary="获取分组下的品种")
async def basic_variety(group: VarietyGroup = Query(...)):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `id`,`create_time`,`variety_name`,`variety_en`,`group_name`, `exchange_lib` "
            "FROM `basic_variety` "
            "WHERE `group_name`=%s "
            "ORDER BY `sorted` DESC;",
            (group.name,)
        )
        varieties = cursor.fetchall()
    for variety_item in varieties:
        variety_item['exchange_lib'] = ExchangeLib[variety_item['exchange_lib']]
        variety_item['group_name'] = VarietyGroup[variety_item['group_name']]
    return {"message": "查询品种信息成功!", "varieties": varieties}


@variety_router.post("/variety/", status_code=201, summary="添加品种")
async def add_basic_variety(
        variety: VarietyItem = Body(...)
):
    variety_item = {
        "variety_name": variety.variety_name,
        "variety_en": variety.variety_en,
        "exchange_lib": variety.exchange_lib.name,
        "group_name": variety.group_name.name,
    }
    try:
        with MySqlZ() as cursor:
            cursor.execute(
                "INSERT INTO `basic_variety`"
                "(`variety_name`,`variety_en`,`exchange_lib`,`group_name`) "
                "VALUES (%(variety_name)s,%(variety_en)s,%(exchange_lib)s,%(group_name)s);",
                variety_item
            )
    except IntegrityError:
        raise HTTPException(
            detail="variety_name and variety_en team repeated!",
            status_code=400
        )
    except ProgrammingError:
        raise HTTPException(
            detail="The app inner error.created variety fail!",
            status_code=500
        )
    return {"message": "添加品种成功!", "new_variety": variety}


@variety_router.get("/contracts/", summary="获取某品种下的所有合约")
async def variety_contract(variety_en: str = Query(...), exchange: ExchangeLib = Query(...)):
    if not re.match(r'^[A-Z]{1,2}$', variety_en):
        raise HTTPException(detail="Got an invalid variety_en.", status_code=400)
    # 从redis获取当前品种的所有合约
    with RedisZ() as rs:
        contracts_str = rs.get("{}_contracts".format(variety_en))
        if not contracts_str:
            # 查询当前数据下的所有品种,保存到redis,有效期为12h
            with MySqlZ() as cursor:
                cursor.execute(
                    "SELECT `contract` FROM {}_daily "
                    "WHERE `variety_en`=%s "
                    "GROUP BY `contract`;".format(exchange.name),
                    variety_en
                )
                contract_indb = cursor.fetchall()
            contracts_str = ';'.join([item['contract'] for item in contract_indb])
            rs.set("{}_contracts".format(variety_en), contracts_str, ex=43200)
    contracts = contracts_str.split(";")
    contracts.reverse()
    return {"message": "获取品种合约成功!", "contracts": contracts}

