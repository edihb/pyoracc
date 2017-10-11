'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''


# -*- coding: utf-8 -*-
from __future__ import print_function

import warnings

from ply import lex as lex

from pyoracc import _pyversion
from pyoracc.atf.common.atflexicon import AtfLexicon


class AtfBaseLexer(object):

    states = AtfLexicon.STATES
    inc_states = AtfLexicon.INC_STATES
    inclusive_state_names = AtfLexicon.INCLUSIVE_STATE_NAMES
    exc_states = AtfLexicon.EXC_STATES
    exclusive_state_names = AtfLexicon.EXCLUSIVE_STATE_NAMES
    keyword_tokens = AtfLexicon.KEYWORD_TOKENS
    base_tokens = AtfLexicon.BASE_TOKENS
    dollar_keywords = AtfLexicon.DOLLAR_KEYWORDS
    translation_keywords = AtfLexicon.TRANSLATION_KEYWORDS
    protocol_keywords = AtfLexicon.PROTOCOL_KEYWORDS
    protocols = AtfLexicon.PROTOCOLS
    long_argument_structures = AtfLexicon.LONG_ARGUMENT_STRUCTURES
    structures = AtfLexicon.STRUCTURES
    tokens = AtfLexicon.TOKENS

    t_nonequals_EQUALS = AtfLexicon.T_EQUALS
    t_flagged_EQUALS = AtfLexicon.T_EQUALS
    t_flagged_parallel_para_HAT = "[\ \t]*\^[\ \t]*"
    t_flagged_STAR = AtfLexicon.T_STAR
    t_flagged_QUERY = AtfLexicon.T_QUERY
    t_flagged_EXCLAIM = AtfLexicon.T_EXCLAIM
    t_flagged_HASH = AtfLexicon.T_HASH
    t_transctrl_MINUS = AtfLexicon.T_TRANSCTRL_MINUS
    t_parallel_QUERY = AtfLexicon.T_QUERY
    t_INITIAL_transctrl_PARENTHETICALID = "\([^\n\r]*\)"
    t_PARBAR = AtfLexicon.T_PARBAR
    t_COMMA = AtfLexicon.T_COMMA
    t_TO = AtfLexicon.T_TO
    t_FROM = AtfLexicon.T_FROM
    t_MINUS = AtfLexicon.T_MINUS
    t_DOLLAR = AtfLexicon.T_DOLLAR
    t_STAR = AtfLexicon.T_STAR
    t_QUERY = AtfLexicon.T_QUERY
    t_EXCLAIM = AtfLexicon.T_EXCLAIM
    t_HASH = AtfLexicon.T_HASH
    t_AMPERSAND = AtfLexicon.T_AMPERSAND

    t_lemmatize_SEMICOLON = r'\;[\ \t]*'
    t_lemmatize_ID = "[^\;\n\r]+"
    t_text_ID = "[^\ \t \n\r]+"
    nonflag = r'[^\ \t\#\!\^\*\?\n\r\=]'
    many_nonflag = nonflag + '*'
    internalonly = r'[^\n\^\r\=]'
    many_int_then_nonflag = '(' + internalonly + '*' + nonflag + '+' + ')'
    intern_or_nonflg = '(' + many_int_then_nonflag + '|' + many_nonflag + ')'
    nonflagnonwhite = r'[^\ \t\#\!\^\*\?\n\r\=]'
    t_labeled_ID = "^[^\n\r]+"
    translation_regex2 = '([^\^\n\r]|([\n\r](?=[ \t])))*'
    translation_regex1 = '([^\?\^\n\r]|([\n\r](?=[ \t])))'
    white = r'[\ \t]*'
    flagged_regex = (white + '(' + nonflagnonwhite + intern_or_nonflg +
                     ')' + white)
    translation_regex = white + translation_regex1 + translation_regex2 + white

    def __init__(self, skipinvalid):
        self.skipinvalid = skipinvalid

    @staticmethod
    def _keyword_dict(tokens, extra):
        keywords = {token.lower(): token for token in tokens}
        firstcap = {token.title(): token for token in tokens}
        keywords.update(firstcap)
        keywords.update(extra)
        return keywords

    def resolve_keyword(self, value, source, fallback=None, extra=None):
        if extra is None:
            extra = {}
        source = self._keyword_dict(source, extra)
        return source.get(value, fallback)

    def t_INITIAL_transctrl_WHITESPACE(self, t):
        r'[\t ]+'
        # NO TOKEN

    @staticmethod
    def t_MULTILINGUAL(t):
        "\=\="
        t.lexer.push_state("text")
        return t

    @staticmethod
    def t_EQUALBRACE(t):
        "^\=\{"
        t.lexer.push_state('text')
        return t

    @staticmethod
    def t_EQUALS(t):
        "\="
        t.lexer.push_state('flagged')
        return t

    @staticmethod
    def t_INITIAL_parallel_labeled_COMMENT(t):
        r'^\#+(?![a-zA-Z]+\:)'
        # Negative lookahead to veto protocols as comments
        t.lexer.push_state('absorb')
        return t

    @staticmethod
    def t_INITIAL_parallel_labeled_DOTLINE(t):
        r'^\s*\.\s*[\n\r]'
        # A line with just a dot, occurs in brm_4_19 at the end
        t.type = "NEWLINE"
        return t

    @staticmethod
    def t_NEWLINE(t):
        r'\s*[\n\r]'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_INITIAL_parallel_labeled_ATID(self, t):
        '^\@[a-zA-Z][a-zA-Z0-9\[\]]*\+?'
        t.value = t.value[1:]
        t.lexpos += 1
        t.type = self.resolve_keyword(t.value,
                                      AtfBaseLexer.structures +
                                      AtfBaseLexer.long_argument_structures,
                                      extra={
                                          "h1": "HEADING",
                                          "h2": "HEADING",
                                          "h3": "HEADING",
                                          "label+": "LABEL",
                                          "end": "END"
                                      },
                                      )

        if t.type == "INCLUDE":
            t.lexer.push_state('nonequals')

        if t.type == "END":
            if not self.skipinvalid or t.lexer.current_state() != 'INITIAL':
                t.lexer.pop_state()
            t.lexer.push_state('transctrl')

        if t.type == "LABEL":
            t.lexer.push_state("para")
            t.lexer.push_state("transctrl")

        if t.type == "TRANSLATION":
            t.lexer.push_state("transctrl")

        if t.type == "SCORE":
            t.lexer.push_state('score')

        if t.type in AtfBaseLexer.long_argument_structures + ["NOTE"]:
            t.lexer.push_state('flagged')
        if t.type is None:
            formatstring = u"Illegal @STRING '{}'".format(t.value)
            valuestring = t.value
            if _pyversion() == 2:
                formatstring = formatstring.encode('UTF-8')
                valuestring = valuestring.encode('UTF-8')
            if self.skipinvalid:
                warnings.warn(formatstring, UserWarning)
                return
            else:
                raise SyntaxError(formatstring,
                                  (None, t.lineno, t.lexpos, valuestring))
        return t

    @staticmethod
    def t_labeled_OPENR(t):
        "\@\("
        t.lexer.push_state("para")
        t.lexer.push_state("transctrl")
        return t

    def t_INITIAL_parallel_labeled_HASHID(self, t):
        '\#[a-zA-Z][a-zA-Z0-9\[\]]+\:'
        # Note that \:? absorbs a trailing colon in protocol keywords
        t.value = t.value[1:-1]
        t.lexpos += 1
        # Use lower here since there are some ATF files with
        # the protocol incorrectly written as #NOTE:
        t.type = self.resolve_keyword(t.value.lower(),
                                      AtfBaseLexer.protocols,
                                      extra={'CHECK': 'CHECK'})
        if t.type == "KEY":
            t.lexer.push_state('nonequals')
        if t.type == "LEM":
            t.lexer.push_state('lemmatize')
        if t.type == "TR":
            t.lexer.push_state('interlinear')
        if t.type in ['PROJECT', "BIB"]:
            t.lexer.push_state('flagged')
        if t.type in ['CHECK']:
            t.lexer.push_state('absorb')
        if t.type == "NOTE":
            t.lexer.push_state('para')
        if t.type is None:
            formatstring = u"Illegal #STRING '{}'".format(t.value)
            valuestring = t.value
            if _pyversion() == 2:
                formatstring = formatstring.encode('UTF-8')
                valuestring = valuestring.encode('UTF-8')
            if self.skipinvalid:
                warnings.warn(formatstring, UserWarning)
                return
            else:
                raise SyntaxError(formatstring,
                                  (None, t.lineno, t.lexpos, valuestring))
        return t

    @staticmethod
    def t_LINELABEL(t):
        r'^[^\ \t\n]*\.'
        t.value = t.value[:-1]
        t.lexer.push_state('text')
        return t

    @staticmethod
    def t_score_SCORELABEL(t):
        r'^[^.:\ \t\#][^.:\ \t]*\:'
        t.value = t.value[:-1]
        t.lexer.push_state('text')
        return t

    def t_ID(self, t):
        u'[a-zA-Z0-9][a-zA-Z\'\u2019\xb4\/\.0-9\:\-\[\]_\u2080-\u2089]*'
        t.value = t.value.replace(u'\u2019', "'")
        t.value = t.value.replace(u'\xb4', "'")
        t.type = self.resolve_keyword(t.value,
                                      AtfBaseLexer.protocol_keywords +
                                      AtfBaseLexer.dollar_keywords +
                                      AtfBaseLexer.structures +
                                      AtfBaseLexer.long_argument_structures, 'ID',
                                      extra={
                                          'fragments': "FRAGMENT",
                                          "parallel": "PARALLEL"
                                      },
                                      )

        if t.type in ['LANG']:
            t.lexer.push_state('flagged')

        if t.type in set(AtfBaseLexer.structures +
                         AtfBaseLexer.long_argument_structures) - set(["NOTE"]):
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        return t

    @staticmethod
    def t_flagged_text_lemmatize_transctrl_nonequals_absorb_NEWLINE(t):
        r'[\n\r]*\s*[\n\r]+'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    def t_transctrl_ID(self, t):
        u'[a-zA-Z0-9][a-zA-Z\'\u2019\u2032\u02CA\xb4\/\.0-9\:\-\[\]_' \
          u'\u2080-\u2089]*'
        t.value = t.value.replace(u'\u2019', "'")
        t.value = t.value.replace(u'\u2032', "'")
        t.value = t.value.replace(u'\u02CA', "'")
        t.value = t.value.replace(u'\xb4', "'")
        t.type = self.resolve_keyword(t.value,
                                      AtfBaseLexer.protocol_keywords +
                                      AtfBaseLexer.dollar_keywords +
                                      AtfBaseLexer.structures +
                                      AtfBaseLexer.translation_keywords +
                                      AtfBaseLexer.long_argument_structures, 'ID',
                                      extra={'fragments': "FRAGMENT"}
                                      )

        if t.type == "LABELED":
            t.lexer.pop_state()
            t.lexer.push_state('labeled')
            t.lexer.push_state('transctrl')
        if t.type == "PARALLEL":
            t.lexer.pop_state()
            t.lexer.push_state('parallel')
            t.lexer.push_state('transctrl')

        if t.type in set(AtfBaseLexer.structures +
                         AtfBaseLexer.long_argument_structures) - set(["NOTE"]):
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        return t

    @staticmethod
    def t_parallel_LINELABEL(t):
        r'^([^\.\ \t]*)\.[\ \t]*'
        t.value = t.value.strip(" \t.")
        return t

    @staticmethod
    def t_parallel_labeled_DOLLAR(t):
        "^\$"
        t.lexer.push_state("absorb")
        return t

    @staticmethod
    def t_transctrl_CLOSER(t):
        "\)"
        t.lexer.pop_state()
        return t

    @staticmethod
    def t_parallel_NEWLINE(t):
        r'\s*[\n\r](?![ \t])'
        t.lexer.lineno += t.value.count("\n")
        return t

    @staticmethod
    def t_interlinear_NEWLINE(t):
        r'\s*[\n\r](?![ \t])'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    @staticmethod
    def t_labeled_NEWLINE(t):
        r'\s*[\n\r]'
        t.lexer.lineno += t.value.count("\n")
        return t

    @lex.TOKEN(translation_regex)
    def t_parallel_interlinear_ID(self, t):
        t.value = t.value.strip()
        t.value = t.value.replace("\r ", "\r")
        t.value = t.value.replace("\n ", "\n")
        t.value = t.value.replace("\n", " ")
        t.value = t.value.replace("\r", " ")
        return t

    @staticmethod
    def t_parallel_labeled_AMPERSAND(t):
        r'\&'
        # New document, so leave translation state
        t.lexer.pop_state()
        return t

    @lex.TOKEN(flagged_regex)
    def t_flagged_ID(self, t):
        # Discard leading whitespace, token is not flag or newline
        # And has at least one non-whitespace character
        t.value = t.value.strip()
        return t

    terminates_para = \
        "(\#|\@[^i][^\{]|\&|\Z|(^[0-9]+[\'\u2019\u2032\u02CA\xb4]?\.))"

    @lex.TOKEN(r'([^\^\n\r]|(\r?\n(?!\s*\r?\n)(?!' +
               terminates_para + ')))+')
    def t_para_ID(self, t):
        t.lexer.lineno += t.value.count("\n")
        t.value = t.value.strip()
        return t

    @staticmethod
    def t_para_NEWLINE(t):
        r'\r?\n\s*[\n\r]*\n'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    @lex.TOKEN(r'\r?\n(?=' + terminates_para + ')')
    def t_para_MAGICNEWLINE(self, t):
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        t.type = "NEWLINE"
        return t

    @staticmethod
    def t_nonequals_ID(t):
        "[^\=\n\r]+"
        t.value = t.value.strip()
        return t

    @staticmethod
    def t_absorb_ID(t):
        "[^\n\r]+"
        t.value = t.value.strip()
        return t

    def t_text_SPACE(self, t):
        r'[\ \t]'
        # No token generated

    def t_ANY_error(self, t):
        fstring = u"PyOracc got an illegal character '{}'".format(t.value[0])
        valuestring = t.value
        if _pyversion() == 2:
            fstring = fstring.encode('UTF-8')
            valuestring = valuestring.encode('UTF-8')
        if self.skipinvalid:
            t.lexer.skip(1)
            warnings.warn(fstring, UserWarning)
            return
        else:
            raise SyntaxError(fstring,
                              (None, t.lineno, t.lexpos, valuestring))


