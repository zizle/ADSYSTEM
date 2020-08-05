# _*_ coding:utf-8 _*_
# @File  : configs.py
# @Time  : 2020-07-21 9:43
# @Author: zizle
import os
import sys
import time
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SYS_BIT = "32" if sys.maxsize < 2 ** 32 else "64"
SYS_BIT = "admin"  # 系统版本,后台管理端默认64使用`admin`代替

SERVER = "http://210.13.218.130:9001/"
# SERVER = "http://127.0.0.1:8000/"

LOCAL_SPIDER_SRC = os.path.join(BASE_DIR, "sources/")  # 爬取保存文件的本地文件夹

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
]

MAIN_MENUS = [
    {"id": "1", "name": "首页", "logo": "", "children": None},
    {"id": "2", "name": "数据查询", "logo": "", "children": [
        {"id": "2_1", "name": "交易所数据", "logo": "icons/exchange.png", "children": None}
    ]},
    {"id": "-8", "name": "系统设置", "logo": "", "children": [
        {"id": "-8_1", "name": "版本检查", "logo": "icons/update.png", "children": None}
    ]},
    {"id": "-9", "name": "后台管理", "logo": "", "children": [
        {"id": "-9_1", "name": "用户管理", "logo": "icons/user_manager.png", "children": None},
        {"id": "-9_2", "name": "交易所数据抓取", "logo": "icons/spider.png", "children": None},
    ]}
]


# 日志记录
def logger_handler(app_dir, log_level):
    # 日志配置
    log_folder = os.path.join(app_dir, "logs/")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_name = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_path = log_folder + os.sep + log_file_name

    handler = logging.FileHandler(log_file_path, encoding='UTF-8')
    handler.setLevel(log_level)
    logger_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s - %(pathname)s[line:%(lineno)d]"
    )
    handler.setFormatter(logger_format)
    return handler


logger = logging.getLogger()
logger.addHandler(logger_handler(app_dir=BASE_DIR, log_level=logging.INFO))
