# _*_ coding:utf-8 _*_
# @File  : update.py
# @Time  : 2020-08-03 9:54
# @Author: zizle

""" 检查更新弹窗 """

import os
import sys
import json
from subprocess import Popen
from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide2.QtNetwork import QNetworkRequest
from PySide2.QtCore import Qt, QUrl
from configs import SERVER, BASE_DIR, SYS_BIT


class DownloadError(Exception):
    """ 下载错误 """


class UpdateDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(UpdateDialog, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("版本检查")
        self.setFixedSize(240, 120)
        layout = QVBoxLayout()
        self.current_version_message = QLabel("当前版本:", self)
        self.current_version_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_version_message)

        self.last_version_message = QLabel("最新版本:检查中...", self)
        self.last_version_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.last_version_message)

        #  启动更新的信息提示
        self.run_message = QLabel("", self)
        self.run_message.setWordWrap(True)
        self.run_message.hide()
        self.run_message.setAlignment(Qt.AlignCenter)
        self.run_message.setStyleSheet("color:rgb(200,50,50)")
        layout.addWidget(self.run_message)

        opts_layout = QHBoxLayout()
        self.update_button = QPushButton("立即更新")
        self.update_button.clicked.connect(self.exit_for_updating)
        self.close_button = QPushButton("下次更新")
        self.close_button.clicked.connect(self.close)
        opts_layout.addWidget(self.update_button)
        opts_layout.addWidget(self.close_button)
        layout.addLayout(opts_layout)
        self.update_button.hide()
        self.setLayout(layout)

        # 检测最新版本
        app = QApplication.instance()
        self.network_manager = getattr(app, "_network")

        self._get_last_version()

    def _get_last_version(self):
        """ 获取最新版本号 """
        # 获取当前版本号
        json_file = os.path.join(BASE_DIR, "classini/update_{}.json".format(SYS_BIT))
        if not os.path.exists(json_file):
            self.current_version_message.setText("当前版本:检测失败.")
            self.last_version_message.setText("最新版本:检测失败.")
            self.close_button.setText("关闭")
            return

        with open(json_file, "r", encoding="utf-8") as jf:
            update_json = json.load(jf)

        self.current_version_message.setText("当前版本:{}".format(update_json["VERSION"]))

        url = SERVER + "check_version/?version={}&sys_bit={}".format(update_json["VERSION"], SYS_BIT)
        request = QNetworkRequest(url=QUrl(url))

        reply = self.network_manager.get(request)
        reply.finished.connect(self.last_version_back)

    def last_version_back(self):
        """ 检测版本结果 """
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            self.last_version_message.setText("最新版本:检测失败.")
            return
        data = reply.readAll().data()
        u_data = json.loads(data.decode("utf-8"))
        if u_data["update_needed"]:
            for_update_file = os.path.join(BASE_DIR, "classini/for_update_{}.json".format(SYS_BIT))
            # 写入待更新信息
            f_data = {
                "VERSION": u_data["last_version"],
                "SERVER": u_data["file_server"],
                "FILES": u_data["update_files"]
            }
            with open(for_update_file, "w", encoding="utf-8") as f:
                json.dump(f_data, f, indent=4, ensure_ascii=False)
            self.update_button.show()
        else:
            self.update_button.hide()
            self.close_button.setText("关闭")
        self.last_version_message.setText("最新版本:{}".format(u_data["last_version"]))
        reply.deleteLater()

    def exit_for_updating(self):
        """ 退出当前程序，启动更新更新 """
        script_file = os.path.join(BASE_DIR, "AutoUpdate.exe")
        if SYS_BIT == "admin":
            script_file = os.path.join(BASE_DIR, "AutoAdminUpdate.exe")
        is_close = True
        if os.path.exists(script_file):
            try:
                Popen(script_file, shell=False)
            except OSError as e:
                self.run_message.setText(str(e))
                is_close = False
        else:
            self.run_message.setText("更新程序丢失...")
            is_close = False
        self.run_message.show()
        if is_close:
            sys.exit()

    def closeEvent(self, event):
        """ 下次更新 """
        for_update_file = os.path.join(BASE_DIR, "classini/for_update_{}.json".format(SYS_BIT))
        if os.path.exists(for_update_file):
            os.remove(for_update_file)
        super(UpdateDialog, self).closeEvent(event)


