# _*_ coding:utf-8 _*_
# @File  : initialize_basic_tables.py
# @Time  : 2020-08-10 9:27
# @Author: zizle
from db.mysql_z import MySqlZ

with MySqlZ() as cursor:
    # 品种数据库
    cursor.execute("CREATE TABLE IF NOT EXISTS `basic_variety` ("
                   "`id` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                   "`create_time` DATETIME NOT NULL DEFAULT NOW(),"
                   "`variety_name` VARCHAR(10) NOT NULL,"
                   "`variety_en` VARCHAR(2) NOT NULL,"
                   "`exchange_lib` ENUM('czce','dce','shfe','cffex','ine') NOT NULL,"
                   "`group_name` ENUM('finance','farm','chemical','metal') NOT NULL,"
                   "`sorted` INTEGER NOT NULL DEFAULT 0,"
                   "`is_active` BIT NOT NULL DEFAULT 1,"
                   "UNIQUE KEY `vnve`(`variety_name`,`variety_en`)"
                   ") DEFAULT CHARSET='utf8';")
