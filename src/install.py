# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# internal #
import sys
import urllib
import subprocess
import os

# own #
from utility.const import URL_SU, URL_MECAB, URL_PYQT, packages

def dlProgress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("Download progress: %d%%   \r" % percent)

def downloadWithProgressbar(url):
    file_name = url.split('/')[-1]
    print 'Downloading ' + file_name
    urllib.urlretrieve(url, file_name, reporthook=dlProgress)
    return file_name

def download_and_install(file_url):
        file = downloadWithProgressbar(file_url)
        subprocess.call('./' + file)
        os.remove('./' + file)
try:
    from setuptools.command import easy_install
except ImportError:
    print 'Please, install easy_install!'
    if raw_input('Download setuptools now? [y/n]: ') == ('y' or 'Y'):
        download_and_install(URL_SU)
    else: sys.exit(0)

def install_with_easyinstall(package):
    try:
        __import__(package)
        in_system.append(package)
    except ImportError:
        print 'Installing ' + package
        try:
            easy_install.main(['-U', package])
            installed.append(package)
        except Exception:
            problematic.append(package)

if __name__ == '__main__':
    installed = []; in_system = []; problematic = []
    for package in packages:
        install_with_easyinstall(package)

    # PyQt
    try:  import PyQt4
    except ImportError: download_and_install(URL_PYQT)
    # MeCab
    if raw_input('Download and install MeCab? [y/n]: ') == ('y' or 'Y'):
        download_and_install(URL_MECAB)

    print 'Install/Update complete. Status:\n'
    print '\n'.join(installed), '\n\n(total installed: ' + str(len(installed)) + ')\n'
    print '\n------------ # # # ------------\n'
    print '\n'.join(in_system), '\n\n(already in system: ' + str(len(in_system)) + ')\n'
    print '\n------------ # # # ------------\n'
    print '\n'.join(problematic), '\n\n(erred somehow: ' + str(len(problematic)) + ')\n'
    raw_input('Press any key and so on.')
    
