# _*_ coding:utf-8 _*_
# @File  : verify.py
# @Time  : 2020-07-21 9:55
# @Author: zizle
import os
import random
import time
from typing import Optional
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from db.redis_z import RedisZ
from db.mysql_z import MySqlZ
from configs import APP_DIR
from uuid import uuid4
from passlib.context import CryptContext
from configs import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_code_image(redis_key):
    """ 生成四位数验证码,存入Redis """
    def get_random_color():  # 获取随机颜色的函数
        return random.randint(0, 240), random.randint(0, 240), random.randint(0, 240)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (90, 30),
        (240, 240, 240)
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    ttf_path = os.path.join(APP_DIR, "ttf/KumoFont.ttf")
    font_obj = ImageFont.truetype(ttf_path, 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(4):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型
        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((10 + 20 * i, 0), tmp, fill=get_random_color(), font=font_obj)  # 20（首字符左间距） + 20*i 字符的间距
    # 加干扰线
    width = 90  # 图片宽度（防止越界）
    height = 30
    for i in range(4):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    # 加干扰点
    for i in range(25):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 获得一个缓存区
    buf = BytesIO()
    # 将图片保存到缓存区
    img_obj.save(buf, 'png')
    buf.seek(0)
    # 将验证码保存到redis
    text = ''.join(tmp_list)
    with RedisZ() as r:
        r.set(name=redis_key, value=text, ex=120)
    return buf


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_user_unique_code():
    uuid = ''.join(str(uuid4()).split("-"))
    return "user_" + ''.join([random.choice(uuid) for _ in range(15)])


def create_access_token(data: dict, expire_seconds: Optional[int] = 1800):
    """ 创建JWT """
    to_encode = data.copy()
    expire = time.time() + expire_seconds
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encode_jwt


def is_active_user(unique_code: str):
    """ 使用unique_code 从数据库中获取用户 """
    with MySqlZ() as cursor:
        cursor.execute(
            "SELECT `id`,`unique_code` FROM `user_user` WHERE `unique_code`=%s AND `is_active`=1;",
            (unique_code, )
        )
        user_dict = cursor.fetchone()
    if user_dict:
        return True
    else:
        return False


async def is_user_logged_in(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        unique_code: str = payload.get("unique_code")  # `unique_code`与生成时的对应
        if unique_code is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # 从数据库中获取用户
    if is_active_user(unique_code):
        return True
    else:
        return False
