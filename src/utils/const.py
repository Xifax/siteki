# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

__version__ = '0.0.4'

_name = 'siteki'
_company = 'nonbyte'
_separator = '.'

WIDTH = 480
HEIGHT = 600

page_breakline = '<div style="page-break-before:always">'
page_end = '</div>'

# paths
ROOT = '../'
RES = 'res/'
ICONS = 'icons/'

# icons
LOGO = 'looking_glass.png'
PARSE = 'print.png'
PDF = 'pdf.png'
FONT = 'zoom.png'
TOGGLE = 'toggle.png'
EXCLUDE = 'excluded.png'
OPTIONS = 'cog.png'
QUIT = 'quit.png'
SHOW = 'show.png'

# fonts
FONT_MIN = 10
FONT_MAX = 36

PRETTY_FONTS = [u'A-OTF リュウミン Pr5 R-KL', u'A-OTF 教科書ICA Pro R', u'A-OTF 新正楷書CBSK1 Pro CBSK1']
KEY_FONT = u'ヒラギノ明朝 Pro W3'
KEY_SENSE_FONT = u'Calibri'
VERSE_FONT_SIZE = 18
KEY_FONT_SIZE = 12.5
KEY_SENSE_SIZE = 10

def get_pretty_font():
    import random
    return PRETTY_FONTS[random.randrange(0, len(PRETTY_FONTS))]

# key
SEPARATOR_SEGMENT = '_'
SEPARATOR_LENGTH = 110
NEWLINE = '<br/>'

# style
STYLE = 'plastique'