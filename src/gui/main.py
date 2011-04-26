# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# own #
from parse.verse import parse_verse
from printer.printing import print_document
from utils.const import __version__, _name, WIDTH, HEIGHT,\
                        ROOT, RES, ICONS,\
                        PARSE, PDF, FONT, TOGGLE, EXCLUDE, OPTIONS

# external #
from PyQt4.QtGui import *

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.layout = QGridLayout()

        self.input = QTextEdit()
        self.parse = QPushButton('Par&se')
        self.topdf = QPushButton('P&DF')
        self.toggle = QPushButton('&Toggle')
        self.font = QPushButton('&Font')

        self.exclude = QPushButton('E&xclude')
        self.options = QPushButton('&Options')

        self.layout.addWidget(self.parse, 0, 0)
        self.layout.addWidget(self.topdf, 0, 1)
        self.layout.addWidget(self.font, 0, 2)
        self.layout.addWidget(self.toggle, 0, 3)
        self.layout.addWidget(self.input, 1, 0, 1, 4)
        self.layout.addWidget(self.exclude, 2, 0, 1, 2)
        self.layout.addWidget(self.options, 2, 2, 1, 2)

        self.setLayout(self.layout)

        self.initComposition()
        self.initComponents()
        self.initActions()


    def initComposition(self):
        self.setWindowTitle(_name + ' ' + __version__)
        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2, (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

    def initComponents(self):
        self.toggle.setCheckable(True)
        self.font.setCheckable(True)
        self.exclude.setCheckable(True)
        self.options.setCheckable(True)

        # icons
        self.parse.setIcon(QIcon(ROOT + RES + ICONS + PARSE ))
        self.topdf.setIcon(QIcon(ROOT + RES + ICONS + PDF ))
        self.font.setIcon(QIcon(ROOT + RES + ICONS + FONT ))
        self.toggle.setIcon(QIcon(ROOT + RES + ICONS + TOGGLE ))
        self.exclude.setIcon(QIcon(ROOT + RES + ICONS + EXCLUDE ))
        self.options.setIcon(QIcon(ROOT + RES + ICONS + OPTIONS ))

    def initActions(self):
        self.parse.clicked.connect(self.parseNPrint)
        self.topdf.clicked.connect(self.parseNPDF)

        self.toggle.clicked.connect(self.toggleInput)

    def centerWidget(self):
        desktop = QApplication.desktop()
        self.move((desktop.width() - self.width())/2, (desktop.height() - self.height())/2)

    # ------------- actions --------------#
    def parseNPrint(self):
        if not self.input.toPlainText() == '': print_document(self.input.toHtml(), parse_verse(self.input.toPlainText()))
        else: QMessageBox.information(self, 'Nothing to parse', 'Would you kindly paste some delicious text?')

    def parseNPDF(self):
         if not self.input.toPlainText() == '': print_document(self.input.toHtml(), parse_verse(self.input.toPlainText()), True)
         else: QMessageBox.information(self, 'Ahem', 'Well, pdf convertor needs some text too, duh!')

    def toggleInput(self):
        if self.toggle.isChecked(): self.input.hide()
        else: self.input.show()

        self.adjustSize()
        self.centerWidget()