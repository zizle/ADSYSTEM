# _*_ coding:utf-8 _*_
# @File  : basis_price.py
# @Time  : 2020-08-26 17:02
# @Author: zizle
from fastapi import APIRouter, Depends, Query
from utils.contract import verify_contract
from utils.characters import split_number_en

basis_router = APIRouter()


@basis_router.get("/contract-basis/dce/{contract}/", summary="大商所合约的基差")
async def contract_basis(
        contract: str = Depends(verify_contract),
        query_month: int = Query(3)
):
    variety_en, _ = split_number_en(contract)
    print(variety_en)
    return {"message": "{}基差分析数据查询成功!".format(contract), "data": []}

