# -*- coding=utf-8 -*-
from PySide.QtCore import Qt

__author__ = 'Yadavito'

# own #
from options.settings import Config
from parse.verse import parse_verse
from printer.printing import print_document
from utils.const import __version__, _name, WIDTH, HEIGHT,\
                        ROOT, RES, ICONS,\
                        PARSE, PDF, FONT, TOGGLE, EXCLUDE, OPTIONS

# external #
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.config = Config()

        self.layout = QGridLayout()

        self.input = QTextEdit()
        self.parse = QPushButton('Par&se')
        self.topdf = QPushButton('P&DF')
        self.toggle = QPushButton('&Toggle')
        self.font = QPushButton('&Font')

        self.exclude = QPushButton('E&xclude')
        self.options = QPushButton('&Options')

        self.fontGroup = QGroupBox('Zoom')
        self.excludeGroup = QGroupBox('Exceptions')
        self.optionsGroup = QGroupBox('Settings')

        # fonts contents

        # exclude contents

        # options contents
        self.onTop = QCheckBox('Always on top')
        self.reSize = QCheckBox('Allow automatic resize')
        self.centerSize = QCheckBox('Center on resize')
        self.savePos = QCheckBox('Save window position on exit')
        self.saveButtons = QCheckBox('Save buttons states states on exit')
        self.toTray = QCheckBox('Send to tray on minimize')

        self.optionsLayout = QVBoxLayout()
        self.optionsLayout.addWidget(self.onTop)
        self.optionsLayout.addWidget(self.reSize)
        self.optionsLayout.addWidget(self.centerSize)
        self.optionsLayout.addWidget(self.savePos)
        self.optionsLayout.addWidget(self.saveButtons)
        self.optionsLayout.addWidget(self.toTray)
        self.optionsGroup.setLayout(self.optionsLayout)

        # buttons
        self.layout.addWidget(self.parse, 0, 0)
        self.layout.addWidget(self.topdf, 0, 1)
        self.layout.addWidget(self.font, 0, 2)
        self.layout.addWidget(self.toggle, 0, 3)
        # font group
        self.layout.addWidget(self.fontGroup, 1, 0, 1, 4)
        # text edit
        self.layout.addWidget(self.input, 2, 0, 1, 4)
        # exclude/options groups
        self.layout.addWidget(self.excludeGroup, 3, 0, 1, 4)
        self.layout.addWidget(self.optionsGroup, 4, 0, 1, 4)
        # buttons again
        self.layout.addWidget(self.exclude, 5, 0, 1, 2)
        self.layout.addWidget(self.options, 5, 2, 1, 2)

        self.setLayout(self.layout)

        self.initComposition()
        self.initComponents()
        self.initActions()

    def initComposition(self):
        self.setWindowTitle(_name + ' ' + __version__)

        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2, (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

        if self.config.save_position(): self.move(self.config.get_position)
        if self.config.on_top(): self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def initComponents(self):
        self.toggle.setCheckable(True)
        self.font.setCheckable(True)
        self.exclude.setCheckable(True)
        self.options.setCheckable(True)

        self.fontGroup.hide()
        self.excludeGroup.hide()
        self.optionsGroup.hide()

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
        self.font.clicked.connect(self.toggleFont)
        self.exclude.clicked.connect(self.toggleExclude)
        self.options.clicked.connect(self.toggleOptions)

        self.onTop.clicked.connect(self.updateOptions)
        self.centerSize.clicked.connect(self.updateOptions)
        self.reSize.clicked.connect(self.updateOptions)
        self.saveButtons.clicked.connect(self.updateOptions)
        self.savePos.clicked.connect(self.updateOptions)
        self.toTray.clicked.connect(self.updateOptions)

    #------------- position -------------#
    def centerWidget(self):
        desktop = QApplication.desktop() 
        self.move((desktop.width() - self.width())/2, (desktop.height() - self.height())/2)

    def updateComposition(self):
        if self.config.resize(): self.adjustSize()
        if self.config.center(): self.centerWidget()

    def updateComponents(self):
        self.toggleInput()
        self.toggleFont()
        self.toggleExclude()
        self.toggleOptions()

    # ------------- actions --------------#
    def parseNPrint(self):
        if not self.input.toPlainText() == '': print_document(self.input.toHtml(), parse_verse(self.input.toPlainText()))
        else: QMessageBox.information(self, 'Nothing to parse', 'Would you kindly paste some delicious text?')

    def parseNPDF(self):
         if not self.input.toPlainText() == '': print_document(self.input.toHtml(), parse_verse(self.input.toPlainText()), True)
         else: QMessageBox.information(self, 'Ahem', 'Well, pdf convertor needs some text too, duh!')

    # ------------- interface ------------#
    def toggleInput(self):
        if self.toggle.isChecked(): self.input.hide()
        else: self.input.show()
        self.updateComposition()

    def toggleFont(self):
        if self.font.isChecked(): self.fontGroup.show()
        else: self.fontGroup.hide()
        self.updateComposition()

    def toggleExclude(self):
        if self.exclude.isChecked(): self.excludeGroup.show()
        else: self.excludeGroup.hide()
        self.updateComposition()

    def toggleOptions(self):
        if self.options.isChecked(): self.optionsGroup.show()
        else: self.optionsGroup.hide()
        self.updateComposition()

    def updateButtonStates(self):
        if self.config.save_buttons():
            self.toggle.setChecked(self.config.toggle())
            self.font.setChecked(self.config.font())
            self.exclude.setChecked(self.config.excluded())
            self.options.setChecked(self.config.options())

    def updateCheckboxes(self):
        self.onTop.setChecked(self.config.on_top())
        self.reSize.setChecked(self.config.resize())
        self.savePos.setChecked(self.config.save_position())
        self.saveButtons.setChecked(self.config.save_buttons())
        self.centerSize.setChecked(self.config.center())

    def saveButtonsStates(self):
        if self.config.save_buttons():
            self.config.set_toggle(self.toggle.isChecked())
            self.config.set_font(self.font.isChecked())
            self.config.set_excluded(self.exclude.isChecked())
            self.config.set_options(self.options.isChecked())

    def updateOptions(self):
        self.config.set_on_top(self.onTop.isChecked())
        self.config.set_resize(self.reSize.isChecked())
        self.config.set_center(self.centerSize.isChecked())
        self.config.set_save_position(self.savePos.isChecked())
        self.config.set_save_buttons(self.saveButtons.isChecked())

    # ----------- update events -----------#
    def showEvent(self, QShowEvent):
        self.updateCheckboxes()
        self.updateButtonStates()
        self.updateComponents()
        self.updateComposition()

    def closeEvent(self, QCloseEvent):
        if self.config.save_buttons():
            self.updateOptions()
            self.saveButtonsStates()
        if self.config.save_position(): self.config.set_position((self.x(), self.y()))