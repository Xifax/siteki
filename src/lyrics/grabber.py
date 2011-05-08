# -*- coding=utf-8 -*-
__author__ = 'Yadavito'

# internal #
import urllib2
import threading
import re
from xml.dom.minidom import parseString
from chardet import detect

## Lyrics grabber.
#
# Retrieve lyrics from popular internet resources.
# As of now works with viewlyrics.com
# @todo: implement multiple resources
class LyricsGrabber:

    ## @var _timeout
    #  HTTP request timeout.

    ## @var _max
    #  Max number of lyrics expected.

    ## @var _candidate
    #  Lyrics candidates.

    ## @var _lock
    #  Thread lock for appending _candidate list.

    ## @var _pattern
    #  Regexp pattern for removing [*] blocks.

    _timeout = 3
    _max = 5
    _lock = threading.Condition(threading.Lock())
    _lyrics = None
    _pattern = re.compile('\[*?.*?\]')

    ## Lyrics receive handler.
    #  @param url Lyrics url.
    #  @param rate Lyrics rating.
    @staticmethod
    def _receive_lyrics(url, rate):
                    try:
                            cache = urllib2.urlopen(url, None, LyricsGrabber._timeout).read()
                    except Exception, e:
                        pass
                    else:
                            encoding = detect(cache)['encoding']
                            cache = cache.decode(encoding, 'ignore').encode('UTF-8', 'ignore')
                            LyricsGrabber._lock.acquire()
                            LyricsGrabber._lyrics.append((LyricsGrabber.remove_timestamps(cache), rate))
                            LyricsGrabber._lock.release()
                    return

    ## Retrieve lyrics.
    #  @param artist Song artist.
    #  @param title Song title.
    #  @return List of tuples for lyrics[0] coupled with rating[1].
    @staticmethod
    def lookup_by_artist_title(artist, title):
            LyricsGrabber._lyrics = []
            artist_token = urllib2.quote(artist.encode('utf-8'))
            title_token = urllib2.quote(title.encode('utf-8'))
            xml = "<?xml version=\"1.0\" encoding='utf-8'?>\r\n"
            xml += "<search filetype=\"lyrics\" artist=\"%s\" title=\"%s\" " % (artist_token, title_token)
            xml += "ClientCharEncoding=\"utf-8\"/>\r\n"
            request = xml
            url = 'http://www.viewlyrics.com:1212/searchlyrics.htm'
            try:
                    xml = urllib2.urlopen(url, request, LyricsGrabber._timeout).read()
                    elements = parseString(xml).getElementsByTagName('fileinfo')
            except Exception, e:
                    pass
            else:
                    threads = []
                    for element in elements:
                            url = element.getAttribute('link')
                            rate = element.getAttribute('rate')
                            threads.append(threading.Thread(target=LyricsGrabber._receive_lyrics, args=(url,rate)))
                            if len(threads) >= LyricsGrabber._max:
                                    break
                    for t in threads:
                            t.start()
                    for t in threads:
                            t.join()
                    pass
            return LyricsGrabber._lyrics

    ## Remove timestamps.
    #  @param lyric String with timestamps.
    #  @return String without timestamps.
    @staticmethod
    def remove_timestamps(lyric):
        return LyricsGrabber._pattern.sub('', lyric)

    ## Remove empty lines from text.
    #  @param lyric String with lyrics.
    #  @return String without empty lines (if there were any).
    @staticmethod
    def remove_empty_lines(lyric):
        return filter(lambda x: not re.match(r'^\s*$', x), lyric)

#artist = u'梶浦由記'
#title = u'Fake Wings'
#artist = 'Queen'
#title = 'Show must go on'
#artist = u'ルルティア'
#title = u'Seirios'
#lyrics = LyricsGrabber.lookup_by_artist_title(artist, title)
#for lyric in lyrics:
#    print lyric[0], lyric[1]
