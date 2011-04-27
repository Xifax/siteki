# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

from mcab.mecabTool import MecabTool

def parse_verse(verses, ignore=[]):
#    parsed = MecabTool.parseToWordsFull(unicode(verses))
    parsed = []
    for verse in verses.split('\n\n'):
#        print unicode(verse)
        parsed.append(MecabTool.parseToWordsFull(unicode(verse)))
    verse_key = u''
    for paragraph in parsed:
        verse_key += '<br/>-------------------------------------------------<br/>'
        for word in paragraph:
            try:
                verse_key += word['word'] + '\t' + word['pronunciation'] + '<br/>'
            except KeyError:
                pass
    return verse_key