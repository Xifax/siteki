# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# internal #
import os, pickle

# external #
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QObject, QEvent
from cjktools import scripts

# own #
#from util.tools import unfillLayout
from util.const import UL_WIDTH, UL_HEIGHT, ROOT, RES, USER, ICONS,\
                        PLUS, REMOVE, VERSE_FONT_SIZE, get_pretty_font, ROWS_MAX

#class Filter(QObject):
#    def eventFilter(self, object, event):
#        if event.type() == QEvent.HoverEnter:
#            object.setStyleSheet('QLabel { color: red; }')
#
#        if event.type() == QEvent.HoverLeave:
#            object.setStyleSheet('QLabel { color: black; }')
#
#        if event.type() == QEvent.MouseButtonPress:
#            object.parent().parent().user_list.remove(object.text())
##            object.parent().parent().removeFromGrid(object)
#            object.parent().parent().updateGrid()
#
#        return False

class UserList(QWidget):
    def __init__(self, parent=None):
        super(UserList, self).__init__(parent)
        self.user_list = []
        self.file_path = ROOT + RES + USER
        # grid coordinates
#        self.i = 0; self.j = 0

        self.add = QPushButton()
        self.input = QLineEdit()

        self.list = QListWidget()

        self.itemsGroup = QGroupBox()
        self.itemsLayout = QGridLayout()
        self.itemsGroup.setLayout(self.itemsLayout)

        self.layout = QGridLayout()
        self.layout.addWidget(self.add, 0, 0)
        self.layout.addWidget(self.input, 0, 1)
        self.layout.addWidget(self.list, 1, 0, 1, 2)
#        self.layout.addWidget(self.itemsGroup, 1, 0, 1, 2)

        self.setLayout(self.layout)

#        self.filter = Filter(self)

        self.initComponents()
        self.initComposition()
        self.initActions()

    # --------- initialization --------- #
    def initComposition(self):
        self.setWindowTitle('Excluded items list')
        self.setGeometry((QApplication.desktop().width() - self.width())/2, (QApplication.desktop().height() - self.height())/2, UL_WIDTH, UL_HEIGHT)
        
    def initComponents(self):
        self.add.setIcon(QIcon(ROOT + RES + ICONS + PLUS))
        self.add.setMinimumHeight(40)
        self.input.setFont(QFont(get_pretty_font(), VERSE_FONT_SIZE))

        self.items_font = QFont(get_pretty_font(), VERSE_FONT_SIZE)
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.setToolTip('Double click to delete')
        self.list.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.list.setSortingEnabled(True)
#        self.list.sortItems(Qt.AscendingOrder)

#        self.itemsGroup.setStyleSheet('QGroupBox {background-color : white }')
    
    def initActions(self):
        self.add.clicked.connect(self.addItem)
        self.input.returnPressed.connect(self.addItem)

        self.list.itemDoubleClicked.connect(self.removeFromList)
        self.list.addAction(QAction(QIcon(ROOT + RES + ICONS + REMOVE), '&Remove selected', self, triggered=self.removeItems))

    # ------------ events -------------- #
    def showEvent(self, QShowEvent):
        if os.path.exists(self.file_path):
            dump = open(self.file_path, 'r')
            self.user_list = pickle.load(dump)
            dump.close()
#            for item in self.user_list: self.appendItemToGroup(item)
            for item in self.user_list: self.appendToList(item)


    def closeEvent(self, QCloseEvent):
        dump = open(self.file_path, 'w')
        pickle.dump(self.user_list, dump)
        dump.close()
        self.list.clear()

    # ------------ actions -------------- #
    def addItem(self):
        if unicode(self.input.text()).strip() != '':
            if scripts.Script.Ascii in scripts.script_types(self.input.text()):
                pass
            else:
                if not self.input.text() in self.user_list:
                    self.user_list.append(self.input.text())
                    self.appendToList(self.input.text())
#            self.appendItemToGroup(self.input.text())

    def appendToList(self, item):
        list_item = QListWidgetItem(item)
        list_item.setFont(self.items_font)
        self.list.addItem(list_item)

        self.list.sortItems(Qt.AscendingOrder)

    def removeFromList(self, item):
        self.user_list.remove(item.text())
        self.list.takeItem(self.list.indexFromItem(item).row())

    def removeItems(self):
        for item in self.list.selectedItems():
            self.list.remove(item.text())
            self.list.takeItem(self.list.indexFromItem(item).row())

#    def appendItemToGroup(self, item):
#        if self.j > ROWS_MAX: self.i += 1; self.j = 0
#        element = QLabel(item)
#        element.setAttribute(Qt.WA_Hover, True)
#        element.installEventFilter(self.filter)
#        element.setFont(self.items_font)
##        element.setStyleSheet('QLabel { border: 1px solid black; }')
#        element.setToolTip('Delete ' + item)
#
#        self.itemsLayout.addWidget(element, self.i, self.j); self.j += 1

#    def updateGrid(self):
#        unfillLayout(self.itemsLayout)
#        for item in self.user_list: self.appendItemToGroup(item)
#        self.update()

#    def removeFromGrid(self, item):
#        self.itemsLayout.removeWidget(item)
#        self.update()

