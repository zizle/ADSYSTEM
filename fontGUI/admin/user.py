# _*_ coding:utf-8 _*_
# @File  : user.py
# @Time  : 2020-07-20 22:18
# @Author: zizle

from .user_ui import UserUI


class UserAdmin(UserUI):
    """ 用户管理业务 """
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.user_role_combobox.currentIndexChanged.connect(self.change_user_role)
        self.search_input.returnPressed.connect(self.search_input_enter)
        # 为用户角色框添加选项
        roles = [
            {"id": 0, "name": "全部"},
            {"id": 1, "name": "超级管理员"},
            {"id": 2, "name": "运营管理员"},
            {"id": 3, "name": "信息管理员"},
            {"id": 4, "name": "品种研究员"},
            {"id": 5, "name": "普通用户"},
        ]
        for role_item in roles:
            self.user_role_combobox.addItem(role_item["name"], role_item["id"])

    def __del__(self):
        print("~用户管理页面析构了")

    def change_user_role(self):
        """ 改变用户角色选项 """
        print(self.user_role_combobox.currentData())
        # 获取当前角色的所有用户

    def search_input_enter(self):
        """ 搜索框enter按键事件 """
        print(self.search_input.text())

