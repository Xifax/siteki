# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# internal #
import urllib2, pickle, os

# own #
from utility.const import FREQ_LIST, FREQ_LEMMATA, ROOT, RES, IGNORED

class FrequencyList():
    def __init__(self):
        self.range = None
        self.items = None
        self.data = None
        self.ignore = []
        self.processed = []
        self.file_path = ROOT + RES + IGNORED

    def checkIfInit(self):
        if self.data is None: return False
        else: return True

    def getFrequencyRange(self):
        success = False
        try:
            self.data = urllib2.urlopen(FREQ_LIST).read()
            # number frequency item
            self.items = int(self.data.split('\n')[-2:][0].split(' ')[0])
            # (min, max) frequencies
            self.range = (float(self.data.split('\n')[-2:][0].split(' ')[1]), float(self.data.split('\n')[4].split(' ')[1]))
            success = True
        except Exception:
            pass
        finally:
            return success

    def processData(self):
        for line in self.data.split('\n')[4 : -1]:
            # (item, number) ~ normalised
            self.processed.append( ( unicode(line.split(' ')[-1], 'utf-8'), int(line.split(' ')[-3]) ) )

    def getItemsListExFromRange(self, min, max):
        if max > min:
            # items not in range
            self.ignore = [ i[0] for i in filter (lambda e: (e[1] < min) or (e[1] > max), self.processed) ]
            return self.ignore

    def getItemsExFromNormalRange(self, min, max):
        return self.getItemsListExFromRange( int(self.items * min/100), int(self.items * max/100) )

    def saveIgnored(self):
        dump = open(self.file_path, 'w')
        pickle.dump(self.ignore, dump)
        dump.close()

    def loadIgnored(self):
        if os.path.exists(self.file_path):
            dump = open(self.file_path, 'r')
            self.ignore = pickle.load(dump)
            dump.close()