# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# own #
from gui.imessage import InfoMessage
from gui.exlist import UserList
from corpus.frequency import FrequencyList
from options.settings import Config
from parse.verse import parse_verse, Dictionary, sift_nonj_characters, check_scripts
from printer.printing import print_document
from util.const import __version__, _name, WIDTH, HEIGHT,\
                        ROOT, RES, ICONS, LOGO,\
                        PARSE, PDF, FONT, TOGGLE, EXCLUDE, OPTIONS, SHOW, QUIT,\
                        FONT_MAX, FONT_MIN, VERSE_FONT_SIZE, get_pretty_font,\
                        URL_NAME
# external #
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QSize, QThread, pyqtSignal, QString
from gui.qrangeslider import QRangeSlider

class GUI(QWidget):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        # internal modules
        self.config = Config()
        self.dictionary = Dictionary(self.config)
        self.frequencyList = FrequencyList()
        self.message = InfoMessage(self)
        self.userList = UserList()

        self.layout = QGridLayout()

        self.progress = QProgressBar()

        self.input = QTextEdit()
        self.parse = QPushButton('Par&se')
        self.topdf = QPushButton('P&DF')
        self.toggle = QPushButton('&Toggle')
        self.font = QPushButton('&Input')

        self.exclude = QPushButton('E&xclude')
        self.options = QPushButton('&Options')

        self.fontGroup = QGroupBox('Prettify')
        self.excludeGroup = QGroupBox('Exceptions')
        self.optionsGroup = QGroupBox('Settings')

        # fonts contents
        self.changeFont = QFontComboBox()
        self.changeSize = QDial()
        self.changeSelected = QRadioButton('Zoom selected')
        self.changeAll = QRadioButton('Zoom all')
        self.prettify = QPushButton('Prettify!')
        self.normalize = QPushButton('Normalize')

        self.fontLayout = QGridLayout()
        self.fontLayout.addWidget(self.changeSelected, 0, 0, 1, 1)
        self.fontLayout.addWidget(self.changeAll, 1, 0, 1, 1)
        self.fontLayout.addWidget(self.changeSize, 0, 1, 2, 1)
        self.fontLayout.addWidget(self.changeFont, 0, 2, 1, 2)
        self.fontLayout.addWidget(self.prettify, 1, 2, 1, 1)
        self.fontLayout.addWidget(self.normalize, 1, 3, 1, 1)
        self.fontGroup.setLayout(self.fontLayout)

        # exclude contents
        self.ignoreKana = QCheckBox('Ignore standalone kana')
        self.ignoreDuplicates = QCheckBox('Do not repeat the same words')
        self.byFrequency = QPushButton('By frequency')
        self.customExclude = QPushButton('User list')

        self.frequencyRange = QRangeSlider()
        self.loadList = QPushButton('From corpus')
        self.updateIgnore = QPushButton('Update')

        self.excludeLayout = QGridLayout()
        self.excludeLayout.addWidget(self.loadList, 0, 0)
        self.excludeLayout.addWidget(self.updateIgnore, 0, 1)
        self.excludeLayout.addWidget(self.frequencyRange, 1, 0, 1, 2)
        self.excludeLayout.addWidget(self.byFrequency, 2, 0)
        self.excludeLayout.addWidget(self.customExclude, 2, 1)
        self.excludeLayout.addWidget(self.ignoreKana, 3, 0, 1, 2)
        self.excludeLayout.addWidget(self.ignoreDuplicates, 4, 0, 1, 2)
        self.excludeGroup.setLayout(self.excludeLayout)

        self.corpusUpdated = False

        # options contents
        self.onTop = QCheckBox('Always on top')
        self.reSize = QCheckBox('Allow automatic resize')
        self.centerSize = QCheckBox('Center on resize')
        self.savePos = QCheckBox('Save window position on exit')
        self.saveSize = QCheckBox('Save window size on exit')
        self.saveButtons = QCheckBox('Save buttons states on exit')
        self.toTray = QCheckBox('Send to tray on close')
        self.plastique = QCheckBox("Use 'plastique' style")
        self.nextPage = QCheckBox('Skip page after main text')

        self.optionsLayout = QVBoxLayout()
        self.optionsLayout.addWidget(self.onTop)
        self.optionsLayout.addWidget(self.reSize)
        self.optionsLayout.addWidget(self.centerSize)
        self.optionsLayout.addWidget(self.savePos)
        self.optionsLayout.addWidget(self.saveSize)
        self.optionsLayout.addWidget(self.saveButtons)
        self.optionsLayout.addWidget(self.toTray)
        self.optionsLayout.addWidget(self.plastique)
        self.optionsLayout.addWidget(self.nextPage)
        self.optionsGroup.setLayout(self.optionsLayout)

        # progress
        self.layout.addWidget(self.progress, 0, 0, 1, 4)
        # buttons
        self.layout.addWidget(self.parse, 1, 0)
        self.layout.addWidget(self.topdf, 1, 1)
        self.layout.addWidget(self.font, 1, 2)
        self.layout.addWidget(self.toggle, 1, 3)
        # font group
        self.layout.addWidget(self.fontGroup, 2, 0, 1, 4)
        # text edit
        self.layout.addWidget(self.input, 3, 0, 1, 4)
        # exclude/options groups
        self.layout.addWidget(self.excludeGroup, 4, 0, 1, 4)
        self.layout.addWidget(self.optionsGroup, 5, 0, 1, 4)
        # buttons again
        self.layout.addWidget(self.exclude, 6, 0, 1, 2)
        self.layout.addWidget(self.options, 6, 2, 1, 2)

        self.setLayout(self.layout)

        # tray icon
        self.trayIcon = QSystemTrayIcon(self)
        self.forbidClose = True

        self.initComposition()
        self.initComponents()
        self.initActions()

    def initComposition(self):
        self.setWindowTitle(_name + ' ' + __version__)

        desktop = QApplication.desktop()
        self.setGeometry((desktop.width() - WIDTH)/2, (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

        if self.config.save_position(): self.move(self.config.get_position()[0], self.config.get_position()[1])
        if self.config.save_size(): self.setGeometry(self.x(), self.y(), self.config.get_size()[0], self.config.get_size()[1])
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

        # font dialog
        self.changeSize.setRange(FONT_MIN, FONT_MAX)
        self.changeSize.setNotchesVisible(True)
        self.changeSize.setMaximumHeight(40)

        self.changeSize.setValue(16.5)
        self.changeSelected.setChecked(True)

        # progress
        self.progress.setMaximumHeight(14)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setRange(0, 0)
        self.progress.hide()

        # tray
        self.trayIcon.setIcon(QIcon(ROOT + RES + ICONS + LOGO))
        self.trayIcon.setToolTip(u'詩的なパーサーであります')

        # tooltips
        self.updateTooltips()

        # exclude
        self.byFrequency.setCheckable(True)

        self.loadList.hide()
        self.updateIgnore.hide()
        self.frequencyRange.hide()

        self.frequencyRange.setBackgroundStyle('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #111, stop:1 #333);')
        self.frequencyRange.handle.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #145, stop:1 #393);')

        # inactive
        self.onTop.setEnabled(False)

    def initActions(self):
        # analysis buttons
        self.parse.clicked.connect(self.parseNPrint)
        self.topdf.clicked.connect(self.parseNPDF)
        # options buttons
        self.toggle.clicked.connect(self.toggleInput)
        self.font.clicked.connect(self.toggleFont)
        self.exclude.clicked.connect(self.toggleExclude)
        self.options.clicked.connect(self.toggleOptions)
        # options checkboxes
        self.onTop.clicked.connect(self.updateOptions)
        self.centerSize.clicked.connect(self.updateOptions)
        self.reSize.clicked.connect(self.updateOptions)
        self.saveButtons.clicked.connect(self.updateOptions)
        self.savePos.clicked.connect(self.updateOptions)
        self.saveSize.clicked.connect(self.updateOptions)
        self.toTray.clicked.connect(self.updateOptions)
        self.plastique.clicked.connect(self.updateOptions)
        self.nextPage.clicked.connect(self.updateOptions)
        # exclude checkboxes
        self.ignoreKana.clicked.connect(self.updateOptions)
        self.ignoreDuplicates.clicked.connect(self.updateOptions)
        # font dialog
        self.changeSize.valueChanged.connect(self.updateFontSize)
        self.changeFont.currentFontChanged.connect(self.updateFontSize)
        self.prettify.clicked.connect(self.prettifyFont)
        self.normalize.clicked.connect(self.normalizeInput)

        # input
        self.input.textChanged.connect(self.updateInputSize)

        # tray
        self.trayIcon.activated.connect(self.restoreFromTray)
        self.trayMenu = QMenu()
        self.trayMenu.addAction(QAction(QIcon(ROOT + RES + ICONS + QUIT), '&Quit', self, triggered=self.quit))
        self.trayMenu.addAction(QAction(QIcon(ROOT + RES + ICONS + SHOW), '&Show', self, triggered=self.showHide))
        self.trayIcon.setContextMenu(self.trayMenu)

        # exclude
        self.byFrequency.clicked.connect(self.toggleFrequencyExclude)
        updateIgnore = QMenu()
        updateIgnore.addAction(QAction('Exclude items outside of range', self, triggered=self.setIgnoreSet))
        updateIgnore.addAction(QAction('Restore from file', self, triggered=self.loadExFromFile))
        updateIgnore.addAction(QAction('Save to file', self, triggered=self.saveExToFile))
        self.updateIgnore.setMenu(updateIgnore)
        self.loadList.clicked.connect(self.initCorpus)

        self.customExclude.clicked.connect(self.showCustomExclude)

    def updateTooltips(self):
#        self.setStyleSheet('QToolTip { background-color: black; color: white; border: 1px solid white; border-radius: 2px; }')

        # buttons
        self.parse.setToolTip('Analyze text and print results')
        self.topdf.setToolTip('Analyze text and save results to pdf')
        self.font.setToolTip('Font tweaks')
        self.toggle.setToolTip('Show/hide input field')
        self.exclude.setToolTip('Item exclusions: options and ignore list')
        self.options.setToolTip('General application settings')

        # in groups
        self.prettify.setToolTip("Set one of those 'shiny' fonts and change font size")
        self.normalize.setToolTip('Remove non-japanese characters')

        # input
        self.input.setToolTip("I-It's not like you should paste something!")

        # exclude
        self.frequencyRange.setToolTip('Normalised frequencies')
        self.loadList.setToolTip('Get frequencies from ' + URL_NAME)
        self.updateIgnore.setToolTip('Update active set of excluded items')

    #------------- position -------------#
    def centerWidget(self):
        desktop = QApplication.desktop()
        self.move((desktop.width() - self.width())/2, (desktop.height() - self.height())/2)

    def updateComposition(self):
        if self.config.resize(): self.adjustSize()
        if self.config.center(): self.centerWidget()
        self.updateInputSize()

    def updateComponents(self):
        self.toggleInput()
        self.toggleFont()
        self.toggleExclude()
        self.toggleOptions()

    def moveMessage(self):
        self.message.move(self.x() + (self.width() - self.message.width())/2, self.y() + self.height() + self.message.height())

    def moveEvent(self, QMoveEvent):
        self.moveMessage()

    def resizeEvent(self, QResizeEvent):
        self.moveMessage()

    # ------------- actions --------------#
    def setupParserThread(self, pdf = False):
        self.progress.show()
        self.parser = ParserThread(self.input.toPlainText(), self.dictionary,
                                   self.frequencyList.ignore + self.userList.user_list, pdf)
        self.parser.done.connect(self.parsingFinished)
        self.parser.start()

    def parseNPrint(self):
        if not self.input.toPlainText() == '': self.setupParserThread()
        else: self.message.showInfo('Would you kindly paste some delicious text?', True)

    def parseNPDF(self):
        if not self.input.toPlainText() == '': self.setupParserThread(True)
        else: self.message.showInfo('Well, pdf convertor needs some text too, duh!', True)

    # ------------- interface ------------#
    def updateInputSize(self):
        correction = 90
        contents_height = self.input.document().documentLayout().documentSize().toSize().height()
        if contents_height > self.input.height():
            # check if new height goes over desktop limits
            if contents_height >= QApplication.desktop().height():
                contents_height = QApplication.desktop().height() - correction*2

            self.resize(QSize(self.width(), contents_height + correction))
            # reposition dialog, in case of considerable height value
            if self.y() + self.height() >= QApplication.desktop().height():
                self.move(self.x(), 10)

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
        self.saveSize.setChecked(self.config.save_size())
        self.saveButtons.setChecked(self.config.save_buttons())
        self.centerSize.setChecked(self.config.center())
        self.toTray.setChecked(self.config.to_tray())
        self.plastique.setChecked(self.config.plastique())
        self.nextPage.setChecked(self.config.skip_page())

        self.ignoreKana.setChecked(self.config.ignore_kana())
        self.ignoreDuplicates.setChecked(self.config.ignore_duplicates())

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
        self.config.set_save_size(self.saveSize.isChecked())
        self.config.set_save_buttons(self.saveButtons.isChecked())
        self.config.set_to_tray(self.toTray.isChecked())
        self.config.set_plastique(self.plastique.isChecked())
        self.config.set_skip_page(self.nextPage.isChecked())

        self.config.set_ignore_kana(self.ignoreKana.isChecked())
        self.config.set_ignore_duplicates(self.ignoreDuplicates.isChecked())

    def toggleFrequencyExclude(self):
        if self.byFrequency.isChecked():
            self.loadList.show()
            self.updateIgnore.show()
            if self.corpusUpdated: self.frequencyRange.show()
        else:
            self.loadList.hide()
            self.updateIgnore.hide()
            self.frequencyRange.hide()

    # -------------- fonts ----------------#
    def updateFontSize(self):
        if self.changeAll.isChecked():
            font = self.changeFont.currentFont()
            font.setPointSizeF(self.changeSize.value())
            self.input.setFont(font)
        else:
            self.input.setFont(self.changeFont.currentFont())
            self.input.setFontPointSize(self.changeSize.value())

    def prettifyFont(self):
        shiny = QFont(get_pretty_font(), VERSE_FONT_SIZE)

        self.changeFont.setCurrentFont(QFont(shiny))
        self.changeSize.setValue(VERSE_FONT_SIZE)
        self.input.setFont(shiny)

        self.updateInputSize()

    # ------------- input data --------------#
    def normalizeInput(self):
        while check_scripts(self.input.toPlainText()):
            self.input.setHtml(sift_nonj_characters(unicode(self.input.toHtml()), unicode(self.input.toPlainText())))

    # ----------- update events -------------#
    def showEvent(self, QShowEvent):
        self.updateCheckboxes()
        self.updateButtonStates()
        self.updateComponents()
        self.updateComposition()

    def saveAndQuit(self):
        if self.config.save_buttons():
            self.updateOptions()
            self.saveButtonsStates()
        if self.config.save_position(): self.config.set_position((self.x(), self.y()))
        if self.config.save_size(): self.config.set_size((self.width(), self.height()))

    def closeEvent(self, QCloseEvent):
        if self.config.to_tray() and self.forbidClose:
            self.hide()
            self.trayIcon.show()
            QCloseEvent.ignore()
        else:
            self.saveAndQuit()
            QCloseEvent.accept()

    def restoreFromTray(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.trayIcon.hide()

    def quit(self):
        self.forbidClose = False
        self.close()

    def showHide(self):
        self.show()
        self.trayIcon.hide()
        
    def parsingFinished(self, success, data, pdf):
        if success:
            self.progress.hide()
            print_document(self.input.toHtml(), data, pdf, skip=self.config.skip_page())

    # -------------- exclude ----------------#
    def initCorpus(self):
        self.progress.show()
        self.corpusThread = CorpusThread(self.frequencyList)
        self.corpusThread.done.connect(self.updateFrequencies)
        self.corpusThread.start()

    def setIgnoreSet(self):
        if self.frequencyList.checkIfInit():
            self.frequencyList.getItemsExFromNormalRange(self.frequencyRange.getRange()[0], self.frequencyRange.getRange()[1])
            self.message.showInfo(str(len(self.frequencyList.ignore)) + ' items will be ignored!')
        else: self.message.showInfo('You should initialize corpus or restore set from file', True)

    def updateFrequencies(self, success):
        if success:
            self.corpusUpdated = True
            self.progress.hide()

            self.frequencyRange.show()
            self.frequencyRange.setToolTip('Normalised distribution (actual min: ' + str(self.frequencyList.range[0]) + ' max: ' +\
            str(self.frequencyList.range[1]) + ')')

            self.frequencyRange.setMin(0)
            self.frequencyRange.setMax(100)
            self.frequencyRange.setRange(0, 80)
            self.message.showInfo(str(self.frequencyList.items) + ' items in corpus')
        else: self.message.showInfo('Could not get frequency list from ' + URL_NAME, True)

    def loadExFromFile(self):
        self.frequencyList.loadIgnored()
        self.message.showInfo('Restored from ' + self.frequencyList.file_path)

    def saveExToFile(self):
        self.frequencyList.saveIgnored()
        self.message.showInfo('Saved to ' + self.frequencyList.file_path)

    def showCustomExclude(self):
        self.userList.show()

### processing threads ###
class ParserThread(QThread):
    done = pyqtSignal(bool, QString, bool)

    def __init__(self, inputPlain, dictionary, ignore, pdf = False, parent = None):
        super(ParserThread, self).__init__(parent)
        self.ignore = ignore
        self.plain = inputPlain
        self.dict = dictionary
        self.pdf = pdf
        
    def run(self):
        self.data = parse_verse(self.plain, self.dict, self.ignore)
        self.done.emit(True, self.data, self.pdf)

class CorpusThread(QThread):
    done = pyqtSignal(bool)
    
    def __init__(self, fList, parent = None):
        super(CorpusThread, self).__init__(parent)
        self.fList = fList

    def run(self):
        success = True
        if not self.fList.checkIfInit():
            if self.fList.getFrequencyRange():
                self.fList.processData()
            else: success = False
        self.done.emit(success)

