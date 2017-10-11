import re

from ply import lex as lex

from pyoracc.atf.common.atfbaselex import AtfBaseLexer


class AtfCDLILexer(AtfBaseLexer):

    def __init__(self, skipinvalid=False, debug=0):
        super(AtfCDLILexer, self).__init__(skipinvalid)
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)