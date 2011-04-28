# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

#TODO: excluded items list
#TODO: hide to tray on close
#TODO: add progress bar

# internal #
import sys, ctypes

# external #
from PyQt4.QtGui import QApplication, QIcon

# own #
from gui.main import GUI
from utils.const import _name, __version__, _separator, _company,\
                        ROOT, RES, ICONS, LOGO

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ROOT + RES + ICONS + LOGO))

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