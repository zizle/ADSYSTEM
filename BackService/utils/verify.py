# _*_ coding:utf-8 _*_
# @File  : verify.py
# @Time  : 2020-07-21 9:55
# @Author: zizle
import os
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from db.redis_z import RedisZ
from configs import APP_DIR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
