# _*_ coding:utf-8 _*_
# @File  : passport.py
# @Time  : 2020-07-19 10:12
# @Author: zizle

""" 用户登录、注册 """
import time
from fastapi import APIRouter, Form, File, UploadFile
from fastapi.exception_handlers import HTTPException
from fastapi.responses import StreamingResponse

from utils.verify import generate_code_image, get_password_hash, verify_password
from db.redis_z import RedisZ

passport_router = APIRouter()


@passport_router.post("/register/", summary="用户注册")
async def register(
        phone: str = Form(...),
        nickname: str = Form(""),
        password: str = Form(...),
        input_code: str = Form(...),
        code_uuid: str = Form(...)
):
    print("phone:%s\n nickname:%s\n password:%s\n input_code:%s\n code_uuid:%s" % (phone, nickname, password, input_code, code_uuid))
    time.sleep(3)
    # 使用手机号为key将用户密码保存在redis中
    with RedisZ() as r:
        r.set(name=phone, value=get_password_hash(password))

    return {"message": "注册成功!"}


@passport_router.post("/login/", summary="用户登录")
async def login(
        phone: str = Form(...),
        password: str = Form(...),
        input_code: str = Form(...),
        code_uuid: str = Form(...)
):
    print(phone)
    print(password)
    print(input_code)
    print(code_uuid)
    time.sleep(3)
    # 使用code_uuid取得redis中的验证码
    with RedisZ() as r:
        real_image_code = r.get(code_uuid)
        hash_password = r.get(phone)  # 注册时hash保存的密码
    if not real_image_code or input_code.lower() != real_image_code.lower():
        raise HTTPException(status_code=400, detail="get a error image code.")
    print("图片验证码成功")
    # 查询用户用对比hash_密码
    # hash_password = get_password_hash(password)  注册时hash保存的密码

    print("hash_password:", hash_password)
    print(verify_password(password, hash_password))
    if not verify_password(password, hash_password):
        raise HTTPException(status_code=401, detail="username or password error.")

    return {"message": "用户登录", "phone": phone}


@passport_router.post("/login/file/", summary="测试接口,上传文件")
async def login_file(
        file_key: UploadFile = File(...),
):
    print(file_key.filename)
    return {"message": "用户登录"}


@passport_router.get("/image_code/", summary="图片验证码")
async def image_code(code_uuid: str):
    response = StreamingResponse(generate_code_image(code_uuid))
    return response
