# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# own #
from mcab.mecabTool import MecabTool
from utils.const import KEY_FONT, KEY_FONT_SIZE, KEY_SENSE_FONT, KEY_SENSE_SIZE,\
                        SEPARATOR_SEGMENT, SEPARATOR_LENGTH, NEWLINE

# external #
from pkg_resources import resource_filename
from cjktools.resources import auto_format
#from cjktools.resources import kanjidic
from cjktools import scripts

class Dictionary:
    def __init__(self, config):
        self.config = config

        self.edict = None
#        self.kjd = None
        self.edict_file = resource_filename('cjktools_data', 'dict/je_edict')
        self.stats = []
        self.missed = []

    def load_dictionaries(self):
        if self.edict is None: self.edict = auto_format.load_dictionary(self.edict_file)
        #if self.kjd is None: self.kjd = kanjidic.Kanjidic()

    def clear_statistics(self):
        self.stats = []

    def lookup(self, query):
        found = None

        if self.config.ignore_kana():
            if len(scripts.script_types(query)) is 1:
                if scripts.script_type(query) is scripts.Script.Hiragana or scripts.script_type(query) is scripts.Script.Katakana:
                    return found
        try:
            found = self.edict[query]

            if self.config.ignore_duplicates():
                if found.word in self.stats: found = None
                else: self.stats.append(found.word)
        except KeyError:
            if query not in self.missed: self.missed.append(query)
        finally:
            return found

    @staticmethod
    def gloss(senses):
        toneDown = lambda str: str.replace('(', "<font style='color: gray;'>(").replace(')', ')</font>')
#        senses = [toneDown(s) for s in senses ]
        return filter (lambda e: '(P)' not in e, [toneDown(s) for s in senses ])

def parse_verse(verses, dictionary, ignore=[]):
    dictionary.load_dictionaries()
    dictionary.clear_statistics()

    parsed = []
    for verse in verses.split('\n\n'):
        parsed.append(MecabTool.parseToWordsFull(unicode(verse)))
    verse_key = u''
    for paragraph in parsed:
        verse_key += NEWLINE + SEPARATOR_SEGMENT * SEPARATOR_LENGTH + NEWLINE
        for word in paragraph:
            lookup = dictionary.lookup(word['nform'])
            if lookup is not None:
                # selecting senses by (probable) reading from source text
                reading = MecabTool.getWordPronunciationFromText(word['word'], unicode(verses))
                if reading is not None:
                    try:
                        verse_key += "<font style='font-family: " + KEY_FONT + "; font-size: " + str(KEY_FONT_SIZE) +"pt'>" + \
                                    word['nform'] + '\t' + reading + \
                                     "</font>\t<font style='font-family: " + KEY_SENSE_FONT + "; font-size: " + str(KEY_SENSE_SIZE) + "pt'>" + \
                                     ', '.join( Dictionary.gloss( lookup.senses_by_reading()[reading] ) ) + '</font>' + NEWLINE
                    except KeyError:
                        verse_key = update_key(verse_key, word, lookup)
                else: verse_key = update_key(verse_key, word, lookup)

    print 'Missed: ' + '\t'.join(dictionary.missed)
    return verse_key

def update_key(key, word, lookup):
    key += "<font style='font-family: " + KEY_FONT + "; font-size: " + str(KEY_FONT_SIZE) +"pt'>" + \
            word['nform'] + '\t' + \
           ', '.join(lookup.senses_by_reading().keys()) + \
            "</font>\t<font style='font-family: " + KEY_SENSE_FONT + "; font-size: " + str(KEY_SENSE_SIZE) + "pt'>" + \
           ', '.join(Dictionary.gloss(lookup.senses)) + '</font>' + NEWLINE
    return key