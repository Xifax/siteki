# -*- coding: utf-8 -*-

# external #
import MeCab
from jcconv import kata2hira

class MecabTool:
    @staticmethod
    def parseToWordsFull(text):
        mecab = MeCab.Tagger("")
    
        mnode = mecab.parseToNode(text.encode('utf8'))
        word_array = []
    
        while mnode:
            infos = {}
            infos['word'] = mnode.surface.decode('utf8')
            feature = mnode.feature.decode('utf8')
            array = feature.split(",")
            infos['type'] = array[0]
            infos['dform'] = array[4]
            infos['reading'] = array[5]
            infos['nform'] = array[6]
            try:
                infos['pronunciation'] = array[7]
            except IndexError:
                pass
            if not infos['type'] == "BOS/EOS":
                word_array.append(infos)
            mnode = mnode.next
    
        return word_array
    
    @staticmethod
    def parseToWordsOnly(text):
        words = MecabTool.parseToWordsFull(text)
        result = []
        for w in words:
            result.append(w['word'])
            
        return result
    
    @staticmethod
    def parseToReadingsKana(text):
        words = MecabTool.parseToWordsFull(text)
        result = []
        for w in words:
            result.append(w['pronunciation'])
            
        return result

    @staticmethod
    def findUsingF(f, seq):
        for item in seq:
            if f(item): return item

    @staticmethod
    def getWordPronunciationFromText(query, text):
        words = MecabTool.parseToWordsFull(text)
        answer = MecabTool.findUsingF(lambda word: query in word['word'] , words)
        try:
            return kata2hira(answer['pronunciation'])
        except Exception:
            return None
