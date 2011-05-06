# -*- coding=utf-8 -*-

__author__ = 'Yadavito'

# external #
from PyQt4.QtGui import QPrinter, QTextDocument, QPrintPreviewDialog
from PyQt4.QtCore import Qt

# own #
from util.const import page_breakline, page_end, ROOT

def print_document(document, verse_key, pdf = False, copies=1, skip=False):
    printer = QPrinter(QPrinter.HighResolution)

    if not pdf: printer.setOutputFormat(QPrinter.NativeFormat)
    else:
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(ROOT + 'verse.pdf')
    printer.setPaperSize(QPrinter.A4)
    printer.setCopyCount(copies)

    printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)

    doc = QTextDocument()
    doc.setHtml(concatenate_pages(document, verse_key, skip))

    dialog = QPrintPreviewDialog(printer)
    dialog.setWindowFlags(Qt.Window)
    dialog.setWindowTitle('Print preview: parse results')

    def preview(): doc.print_(printer)

    dialog.paintRequested.connect(preview)
    dialog.exec_()

def concatenate_pages(original, key, skip):
    if skip: return original + page_breakline + ' ' + page_end + page_breakline + key + page_end
    else: return  original + page_breakline + key + page_end