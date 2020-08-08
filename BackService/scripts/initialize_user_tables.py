# _*_ coding:utf-8 _*_
# @File  : initialize_user_tables.py
# @Time  : 2020-08-08 9:57
# @Author: zizle
from db.mysql_z import MySqlZ

with MySqlZ() as cursor:
    # 用户数据库
    cursor.execute("CREATE TABLE IF NOT EXISTS `user_user` ("
                   "`id` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                   "`joined_date` DATETIME NOT NULL DEFAULT NOW(),"
                   "`last_login` DATETIME NOT NULL DEFAULT NOW(),"
                   "`unique_code` VARCHAR(20) NOT NULL,"
                   "`username` VARCHAR(20) NOT NULL,"
                   "`phone` VARCHAR(11) DEFAULT '',"
                   "`email` VARCHAR(50) DEFAULT '',"
                   "`weixin` VARCHAR(50) DEFAULT '',"
                   "`password_hashed` VARCHAR(60) NOT NULL,"
                   "`is_active` BIT NOT NULL DEFAULT 1"
                   ") DEFAULT CHARSET='utf8';")
