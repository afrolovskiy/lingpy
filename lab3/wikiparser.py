# coding: utf-8
import xml.sax

import mwparserfromhell


class MusicBand(object):

    def __init__(self, name):
        self.name = name


class WikiContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.need_parse = False
        self.is_page = False
        self.depth = 0
        self.text = None
        self.mband = None

    def startElement(self, name, attrs):
        if name == 'page':
            self.is_page = True
            self.depth = 0

    def endElement(self, name):
        if name == 'page':
            self.is_page = False

    def characters(self, content):
        if not self.is_page:
            return

        if '{{' in content:
            self.depth = self.depth + 1
            # print 'start: ', content, 'depth: ', self.depth

            if self.depth == 1 and u'Музыкальный коллектив' in content:
                # ipdb.set_trace()
                self.need_parse = True
                self.text = ''

        if self.need_parse:
            self.text += content

        if '}}' in content:
            self.depth = self.depth - 1
            # print 'end: ', content, 'depth: ', self.depth

            if self.need_parse and self.depth == 0:
                # ipdb.set_trace()
                self.need_parse = False
                self.parse()

    def parse(self):
        print self.text
        import ipdb; ipdb.set_trace()
        names = (u'Название', u'Страна', u'Годы', u'Город', u'Состав',
                 u'Бывшие участники', u'Жанры', u'Язык')
        wikicode = mwparserfromhell.parse(self.text)
        templates = wikicode.filter_templates()
        template = templates[0]
        for param in template.params:
            name = unicode(param.name).strip()
            if name not in names:
                continue

            if name == u'Название':
                ipdb; ipdb.set_trace()
                band_name = unicode(param.value).strip()
            else:
                print 'name:', name
                ipdb.set_trace()
                print 'value:', param.value
        ipdb.set_trace()
        print res


def parse(filename):
    with open(filename) as fin:
        xml.sax.parse(fin, WikiContentHandler())


if __name__ == "__main__":
    parse("dumps/ruwiki-20140324-pages-articles1.xml")
