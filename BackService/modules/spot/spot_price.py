# _*_ coding:utf-8 _*_
# @File  : basis_price.py
# @Time  : 2020-08-25 16:08
# @Author: zizle
from typing import List
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, Query, Depends
from fastapi.encoders import jsonable_encoder
from db.mysql_z import MySqlZ
from .validate_items import SpotPriceItem

price_router = APIRouter()


async def verify_date(date: str = Query(...)):
    try:
        date = datetime.strptime(date, "%Y%m%d")
    except Exception:
        # 直接抛出异常即可
        raise HTTPException(status_code=400, detail="the query param `date` got an error format! must be `%Y-%m-%d`.")
    return date.strftime("%Y%m%d")


@price_router.post("/spot/price/", summary="上传现货价格数据")
async def spot_price(sources: List[SpotPriceItem] = Body(...), current_date: str = Depends(verify_date)):
    data_json = jsonable_encoder(sources)
    save_sql = "INSERT INTO `variety_spot_price` " \
               "(`date`,`variety_en`,`spot_price`,`price_increase`) " \
               "VALUES (%(date)s,%(variety_en)s,%(spot_price)s,%(price_increase)s);"
    with MySqlZ() as cursor:
        # 查询数据时间
        cursor.execute("SELECT `id`, `date` FROM `variety_spot_price` WHERE `date`=%s;" % current_date)
        fetch_one = cursor.fetchone()
        message = "{}现货价格数据已经存在,请不要重复保存!".format(current_date)
        if not fetch_one:
            count = cursor.executemany(save_sql, data_json)
            message = "保存{}现货价格数据成功!\n新增数量:{}".format(current_date, count)
    return {"message": message}
