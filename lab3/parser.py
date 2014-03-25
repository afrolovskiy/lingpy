# coding: utf-8

import os

import ply.lex as lex
import ply.yacc as yacc


class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = (os.path.split(os.path.splitext(__file__)[0])[1] + "_" +
                       self.__class__.__name__)
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self, text):
        result = yacc.parse(text)
        print result


class WikiDataParser(Parser):

    tokens = ('BEGIN', 'END', 'EQUALS', 'PIPE', 'VALUE')

    t_BEGIN = r'\{\{'
    t_END = r'\}\}'
    t_EQUALS = r'\='
    t_PIPE = r'\|'
    t_VALUE = r'[^{}|]+'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    t_ignore = ' \t'

    def p_description(self, p):
        'description : BEGIN VALUE statements_list END'
        p[0] = (p[2], p[3])

    def p_statement_list_empty(self, p):
        'statements_list : '
        p[0] = {}

    def p_statement_list(self, p):
        'statements_list : PIPE statement statements_list'
        p[0] = p[2]
        p[0].update(p[3])

    def p_statement(self, p):
        '''
        statement : VALUE EQUALS VALUE
                  | VALUE EQUALS description
        '''
        p[0] = {p[1]: p[3]}

    def p_error(self, p):
        print u'Syntax error at "%s"' % p.value

if __name__ == '__main__':
    WikiDataParser().run(
        u'''
        {{Музыкальный коллектив
        |Название = The Beatles
        |Ключ = Beatles
        |Лого = Beatles logo.svg
        |Фото = {{часть изображения
        | изобр = Beatles ad 1965.JPG
        | позиция = center
        }}
        }}
        '''
    )
