# _*_ coding:utf-8 _*_
# @File  : passport.py
# @Time  : 2020-07-19 10:12
# @Author: zizle

""" 用户登录、注册 """
import time
from datetime import datetime
from fastapi import APIRouter, Form, File, UploadFile, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import HTTPException
from fastapi.responses import StreamingResponse

from utils import verify

from db.redis_z import RedisZ
from db.mysql_z import MySqlZ
from .models import JwtToken, User, UserInDB

passport_router = APIRouter()


async def checked_image_code(input_code: str = Form(...), code_uuid: str = Form(...)):
    """ 验证图形验证码的依赖项 """
    print("开始进行图形验证码的验证:", input_code, code_uuid)
    with RedisZ() as r:
        real_image_code = r.get(code_uuid)  # 使用code_uuid取得redis中的验证码
    print(real_image_code, input_code)
    if not real_image_code or input_code.lower() != real_image_code.lower():
        return False
    return True


@passport_router.post("/register/", summary="用户注册")
async def register(
        is_image_code_passed: bool = Depends(checked_image_code),
        phone: str = Form(...),
        nickname: str = Form(""),
        email: str = Form(""),
        weixin: str = Form(""),
        password: str = Form(...),
):
    if not is_image_code_passed:
        raise HTTPException(status_code=400, detail="Got an error image code.")
    print("phone:%s\n nickname:%s\n password:%s" % (phone, nickname, password))
    time.sleep(3)
    # 将用户信息保存到数据库中
    user_to_save = UserInDB(
        unique_code=verify.generate_user_unique_code(),  # 生成系统号
        username=nickname,
        phone=phone,
        email=email,
        weixin=weixin,
        password_hashed=verify.get_password_hash(password)  # hash用户密码
    )
    with MySqlZ() as cursor:
        cursor.execute(
            "INSERT INTO `user_user` (`unique_code`,`username`,`phone`,`email`,`weixin`,`password_hashed`) "
            "VALUES (%(unique_code)s,%(username)s,%(phone)s,%(email)s,%(weixin)s,%(password_hashed)s);",
            (jsonable_encoder(user_to_save))
        )
    back_user = User(
        unique_code=user_to_save.unique_code,
        username=user_to_save.username,
        phone=user_to_save.phone,
        email=user_to_save.email,
        weixin=user_to_save.weixin
    )
    return {"message": "注册成功!", "user": back_user}


async def get_user_in_db(
        phone: str = Form(...),
        password: str = Form(...),
        unique_code: str = Form("")
):
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `id`,`unique_code`,`username`,`phone`,`email`,`weixin`,`password_hashed` "
            "FROM `user_user` WHERE (`phone`=%s OR `unique_code`=%s) AND `is_active`=1;",
            (phone, unique_code)
        )
        user_dict = cursor.fetchone()
        if not user_dict:  # 数据库中没有查询到用户
            return None
        # 如果有用户,修改登录时间
        cursor.execute(
            "UPDATE `user_user` SET `last_login`=%s WHERE `id`=%s;",
            (datetime.today(), user_dict["id"])
        )
    print(user_dict, "数据库查完进行密码验证")
    if not verify.verify_password(password, user_dict["password_hashed"]):  # 将查询到的密码验证
        return None
    return User(**user_dict)


@passport_router.post("/login/", response_model=JwtToken, summary="用户登录")
async def login_for_access_token(
        is_image_code_passed: bool = Depends(checked_image_code),
        user: User = Depends(get_user_in_db)
):
    if not is_image_code_passed:
        raise HTTPException(status_code=400, detail="Got an error image code.")
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    # 得到通过密码验证的用户,签发token证书
    access_token = verify.create_access_token(data={"unique_code": user.unique_code})
    show_username = user.username if user.username else user.phone
    print(show_username)
    return {"show_username": show_username, "access_token": access_token, "token_type": "bearer"}


@passport_router.get("/image_code/", summary="图片验证码")
async def image_code(code_uuid: str):
    response = StreamingResponse(verify.generate_code_image(code_uuid))
    return response


@passport_router.post("/login/file/", summary="测试接口,上传文件")
async def login_file(
        file_key: UploadFile = File(...),
):
    print(file_key.filename)
    return {"message": "用户登录"}


@passport_router.get("/token_login/", summary="使用token进行登录")
async def login_status_keeping(
        is_logged: bool = Depends(verify.is_user_logged_in),
):
    print("用户登录情况:", is_logged)
    return {"message": "用户登录"}
