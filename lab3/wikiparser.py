# coding: utf-8
import sys
from select import select

import ipdb
import xml.sax

import mwparserfromhell

PARSED_KEYS = (
    u'Название',
    u'Страна',
    u'Страны',
    u'Жанр',
    u'Жанры',
    u'Годы',
    u'Состав',
    u'Бывшие_участники',
)

PARAMS = (
    'name',
    'countries',
    'countries',
    'styles',
    'styles',
    'years',
    'members',
    'former_participants',
)

PARAMS_MAP = dict(zip(PARSED_KEYS, PARAMS))


class MusicBand(object):

    def __init__(self, name, countries=None, styles=None, years=None,
                 members=None, former_participants=None):
        self.name = name
        self.countries = countries or ''
        self.styles = styles or ''
        self.years = years or ''
        self.members = members or ''
        self.former_participants = former_participants or ''

    def write2stdout(self):
        print 'name: ', self.name
        print 'countries: ', self.countries
        print 'styles: ', self.styles
        print 'years: ', self.years
        print 'members: ', self.members
        print 'former_participants: ', self.former_participants

    def write2db(self):
        pass
        


class WikiMusicBandParser(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.need_parse = False
        self.is_page = False
        self.depth = 0
        self.text = None
        self.count = 0

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

            if self.depth == 1 and u'Музыкальный коллектив' in content:
                self.need_parse = True
                self.text = ''

        if self.need_parse:
            self.text += content

        if '}}' in content:
            self.depth = self.depth - 1

            if self.need_parse and self.depth == 0:
                self.need_parse = False
                self.parse()

    def parse(self):
        wikicode = mwparserfromhell.parse(self.text)
        templates = wikicode.filter_templates()

        if len(templates) == 0:
            return

        params = {}        
        template = templates[0]
        for param in template.params:
            name = unicode(param.name).strip()

            if name not in PARSED_KEYS:
                continue

            key = PARAMS_MAP[name]
            value = unicode(param.value).strip()
            params[key] = value
        
        print params.keys()
        band = MusicBand(**params)
        band.write2stdout()

        print "Press any key to continue..."
        rlist, wlist, xlist = select([sys.stdin], [], [])
        sys.stdin.readline()


def parse(filename):
    with open(filename) as fin:
        xml.sax.parse(fin, WikiMusicBandParser())


if __name__ == "__main__":
    parse("dumps/ruwiki-20140324-pages-articles1.xml")
