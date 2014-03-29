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
        print '==========================================='
        print 'count: ', self.count
        # print 'text:'
        # print self.text
        data = {}

        names = (u'Название', u'Страна', u'Страны', u'Годы', u'Город',
                 u'Состав', u'Бывшие участники', u'Жанры', u'Язык')
        wikicode = mwparserfromhell.parse(self.text)
        templates = wikicode.filter_templates()
        if len(templates) == 0:
            return
        template = templates[0]
        print '++++++++++++++++++++++++++++++++++++++++++++'
        for param in template.params:
            name = unicode(param.name).strip()
            if name not in names:
                continue

            if name == u'Название':
                # ipdb; ipdb.set_trace()
                data['name'] = unicode(param.value).strip()
                print data['name']
            elif name == u'Страна':
                if self.count in (358, ):
                    ipdb.set_trace()

                if not unicode(param.value).strip():
                    continue
                strs = unicode(param.value)
                strs = [s.strip() for s in strs.split(',')]
                data['countries'] = list(set([s for s in strs if s]))
                print 'unicode: ', unicode(param.value)
                # print 'type: ', type(param.value)
                # print 'unparsed texts:'
                # for p in param.value.filter_text():
                #     print p
                print 'parsed:'
                print data['countries'][0]
            elif name == u'Страны':
                if self.count in (358, 338, ):
                    ipdb.set_trace()

                print 'unicode: ', unicode(param.value)
                # print 'type: ', type(param.value)
                # print 'unparsed texts:'
                # for p in param.value.filter_text():
                #     print p

                def vlog():
                    print 'parsed:'
                    for p in data['countries']:
                        print p


                tmpls = [tmpl for tmpl in param.value.filter_templates()]
                if tmpls:
                    def get_country(tmpl):
                        if len(tmpl.params) == 0:
                            return unicode(tmpl.name)
                        return unicode(tmpl.params[0])
                    data['countries'] = map(get_country, tmpls)
                    vlog()
                    continue

                links = [link for link in param.value.filter_wikilinks()]
                if links:
                    def get_country(link):
                        if link.text:
                            return unicode(link.text)
                        return unicode(link.title)
                    data['countries'] = map(get_country, links)
                    vlog()
                    continue

                # if self.count == 197:
                #     ipdb.set_trace()

                tags = [unicode(tg.tag) for tg in param.value.filter_tags()]
                strs = [unicode(s) for s in param.value.filter_text()]
                names = []
                for s in strs:
                    names.extend(s.split(','))
                names = [s.strip() for s in names]
                data['countries'] = list(set([s for s in names if s]))
                vlog()
            # else:
            #     # print 'name:', name
            #     # # ipdb.set_trace()
            #     # print 'value:', param.value
            #     pass
        # print data
        # ipdb.set_trace()

    def parse_country(self, param, verbose=False):
        def vlog():
            if not verbose:
                return

            print 'parsed countries:'
            for p in cntrs:
                print 'country: "{}"'.format(p)

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
