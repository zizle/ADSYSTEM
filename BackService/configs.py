# _*_ coding:utf-8 _*_
# @File  : configs.py
# @Time  : 2020-07-21 8:42
# @Author: zizle


""" 配置文件 """
import os
import time
import logging

APP_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根路径


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
logger.addHandler(logger_handler(app_dir=APP_DIR, log_level=logging.INFO))

# 数据库配置
DB_CONFIGS = {
    "mysql": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "mysql",
        "database": "analysisdecision"
    },
    "redis": {
        "host": "localhost",
        "port": "6379",
        "db": 1
    }
}
