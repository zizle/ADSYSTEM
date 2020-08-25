# _*_ coding:utf-8 _*_
# @File  : initialize_spot_tables.py
# @Time  : 2020-08-25 16:01
# @Author: zizle
""" 创建与现货有关的数据库表 """

from db.mysql_z import MySqlZ

with MySqlZ() as cursor:
    # 品种数据库
    cursor.execute("CREATE TABLE IF NOT EXISTS `variety_spot_price` ("
                   "`id` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                   "`create_time` DATETIME NOT NULL DEFAULT NOW(),"
                   "`date` VARCHAR(8) NOT NULL,"
                   "`variety_en` VARCHAR(2) NOT NULL,"
                   "`spot_price` DECIMAL(9,2) DEFAULT 0,"
                   "`price_increase` DECIMAL(9,2) DEFAULT 0"
                   ") DEFAULT CHARSET='utf8';")
