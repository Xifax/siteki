# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# own #
from mcab.mecabTool import MecabTool

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
#            print 'Not found: ', query
            if query not in self.missed: self.missed.append(query)
        finally:
            return found

def parse_verse(verses, dictionary, ignore=[]):
    newline = '<br/>'
    separator = '_'

    dictionary.load_dictionaries()
    dictionary.clear_statistics()

    parsed = []
    for verse in verses.split('\n\n'):
        parsed.append(MecabTool.parseToWordsFull(unicode(verse)))
    verse_key = u''
    for paragraph in parsed:
        verse_key += newline + separator * 70 + newline
        for word in paragraph:
            lookup = dictionary.lookup(word['nform'])
            if lookup is not None:
                verse_key += word['nform'] + '\t' + ', '.join(lookup.senses_by_reading().keys()) + newline
                
    print 'Missed: ' + '\t'.join(dictionary.missed)
    return verse_key