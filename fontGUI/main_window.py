# _*_ coding:utf-8 _*_
# @File  : main_window.py
# @Time  : 2020-07-19 15:09
# @Author: zizle

from PySide2.QtWidgets import QApplication, QLabel, QMessageBox, QMenu, QAction
from PySide2.QtGui import QIcon
from PySide2.QtCore import QTimer
from PySide2.QtNetwork import QNetworkAccessManager
from main_window_ui import MainWindowUI
from frames.homepage import Homepage
from frames.passport import PassportPage
from frames.exchange_query import ExchangeQuery
from frames.contract_kei import ContractKei
from admin.exchange_spider import ExchangeSpider
from admin.user import UserAdmin
from popup.update import UpdateDialog
from utils.characters import half_width_to_full_width
from configs import MAIN_MENUS


class MainWindow(MainWindowUI):
    """ 业务 """

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.current_central_widget_name = ""
        self.scroll_timer = QTimer(self)
        self.current_scroll_index = 0  # 当前取的文字索引
        self.scroll_timer.timeout.connect(self.set_username_show_scroll)
        self.set_homepage()
        self.set_menus(MAIN_MENUS, None)
        self.use_bar.login_button.clicked.connect(self.user_login)

        self._init_network_manager()

    def _init_network_manager(self):
        """ 初始化异步网库管理器 """
        app = QApplication.instance()
        if not hasattr(app, "_network"):
            network_manager = QNetworkAccessManager(self)
            setattr(app, "_network", network_manager)

    def set_username_show_scroll(self):
        """ 设置用户名滚动显示 """
        username = half_width_to_full_width(self.use_bar.login_button.username + " ")
        if self.current_scroll_index >= len(username):
            self.use_bar.login_button.setText(username[:4])
            self.current_scroll_index = 0
        else:
            text = username[self.current_scroll_index:self.current_scroll_index + 4]
            if len(text) < 4:
                text += username[:4 - len(text)]
            self.use_bar.login_button.setText(text)
        self.current_scroll_index += 1

    def set_homepage(self):
        """ 设置首页窗口 """
        self.current_central_widget_name = "首页"
        self.setCentralWidget(Homepage())

    def set_menus(self, menu_data, parent_menu=None):
        for menu_item in menu_data:
            if menu_item["children"]:
                if parent_menu:
                    menu = parent_menu.addMenu(menu_item["name"])
                    menu.setIcon(QIcon(menu_item["logo"]))
                else:
                    menu = self.menu_bar.addMenu(menu_item["name"])
                    menu.setIcon(QIcon(menu_item["logo"]))
                self.set_menus(menu_item["children"], menu)
            else:
                if parent_menu:
                    action = parent_menu.addAction(menu_item["name"])
                    action.setIcon(QIcon(menu_item["logo"]))
                else:
                    action = self.menu_bar.addAction(menu_item["name"])
                    action.setIcon(QIcon(menu_item["logo"]))
                setattr(action, "id", menu_item['id'])
                action.triggered.connect(self.select_menu_action)

    def user_login(self):
        """ 跳转登录注册页面"""
        login_button = self.sender()
        if login_button.username:
            return

        def user_logged(username):
            """用户已登录"""
            if login_button.username:  # 已经登录!
                return
            setattr(login_button, 'username', username)
            if len(username) >= 4:
                self.scroll_timer.start(1000)
            # 设置菜单
            sub_menu = QMenu(login_button)
            logout_action = sub_menu.addAction("退出")
            logout_action.triggered.connect(self.user_logout)
            login_button.setMenu(sub_menu)

            self.set_homepage()  # 跳转到首页

        # 显示登录/注册页
        passport_page = PassportPage()
        passport_page.logged_signal.connect(user_logged)
        self.setCentralWidget(passport_page)
        self.current_central_widget_name = "登录注册"

    def user_logout(self):
        """ 用户退出 """
        if QMessageBox.Yes == QMessageBox.information(self, "退出", "确定退出登录吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
            self.use_bar.login_button.menu().deleteLater()
            self.scroll_timer.stop()
            self.use_bar.login_button.setText("点击登录")
            setattr(self.use_bar.login_button, 'username', '')

            self.set_homepage()  # 退出回到首页

    def select_menu_action(self):
        """ 选择菜单栏中的菜单 """
        action = self.sender()
        if self.current_central_widget_name == action.text():
            return
        action_id = getattr(action, "id")
        if action_id == "1":
            self.set_homepage()
            return
        elif action_id == "2_1":   # 数据查询-交易所数据
            central_widget = ExchangeQuery()
        elif action_id == "2_2":   # 合约K线
            central_widget = ContractKei()
        elif action_id == "-8_1":  # 检查更新
            p = UpdateDialog(self)
            p.exec_()
            return
        elif action_id == "-9_1":
            central_widget = UserAdmin()

        elif action_id == "-9_2":  # 数据抓取
            central_widget = ExchangeSpider()
        else:
            print(action.text(), action.__getattribute__("id"))
            central_widget = QLabel(action_id)
        self.setCentralWidget(central_widget)
        self.current_central_widget_name = action.text()
