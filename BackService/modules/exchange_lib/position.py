# _*_ coding:utf-8 _*_
# @File  : position.py
# @Time  : 2020-08-21 12:55
# @Author: zizle

""" 持仓相关 """
from collections import OrderedDict
from datetime import datetime, timedelta
from fastapi import APIRouter, Query
from pandas import DataFrame, pivot_table, concat
from db.mysql_z import MySqlZ

position_router = APIRouter()


def pivot_data_frame(source_df):
    """ 透视转表数据 """
    source_df["net_position"] = source_df["net_position"].astype(int)
    pivot_df = pivot_table(source_df, index=["variety_en"], columns=["date"])
    return pivot_df


@position_router.get('/position/all-variety/', summary='全品种净持仓数据')
async def all_variety_net_position(interval_days: int = Query(1)):
    # 获取当前日期及45天前
    current_date = datetime.today()
    pre_date = current_date + timedelta(days=-45)
    start_date = pre_date.strftime('%Y%m%d')
    end_date = current_date.strftime('%Y%m%d')
    with MySqlZ() as cursor:
        # 查询大商所的品种净持仓
        cursor.execute(
            "select `date`,variety_en,(sum(long_position) - sum(short_position)) as net_position "
            "from dce_rank "
            "where date<=%s and date>=%s and `rank`>=1 and `rank`<=20 "
            "group by `date`,variety_en;",
            (end_date, start_date)
        )
        dce_net_positions = cursor.fetchall()

        # 查询郑商所的品种净持仓
        cursor.execute(
            "select `date`,variety_en,(sum(long_position) - sum(short_position)) as net_position "
            "from czce_rank "
            "where date<=%s and date>=%s and `rank`>=1 and `rank`<=20 "
            "group by `date`,variety_en;",
            (end_date, start_date)
        )
        czce_net_positions = cursor.fetchall()

        # 查询上期所的品种净持仓
        cursor.execute(
            "select `date`,variety_en,(sum(long_position) - sum(short_position)) as net_position "
            "from shfe_rank "
            "where date<=%s and date>=%s and `rank`>=1 and `rank`<=20 "
            "group by `date`,variety_en;",
            (end_date, start_date)
        )
        shfe_net_positions = cursor.fetchall()

        # 查询中金所的品种净持仓
        cursor.execute(
            "select `date`,variety_en,(sum(long_position) - sum(short_position)) as net_position "
            "from cffex_rank "
            "where date<=%s and date>=%s and `rank`>=1 and `rank`<=20 "
            "group by `date`,variety_en;",
            (end_date, start_date)
        )
        cffex_net_positions = cursor.fetchall()

    # 处理各交易所的数据
    dce_df = DataFrame(dce_net_positions)
    czce_df = DataFrame(czce_net_positions)
    shfe_df = DataFrame(shfe_net_positions)
    cffex_df = DataFrame(cffex_net_positions)

    all_variety_df = concat(
        [pivot_data_frame(dce_df), pivot_data_frame(czce_df), pivot_data_frame(shfe_df), pivot_data_frame(cffex_df)]
    )
    # 倒置列顺序
    all_variety_df = all_variety_df.iloc[:, ::-1]
    # 间隔取数
    split_df = all_variety_df.iloc[:, ::interval_days]
    # 整理表头
    split_df.columns = split_df.columns.droplevel(0)
    split_df = split_df.reset_index()
    split_df = split_df.fillna(0)
    data_dict = split_df.to_dict(orient='records')

    header_keys = split_df.columns.values.tolist()

    final_data = dict()
    for item in data_dict:
        final_data[item['variety_en']] = item

    return {"message": "查询全品种净持仓数据成功!", "data": final_data, 'header_keys': header_keys}

