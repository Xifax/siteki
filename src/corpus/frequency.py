# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# internal #
import urllib2, pickle, os

# own #
from utils.const import FREQ_LIST, FREQ_LEMMATA, ROOT, RES, IGNORED

class FrequencyList():
    def __init__(self):
        self.range = None
        self.items = None
        self.data = None
        self.ignore = []
        self.processed = []

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
            # (item, frequency)
#            self.processed.append( ( line.split(' ')[-1], float(line.split(' ')[-2]) ) )
            self.processed.append( ( unicode(line.split(' ')[-1], 'utf-8'), int(line.split(' ')[-3]) ) )

    def getItemsListInRange(self, min, max):
        if max > min:
#            self.ignore = [ i[0] for i in filter (lambda e: max > e[1] > min, self.processed) ]
            self.ignore = [ i[0] for i in filter (lambda e: (e[1] < min) or (e[1] > max), self.processed) ]
            return self.ignore

    def getItemsInNormalRange(self, min, max):
#        print  len(self.getItemsListInRange( int(self.items * min/100), int(self.items * max/100) ) )
#        return self.getItemsListInRange( self.range[1] *(float(min)/100.0), self.range[1] * (float(max)/100.0) )
        return self.getItemsListInRange( int(self.items * min/100), int(self.items * max/100) )

    def saveIgnored(self):
        dump = open(ROOT + RES + IGNORED, 'w')
        pickle.dump(self.ignore, dump)
        dump.close()

    def loadIgnored(self):
        if os.path.exists(ROOT + RES + IGNORED):
            dump = open(ROOT + RES + IGNORED, 'r')
            self.ignore = pickle.load(dump)
            dump.close()