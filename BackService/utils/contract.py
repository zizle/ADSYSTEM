# _*_ coding:utf-8 _*_
# @File  : contract.py
# @Time  : 2020-08-16 21:56
# @Author: zizle
import re
from fastapi import HTTPException


def verify_variety(variety_en: str):
    """ 交易代码的验证 """
    if not re.match(r'^[A-Z]{1,2}$', variety_en):
        raise HTTPException(detail="Invalidate Variety!", status_code=400)
    return variety_en


def verify_contract(contract: str):
    """ 交易合约的验证 """
    if not re.match(r"^[A-Z]{1,2}[0-9]{4}$", contract):
        raise HTTPException(detail="Invalidate Contract!", status_code=400)
    return contract
