# coding: utf-8
import xml.sax

import ipdb


class MusicBand(object):

    def __init__(self, name):
        self.name = name


class WikiContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.need_parse = False
        self.depth = 0
        self.text = None
        self.mband = None

    def characters(self, content):
        if '}}' in self.content:
            self.depth = self.depth - 1

            if self.need_parse:
                self.text += content

            if self.need_parse and self.depth == 0:
                self.need_parse = False

                text = self.text.strip('{}')
                elements = text.split('|')
                data = dict([el.split('=') for el in elements[1:]])
                ipdb.set_trace()

        elif u'{{' in content:
            self.depth = self.depth + 1

            if self.depth == 1 and u'Музыкальный коллектив' in content:
                self.need_parse = True
                self.text = content
            

def parse(filename):
    with open(filename) as fin:
        xml.sax.parse(fin, WikiContentHandler())


if __name__ == "__main__":
    parse("dumps/ruwiki-20140324-pages-articles1.xml")
