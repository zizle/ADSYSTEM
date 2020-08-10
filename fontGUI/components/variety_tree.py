# _*_ coding:utf-8 _*_
# @File  : variety_tree.py
# @Time  : 2020-08-10 16:46
# @Author: zizle

""" 品种目录树 """
import json
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication
from PySide2.QtNetwork import QNetworkRequest
from PySide2.QtCore import Qt, Signal, QUrl
from PySide2.QtGui import QIcon
from configs import SERVER


class VarietyTree(QTreeWidget):
    tree_icons = {
        "金融股指": "icons/finance.png", "农副产品": "icons/farm_product.png",
        "能源化工": "icons/chemical.png", "金属产业": "icons/metal.png"
    }

    selected_signal = Signal(str, str)

    def __init__(self, *args, **kwargs):
        super(VarietyTree, self).__init__(*args, **kwargs)
        self.header().hide()
        self.setFocusPolicy(Qt.NoFocus)
        self.setColumnCount(1)
        self.itemClicked.connect(self.item_clicked)
        self.setObjectName("varietyTree")
        self.setStyleSheet("#varietyTree{font-size:14px;border:none;border-right: 1px solid rgba(50,50,50,100)}"
                           "#varietyTree::item:hover{background-color:rgba(0,255,0,50)}"
                           "#varietyTree::item:selected{background-color:rgba(255,0,0,100)}"
                           "#varietyTree::item{height:28px;}"
                           )

        self._get_all_variety()  # 获取所有分组及旗下品种

    def _get_all_variety(self):
        # 获取所有品种并显示
        app = QApplication.instance()
        network_manager = getattr(app, "_network")
        url = SERVER + 'variety/all/'
        reply = network_manager.get(QNetworkRequest(QUrl(url)))
        reply.finished.connect(self.all_variety_reply)

    def all_variety_reply(self):
        reply = self.sender()
        if reply.error():
            reply.deleteLater()
            return
        data = reply.readAll().data()
        data = json.loads(data.decode('utf-8'))
        varieties = data["varieties"]
        for group_name in varieties:
            tree_item = QTreeWidgetItem(self)
            tree_item.setText(0, group_name)
            tree_item.setIcon(0, QIcon(self.tree_icons[group_name]))
            for child_item in varieties[group_name]:
                child = QTreeWidgetItem(tree_item)
                child.setText(0, child_item["variety_name"])
                setattr(child, "variety_en", child_item["variety_en"])
                setattr(child, "exchange_name", child_item["exchange_name"])
                # child.setIcon(0, QIcon(child_item["logo"]))
                tree_item.addChild(child)
        reply.deleteLater()

    def mouseDoubleClickEvent(self, event):
        event.accept()

    def item_clicked(self, tree_item):
        if tree_item.childCount():
            if tree_item.isExpanded():
                tree_item.setExpanded(False)
            else:
                tree_item.setExpanded(True)
        elif tree_item.parent():
            item_en = getattr(tree_item, "variety_en")
            exchange_name = getattr(tree_item, "exchange_name")
            self.selected_signal.emit(item_en, exchange_name)
