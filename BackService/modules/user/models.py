# _*_ coding:utf-8 _*_
# @File  : models.py
# @Time  : 2020-08-07 23:06
# @Author: zizle
from typing import Optional
from pydantic import BaseModel


class JwtToken(BaseModel):
    show_username: str
    access_token: str
    token_type: str


class User(BaseModel):
    id: int = None
    unique_code: Optional[str] = None
    username: str
    phone: Optional[str] = None
    email: Optional[str] = None
    weixin: Optional[str] = None
    is_active: Optional[bool] = True


class UserInDB(User):
    password_hashed: str
