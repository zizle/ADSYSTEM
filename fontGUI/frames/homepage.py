# _*_ coding:utf-8 _*_
# @File  : homepage.py
# @Time  : 2020-07-19 15:14
# @Author: zizle
import os
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtCore import QSettings, QUrl
from PySide2.QtNetwork import QNetworkRequest, QNetworkReply
from .homepage_ui import HomepageUI
from configs import BASE_DIR, SERVER


class Homepage(HomepageUI):
    """ 首页业务 """
    def __init__(self, *args, **kwargs):
        super(Homepage, self).__init__(*args, **kwargs)
        # self.is_logged_button.clicked.connect(self.ask_login_status)

    def __del__(self):
        print("~首页窗口析构了")

    def ask_login_status(self):
        app_setting_file = os.path.join(BASE_DIR, "classini/app.ini")
        app_settings = QSettings(app_setting_file, QSettings.IniFormat)
        token = "Bearer " + app_settings.value("TOKEN/token")
        print(token)
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + "/token_login/"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader("Authorization".encode("utf-8"), token.encode("utf-8"))
        reply = network_manager.get(request)
        reply.finished.connect(self.is_logged_reply)

    def is_logged_reply(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.AuthenticationRequiredError:
            reply.deleteLater()
            QMessageBox.information(self, "错误", "登录已过期,需登录才能使用!", QMessageBox.Yes)
            self.parent().user_logout(token_expire=True)  # 退出登录,主页用户栏显示点击可登录状态
            return
        QMessageBox.information(self, "成功", "登录信息在有效期内!", QMessageBox.Yes)
        reply.deleteLater()
