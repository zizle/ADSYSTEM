# _*_ coding:utf-8 _*_
# @File  : mysql_z.py
# @Time  : 2020-07-21 8:28
# @Author: zizle

""" 连接MySQL """
import sys
from pymysql import FIELD_TYPE, converters
from pymysql.connections import Connection
from pymysql.cursors import DictCursor
from configs import DB_CONFIGS

params = DB_CONFIGS["mysql"]

conversions = converters.conversions
conversions[FIELD_TYPE.BIT] = lambda x: 1 if int.from_bytes(x, byteorder=sys.byteorder, signed=False) else 0

params["conv"] = conversions  # 数据库中的BIT返回0或1 (INT)


class ConnectError(Exception):
    """ 自定义错误 """


class MySqlZ(Connection):
    def __init__(self):
        super(MySqlZ, self).__init__(**params)
        self.execute_cursor = self.cursor(DictCursor)

    def __enter__(self):
        """Context manager that returns a Cursor"""
        if self.open:
            self.begin()
            return self.execute_cursor
        else:
            raise ConnectionError("连接Mysql失败!")

    def __exit__(self, exc, value, traceback):
        """On successful exit, commit. On exception, rollback"""
        if exc:
            self.rollback()
        else:
            self.commit()
        self.execute_cursor.close()
        self.close()
