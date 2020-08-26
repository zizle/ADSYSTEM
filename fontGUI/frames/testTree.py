# _*_ coding:utf-8 _*_
# @File  : testTree.py
# @Time  : 2020-08-26 8:26
# @Author: zizle

from PySide2.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QLabel, QAbstractItemView
from PySide2.QtGui import QIcon, QBrush, QColor, QFont
from PySide2.QtCore import Qt
class TreeWidget(QTreeWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.setColumnCount(3)
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)
        self.setIndentation(0)
        self.setHeaderHidden(True)
        self.foreground_font = QFont()
        self.foreground_font.setBold(True)
        self.normal_font = QFont()
        self.normal_font.setBold(False)
        self.setExpandsOnDoubleClick(False)
        p = QTreeWidgetItem(self)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        p.setFont(0, font)
        p.setText(0, "父级1父级1父级1父级1父级1父级1")
        p.setIcon(0, QIcon("icons/arrow_right.png"))
        p.setFirstColumnSpanned(True)

        c = QTreeWidgetItem(p)

        c.setText(0,"子级1")
        c.setText(1,"子级2")
        c.setText(2,"子级3")
        c.setTextAlignment(0, Qt.AlignCenter)
        c.setTextAlignment(1, Qt.AlignCenter)
        c.setTextAlignment(2, Qt.AlignCenter)
        c.setData(0, Qt.UserRole, "c_00")
        c.setData(1, Qt.UserRole, "c_01")
        c.setData(2, Qt.UserRole, "c_02")

        c = QTreeWidgetItem(p)

        c.setText(0, "子级1")
        c.setText(1, "子级2")
        c.setTextAlignment(0, Qt.AlignCenter)
        c.setTextAlignment(1, Qt.AlignCenter)
        c.setData(0, Qt.UserRole, "c_03")
        c.setData(1, Qt.UserRole, "c_04")

        p.addChild(c)

        p = QTreeWidgetItem(self)
        p.setText(0, "父级2父级2父级2父级2父级2父级2")
        p.setIcon(0, QIcon("icons/arrow_right.png"))
        p.setFirstColumnSpanned(True)

        p.setFont(0, font)
        c = QTreeWidgetItem(p)

        c.setText(0, "子级2")
        c.setText(1, "子级22")
        c.setText(2, "子级23")
        c.setTextAlignment(0, Qt.AlignCenter)
        c.setTextAlignment(1, Qt.AlignCenter)
        c.setTextAlignment(2, Qt.AlignCenter)
        c.setData(0, Qt.UserRole, "c_10")
        c.setData(1, Qt.UserRole, "c_11")
        c.setData(2, Qt.UserRole, "c_12")

        p.addChild(c)
        self.itemClicked.connect(self.click)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName("tree")
        self.setStyleSheet(
            "#tree::item:selected{background-color:rgb(255,255,255);color:rgb(180,12,34);}"
            "#tree::item:hover{background-color:rgb(255,255,255);color:rgb(10,160,10)}"
        )
        self.setAnimated(True)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def click(self, item, col):
        if item.childCount():
            if item.isExpanded():
                item.setExpanded(False)
                item.setIcon(0, QIcon("icons/arrow_right.png"))
            else:
                item.setExpanded(True)
                item.setIcon(0, QIcon("icons/arrow_bottom.png"))
        elif item.parent():
            print(item.text(0), col)
            print(item.data(col, Qt.UserRole))


class Tree(QWidget):
    def __init__(self):
        super(Tree, self).__init__()
        l = QHBoxLayout()
        self.tree = TreeWidget()
        self.tree.setMaximumWidth(250)
        l.addWidget(self.tree)
        l.addWidget(QLabel('右侧显示', self))
        self.setLayout(l)

