# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# external #
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QObject, QEvent, QTimer

# own #
from lyrics.grabber import LyricsGrabber
from utility.const import LS_WIDTH, LS_HEIGHT, PREVIEW_CHARS, TIP_VISIBLE,\
    get_pretty_font, VERSE_FONT_SIZE, KEY_SENSE_FONT, KEY_SENSE_SIZE,\
    ROOT, RES, ICONS, SEARCH, CLEAR

class LyricsSearch(QWidget):
    def __init__(self, parent=None):
        super(LyricsSearch, self).__init__(parent)

        self.lyrics = []

        self.layout = QGridLayout()

        self.artist = QLineEdit()
        self.title = QLineEdit()
        self.search = QPushButton('&Search')
        self.clear = QPushButton('&Clear')
        self.status = QLabel('')

        self.results = QListWidget()

        self.layout.addWidget(self.artist, 0, 0, 1, 2)
        self.layout.addWidget(self.title, 1, 0, 1, 2)
        self.layout.addWidget(self.search, 2, 0)
        self.layout.addWidget(self.clear, 2, 1)
        self.layout.addWidget(self.results, 3, 0, 1, 2)
        self.layout.addWidget(self.status, 4, 0, 1, 2)
        self.setLayout(self.layout)

        self.initComposition()
        self.initComponents()
        self.initActions()

        self.search.setFocus()

    def initComposition(self):
        self.setWindowTitle('Search for lyrics on web')
        self.setGeometry((QApplication.desktop().width() - self.width())/2, (QApplication.desktop().height() - self.height())/2, LS_WIDTH, LS_HEIGHT)

    def initComponents(self):
        self.artist.setPlaceholderText('artist name')
        self.artist.setToolTip('Press enter to begin searching')
        self.title.setPlaceholderText('track title')
        self.title.setToolTip('Press enter to begin searching')

        pretty_font = QFont(get_pretty_font(), VERSE_FONT_SIZE)
        self.artist.setFont(pretty_font)
        self.title.setFont(pretty_font)
        self.artist.setAlignment(Qt.AlignCenter)
        self.title.setAlignment(Qt.AlignCenter)

        self.search.setIcon(QIcon(ROOT + RES + ICONS + SEARCH))
        self.clear.setIcon(QIcon(ROOT + RES + ICONS + CLEAR))

        self.results.setWordWrap(True)
        self.results.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.results.setToolTip('Double click to paste into main dialog')

        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont(KEY_SENSE_FONT, KEY_SENSE_SIZE))
        self.status.setStyleSheet('QLabel {background-color: black; color:white; border: 1px solid white; border-radius: 4px;}')

        self.status.hide()
        self.results.hide()

    def initActions(self):
        self.search.clicked.connect(self.searchLyrics)
        self.clear.clicked.connect(self.clearFields)
        self.results.itemDoubleClicked.connect(self.pasteToMain)

        self.artist.returnPressed.connect(self.searchLyrics)
        self.title.returnPressed.connect(self.searchLyrics)

    #------------ actions ------------#
    def setInputRef(self, text_edit):
        self.in_ref = text_edit

    def clearFields(self):
        self.artist.clear()
        self.title.clear()

    def searchLyrics(self):
        if self.title.text() == '':
            self.flashInfo('Track title must be specified. No exceptions.')
        else:
            self.lyrics = LyricsGrabber.lookup_by_artist_title(unicode(self.artist.text()), unicode(self.title.text()))
            self.updateResutlsList()

    def updateResutlsList(self):
        self.results.clear()

        if self.lyrics:
            for lyric in self.lyrics:
                item = QListWidgetItem(10 * ' ' + LyricsGrabber.remove_empty_lines(lyric[0])
                                              .decode('UTF-8', 'ignore')
                                                [:PREVIEW_CHARS] + u'・・・')
                self.results.addItem(item)

                if lyric[1] is not '':
                    rate = str(lyric[1])
                else:
                    rate = '0.0'
                label = QLabel("<font style='font-size: 9pt; color: gray'>" + rate + "</font>")
                label.setAlignment(Qt.AlignTop)

                self.results.setItemWidget(item, label)

            self.results.show()
            self.adjustSize()
        else:
            self.results.hide()
            self.adjustSize()
            self.flashInfo('Alas, nothing were found!')

    def pasteToMain(self, item):
        self.in_ref.setText(self.lyrics[self.results.indexFromItem(item).row()][0].decode('UTF-8', 'ignore'))

    def flashInfo(self, text=''):
        self.status.setText(text)
        self.status.show()
        def hideInfo():
            self.status.hide()
        QTimer.singleShot(TIP_VISIBLE, hideInfo)