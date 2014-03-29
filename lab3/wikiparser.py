# coding: utf-8
import ipdb
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
        if self.count > 500:
            raise Exception('Limit exceeded')
        self.count = self.count + 1
        data = {}

        print '==========================================='
        print 'count: ', self.count

        names = (u'Название', u'Страна', u'Страны', u'Годы', u'Город',
                 u'Состав', u'Бывшие участники', u'Жанры', u'Язык')
        wikicode = mwparserfromhell.parse(self.text)
        templates = wikicode.filter_templates()

        if len(templates) == 0:
            # description is empty
            return

        template = templates[0]
        
        for param in template.params:
            name = unicode(param.name).strip()
            if name not in names:
                continue

            if name == u'Название':
                # ipdb; ipdb.set_trace()
                data['name'] = unicode(param.value).strip()
                print data['name']
            elif name in (u'Страна', u'Страны'):
                if self.count in (358, 338, ):
                    ipdb.set_trace()

                print 'unicode: ', unicode(param.value)
                data['countries'] = self.parse_country(param, True)

    def parse_country(self, param, verbose=False):
        def vlog():
            if not verbose:
                return

            print 'parsed countries:'
            for cntr in cntrs:
                print u'country: "{}"'.format(cntr)

        cntrs = []

        if not unicode(param.value).strip():
            # value is empty
            vlog()
            return cntrs

        tmpls = [tmpl for tmpl in param.value.filter_templates()]
        if tmpls:
            def get_country(tmpl):
                if len(tmpl.params) == 0:
                    return unicode(tmpl.name)
                return unicode(tmpl.params[0])
            
            cntrs = map(get_country, tmpls)
            vlog()
            return cntrs

        links = [link for link in param.value.filter_wikilinks()]
        if links:
            def get_country(link):
                if link.text:
                    return unicode(link.text)
                return unicode(link.title)

            cntrs = map(get_country, links)
            vlog()
            return cntrs

        tags = [unicode(tg.tag) for tg in param.value.filter_tags()]
        strs = [unicode(s) for s in param.value.filter_text()]
        names = []
        for s in strs:
            names.extend(s.split(','))
        names = [s.strip() for s in names]
        
        cntrs = list(set([s for s in names if s]))
        vlog()
        return cntrs


def parse(filename):
    with open(filename) as fin:
        xml.sax.parse(fin, WikiContentHandler())


if __name__ == "__main__":
    parse("dumps/ruwiki-20140324-pages-articles1.xml")
