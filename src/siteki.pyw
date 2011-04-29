# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

#TODO: excluded items list
#TODO: immediately update 'on top' behaviour

# internal #
import sys, ctypes, platform

# external #
from PyQt4.QtGui import QApplication, QIcon

# own #
from gui.main import GUI
from utils.const import _name, __version__, _separator, _company,\
                        ROOT, RES, ICONS, LOGO,\
                        STYLE

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ROOT + RES + ICONS + LOGO))

    gui = GUI()
    if gui.config.plastique(): app.setStyle(STYLE)
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    if platform.release() is '7':
        id = _separator.join([_company, _name, _name, __version__.replace('.', '')])
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(id)
    try:
        main()
    except Exception, e:
        print e