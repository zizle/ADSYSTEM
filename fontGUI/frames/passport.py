# _*_ coding:utf-8 _*_
# @File  : passport.py
# @Time  : 2020-07-20 10:49
# @Author: zizle
import os
import uuid
import json
from hashlib import md5
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtCore import Signal, QUrl, QTimer, QSettings
from PySide2.QtGui import QPixmap
from PySide2.QtNetwork import QNetworkRequest, QNetworkReply
from frames.passport_ui import PassportPageUI
from utils.multipart import generate_multipart_data
from configs import SERVER, BASE_DIR


class PassportPage(PassportPageUI):
    """ 登录注册业务 """
    logged_signal = Signal(str)
    _code_uuid = ""

    def __init__(self, *args, **kwargs):
        super(PassportPage, self).__init__(*args, **kwargs)

        self.login_button.clicked.connect(self.user_commit_login)
        self.register_button.clicked.connect(self.user_commit_register)
        self.login_code_image.clicked.connect(self.get_image_code)
        self.register_code_image.clicked.connect(self.get_image_code)

        self.text_suffix_point_count = 3  # 文字后点的个数
        self.text_animation_timer = QTimer(self)
        self.text_animation_timer.timeout.connect(self.animation_button_text)
        self.get_image_code()

    def __del__(self):
        print("~登录注册窗口析构了")

    def get_image_code(self):
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        self._code_uuid = ''.join(str(uuid.uuid4()).split("-"))
        # 保存code_uuid方便登录使用
        url = SERVER + 'image_code/?code_uuid=' + self._code_uuid
        request = QNetworkRequest(url=QUrl(url))
        reply = network_manager.get(request)

        reply.finished.connect(self.image_code_back)

    def image_code_back(self):
        """ 获取到image_code """
        reply = self.sender()
        data = reply.readAll().data()
        reply.deleteLater()
        del reply
        pix_map = QPixmap()
        pix_map.loadFromData(data)
        self.login_code_image.setPixmap(pix_map)  # 登录验证码
        self.register_code_image.setPixmap(pix_map)  # 注册验证码

    def animation_button_text(self):
        """动态显示登录状态文字"""
        if self.tab.currentIndex() == 0:  # 登录页
            if self.login_button.text() == "登录":
                self.login_button.setText("登录中")
            if len(self.login_button.text()[2:]) <= self.text_suffix_point_count:
                self.login_button.setText(self.login_button.text() + "·")
            else:
                self.login_button.setText("登录中")
        else:  # 注册页
            if self.register_button.text() == "注册":
                self.register_button.setText("注册中")
            if len(self.register_button.text()[2:]) <= self.text_suffix_point_count:
                self.register_button.setText(self.register_button.text() + "·")
            else:
                self.register_button.setText("注册中")

    def user_commit_login(self):
        """ 用户提交登录 """
        self.login_button.clicked.disconnect()  # 关闭登录点击链接
        # 改变登录按钮文字显示状态
        self.text_animation_timer.start(800)

        md5_hash = md5()
        md5_hash.update(self.login_password.text().encode("utf-8"))

        app = QApplication.instance()
        network_manager = getattr(app, "_network")

        text_dict = {
            "phone": self.login_phone.text(),
            "password": md5_hash.hexdigest(),
            "input_code": self.login_code.text(),
            "code_uuid": self._code_uuid
        }
        multi_data = generate_multipart_data(text_dict)

        url = SERVER + "login/"
        request = QNetworkRequest(url=QUrl(url))
        # request.setHeader(QNetworkRequest.ContentTypeHeader, "multipart/form-data; boundary=%s" % multi_data.boundary())  # 设置后服务器无法找到边界报400
        reply = network_manager.post(request, multi_data)
        reply.finished.connect(self.user_login_back)
        multi_data.setParent(reply)

    def user_login_back(self):
        """ 登录请求返回 """
        self.text_animation_timer.stop()
        self.login_button.clicked.connect(self.user_commit_login)  # 恢复点击信号
        self.login_button.setText("登录")
        reply = self.sender()
        data = reply.readAll().data()
        if reply.error():
            message = "用户名或密码错误!"
            if reply.error() == QNetworkReply.ProtocolInvalidOperationError:
                message = "验证码错误!"
            QMessageBox.information(self, "错误", message)
            return
        data = json.loads(data.decode("utf-8"))
        # 将access_token保存在客户端
        settings_file_path = os.path.join(BASE_DIR, "classini/app.ini")
        app_settings = QSettings(settings_file_path, QSettings.IniFormat)
        app_settings.setValue("TOKEN/token", data["access_token"])
        self.logged_signal.emit(data["show_username"])  # 登录成功

    def user_commit_register(self):
        """ 用户提交注册 """
        if self.register_password_1.text() != self.register_password_2.text():
            QMessageBox.information(self, "错误", "两次输入密码不一致!")
            return
        self.register_button.clicked.disconnect()  # 关闭注册点击链接
        self.text_animation_timer.start(500)  # 按钮文字显示状态
        md5_hash = md5()
        md5_hash.update(self.register_password_1.text().encode("utf-8"))
        register_dict = {
            "phone": self.register_phone.text(),
            "nickname": self.register_nickname.text(),
            "password": md5_hash.hexdigest(),
            "input_code": self.register_code.text(),
            "code_uuid": self._code_uuid
        }

        print(register_dict)
        multi_data = generate_multipart_data(register_dict)
        app = QApplication.instance()
        network_manager = getattr(app, "_network")

        url = SERVER + "register/"
        request = QNetworkRequest(url=QUrl(url))
        # request.setHeader(QNetworkRequest.ContentTypeHeader, "multipart/form-data; boundary=%s" % multi_data.boundary())  # 设置后服务器无法找到边界报400
        reply = network_manager.post(request, multi_data)
        reply.finished.connect(self.user_register_back)
        multi_data.setParent(reply)

    def user_register_back(self):
        """ 用户注册请求返回 """
        self.text_animation_timer.stop()
        self.register_button.clicked.connect(self.user_commit_register)  # 恢复点击信号
        self.register_button.setText("注册")
        reply = self.sender()
        data = reply.readAll().data()
        data = json.loads(data.decode("utf-8"))
        QMessageBox.information(self, "提示", "注册成功,马上去登录!")
        self.tab.setCurrentIndex(0)
