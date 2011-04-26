# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

from mcab.mecabTool import MecabTool

def parse_verse(verse, ignore=[]):
    parsed = MecabTool.parseToWordsFull(unicode(verse))
    verse_key = u''
    for word in parsed:
        try:
            verse_key += word['word'] + '\t' + word['pronunciation'] + '<br/>'
        except KeyError:
            pass
    return verse_key