# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

#TODO: add optional font tweak
#TODO: excluded items list
#TODO: options (center on resize, always on top, etc)
#TODO: hide to tray on close

# internal #
import sys, ctypes

# external #
from PyQt4.QtGui import QApplication

# own #
from gui.main import GUI
from utils.const import _name, __version__, _separator, _company

def main():
    app = QApplication(sys.argv)

    gui = GUI()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    id = _separator.join([_company, _name, _name, __version__.replace('.', '')])
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(id)
    try:
        main()
    except Exception, e:
        print e