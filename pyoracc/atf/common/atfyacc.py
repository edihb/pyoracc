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


import ply.yacc as yacc
from pyoracc import _pyversion
from pyoracc.atf.common.atflexicon import AtfLexicon

from pyoracc.model.comment import Comment
from pyoracc.model.composite import Composite
from pyoracc.model.line import Line
from pyoracc.model.link import Link
from pyoracc.model.link_reference import LinkReference
from pyoracc.model.milestone import Milestone
from pyoracc.model.multilingual import Multilingual
from pyoracc.model.note import Note
from pyoracc.model.oraccnamedobject import OraccNamedObject
from pyoracc.model.oraccobject import OraccObject
from pyoracc.model.ruling import Ruling
from pyoracc.model.score import Score
from pyoracc.model.state import State
from pyoracc.model.text import Text
from pyoracc.model.translation import Translation


class AtfParser(object):
    tokens = AtfLexicon.TOKENS

    def __init__(self, tabmodule='pyoracc.atf.parsetab'):
        self.parser = yacc.yacc(module=self, tabmodule=tabmodule)

    @staticmethod
    def p_document(p):
        """document : text
                    | object
                    | composite"""
        p[0] = p[1]

    @staticmethod
    def p_codeline(p):
        "text_statement : AMPERSAND ID EQUALS ID newline"
        p[0] = Text()
        p[0].code = p[2]
        p[0].description = p[4]

    @staticmethod
    def p_project_statement(p):
        "project_statement : PROJECT ID newline"
        p[0] = p[2]

    @staticmethod
    def p_project(p):
        "project : project_statement"
        p[0] = p[1]

    @staticmethod
    def p_text_project(p):
        "text : text project"
        p[0] = p[1]
        p[0].project = p[2]

    @staticmethod
    def p_code(p):
        "text : text_statement"
        p[0] = p[1]

    def p_unicode(self, p):
        """skipped_protocol : ATF USE UNICODE newline
                            | ATF USE MATH newline
                            | ATF USE LEGACY newline
                            | ATF USE MYLINES newline
                            | ATF USE LEXICAL newline
                            | key_statement
                            | BIB ID newline
                            | BIB ID EQUALS ID newline
                            | lemmatizer_statement"""

    def p_key_statement(self, p):
        """key_statement : key newline
                         | key EQUALS newline"""

    def p_key(self, p):
        "key : KEY ID"

    def p_key_addendum(self, p):
        "key : key EQUALS ID"

    def p_lemmatizer(self, p):
        "lemmatizer : LEMMATIZER"

    def p_lemmatizer_id(self, p):
        "lemmatizer : lemmatizer ID"

    def p_lemmatizer_statement(self, p):
        "lemmatizer_statement : lemmatizer newline "

    @staticmethod
    def p_link(p):
        "link : LINK DEF ID EQUALS ID EQUALS ID newline"
        p[0] = Link(p[3], p[5], p[7])

    @staticmethod
    def p_link_source(p):
        "link : LINK SOURCE ID EQUALS ID newline"
        # Not documented but fairly common ca 600
        # texts in the full corpus
        p[0] = Link(code=p[3], description=p[5])

    @staticmethod
    def p_link_parallel(p):
        "link : LINK PARALLEL ID EQUALS ID newline"
        p[0] = Link(None, p[3], p[5])

    @staticmethod
    def p_include(p):
        "link : INCLUDE ID EQUALS ID newline"
        p[0] = Link("Include", p[2], p[4])

    @staticmethod
    def p_language_protoocol(p):
        "language_protocol : ATF LANG ID newline"
        p[0] = p[3]

    @staticmethod
    def p_text_math(p):
        "text : text skipped_protocol"
        p[0] = p[1]

    @staticmethod
    def p_text_link(p):
        "text : text link"
        p[0] = p[1]
        p[0].links.append(p[2])

    @staticmethod
    def p_text_language(p):
        "text : text language_protocol"
        p[0] = p[1]
        p[0].language = p[2]

    @staticmethod
    def p_text_object(p):
        """text : text object %prec OBJECT"""
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_text_surface(p):
        """text : text surface %prec OBJECT
                | text translation %prec TRANSLATIONEND"""
        p[0] = p[1]
        # Find the last object in the text
        # If there is none, append a tablet and use that
        # Default to a tablet

        # Has a default already been added?
        if not p[0].objects():
            p[0].children.append(OraccObject("tablet"))
        p[0].objects()[-1].children.append(p[2])

    @staticmethod
    def p_text_surface_element(p):
        """text : text surface_element %prec OBJECT"""
        p[0] = p[1]
        if not p[0].objects():
            p[0].children.append(OraccObject("tablet"))
        # Default to obverse of a tablet
        p[0].objects()[-1].children.append(OraccObject("obverse"))
        p[0].objects()[-1].children[0].children.append(p[2])

    @staticmethod
    def p_text_composite(p):
        """text : text COMPOSITE newline"""
        p[0] = p[1]
        p[0].composite = True

    @staticmethod
    def p_text_text(p):
        """composite : text text"""
        # Text must be a composite
        p[0] = Composite()
        if not p[1].composite:
            # An implicit composite
            pass
        p[0].texts.append(p[1])
        p[0].texts.append(p[2])

    @staticmethod
    def p_composite_text(p):
        """composite : composite text"""
        # Text must be a composite
        p[0] = p[1]
        p[0].texts.append(p[2])

    @staticmethod
    def p_object_statement(p):
        """object_statement : object_specifier newline"""
        p[0] = p[1]

    @staticmethod
    def p_flag(p):
        """ flag : HASH
                 | EXCLAIM
                 | QUERY
                 | STAR """
        p[0] = p[1]

    @staticmethod
    def p_object_flag(p):
        "object_specifier : object_specifier flag"
        p[0] = p[1]
        AtfParser.flag(p[0], p[2])

    @staticmethod
    def flag(target, flag):
        if flag == "#":
            target.broken = True
        elif flag == "!":
            target.remarkable = True
        elif flag == "?":
            target.query = True
        elif flag == "*":
            target.collated = True

    # These MUST be kept as a separate parse rule,
    # as the same keywords also occur
    # in strict dollar lines
    @staticmethod
    def p_object_nolabel(p):
        '''object_specifier : TABLET
                            | ENVELOPE
                            | PRISM
                            | BULLA
                            | SEALINGS'''
        p[0] = OraccObject(p[1])

    @staticmethod
    def p_object_label(p):
        '''object_specifier : FRAGMENT ID
                            | OBJECT ID
                            | TABLET REFERENCE'''
        p[0] = OraccNamedObject(p[1], p[2])

    @staticmethod
    def p_object(p):
        "object : object_statement"
        p[0] = p[1]

    @staticmethod
    def p_object_surface(p):
        """object : object surface %prec SURFACE
              | object translation %prec TRANSLATIONEND """
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_object_surface_element(p):
        """object : object surface_element %prec SURFACE"""
        p[0] = p[1]
        # Default surface is obverse
        p[0].children.append(OraccObject("obverse"))
        p[0].children[0].children.append(p[2])

    @staticmethod
    def p_surface_statement(p):
        "surface_statement : surface_specifier newline"
        p[0] = p[1]

    @staticmethod
    def p_surface_flag(p):
        "surface_specifier : surface_specifier flag"
        p[0] = p[1]
        AtfParser.flag(p[0], p[2])

    @staticmethod
    def p_surface_nolabel(p):
        '''surface_specifier  : OBVERSE
                              | REVERSE
                              | LEFT
                              | RIGHT
                              | TOP
                              | BOTTOM'''
        p[0] = OraccObject(p[1])

    @staticmethod
    def p_surface_label(p):
        '''surface_specifier : FACE ID
                             | SURFACE ID
                             | COLUMN ID
                             | SEAL ID
                             | HEADING ID'''
        p[0] = OraccNamedObject(p[1], p[2])

    @staticmethod
    def p_surface(p):
        "surface : surface_statement"
        p[0] = p[1]

    @staticmethod
    def p_surface_element_line(p):
        """surface_element : line %prec LINE
                           | dollar
                           | note_statement
                           | link_reference_statement %prec LINE
                           | milestone"""
        p[0] = p[1]

    @staticmethod
    def p_dollar(p):
        """dollar          : ruling_statement
                           | loose_dollar_statement
                           | strict_dollar_statement
                           | simple_dollar_statement"""
        p[0] = p[1]

    @staticmethod
    def p_surface_line(p):
        """surface : surface surface_element"""
        p[0] = p[1]
        p[0].children.append(p[2])
        # WE DO NOT YET HANDLE @M=DIVSION lines.

    @staticmethod
    def p_linelabel(p):
        "line_sequence : LINELABEL ID"
        p[0] = Line(p[1])
        p[0].words.append(p[2])

    @staticmethod
    def p_scorelabel(p):
        "line_sequence : SCORELABEL ID"
        p[0] = Line(p[1])
        p[0].words.append(p[2])

    @staticmethod
    def p_line_id(p):
        "line_sequence : line_sequence ID"
        p[0] = p[1]
        p[0].words.append(p[2])

    @staticmethod
    def p_line_reference(p):
        "line_sequence : line_sequence reference"
        p[0] = p[1]
        p[0].references.append(p[2])

    @staticmethod
    def p_line_statement(p):
        "line_statement : line_sequence newline"
        p[0] = p[1]

    @staticmethod
    def p_line(p):
        "line : line_statement"
        p[0] = p[1]

    @staticmethod
    def p_line_lemmas(p):
        "line : line lemma_statement  "
        p[0] = p[1]
        p[0].lemmas = p[2]

    @staticmethod
    def p_line_note(p):
        "line : line note_statement"
        p[0] = p[1]
        p[0].notes.append(p[2])

    @staticmethod
    def p_line_interlinear_translation(p):
        "line : line interlinear"
        p[0] = p[1]
        p[0].translation = p[2]

    @staticmethod
    def p_interlinear(p):
        "interlinear : TR ID newline"
        p[0] = p[2]

    @staticmethod
    def p_interlinear_empty(p):
        "interlinear : TR newline"
        p[0] = ""

    @staticmethod
    def p_line_link(p):
        "line : line link_reference_statement"
        p[0] = p[1]
        p[0].links.append(p[2])

    @staticmethod
    def p_line_equalbrace(p):
        "line : line equalbrace_statement"
        p[0] = p[1]
        # Don't know what to do here

    def p_equalbrace(self, p):
        "equalbrace : EQUALBRACE"

    def p_equalbrace_ID(self, p):
        "equalbrace : equalbrace ID"

    def p_equalbrace_statement(self, p):
        "equalbrace_statement : equalbrace newline"

    @staticmethod
    def p_line_multilingual(p):
        "line : line multilingual %prec MULTI"
        p[0] = Multilingual()
        p[0].lines[None] = p[1]
        p[0].lines[p[2].label] = p[2]
        # Use the language, temporarily stored in the label, as the key.
        p[0].lines[p[2].label].label = p[1].label
        # The actual label is the same as the main line

    @staticmethod
    def p_multilingual_sequence(p):
        "multilingual_sequence : MULTILINGUAL ID "
        p[0] = Line(p[2][1:])  # Slice off the percent

    @staticmethod
    def p_multilingual_id(p):
        "multilingual_sequence : multilingual_sequence ID"
        p[0] = p[1]
        p[0].words.append(p[2])

    @staticmethod
    def p_multilingual_reference(p):
        "multilingual_sequence : multilingual_sequence reference"
        p[0] = p[1]
        p[0].references.append(p[2])

    @staticmethod
    def p_multilingual_statement(p):
        "multilingual_statement : multilingual_sequence newline"
        p[0] = p[1]

    @staticmethod
    def p_multilingual(p):
        "multilingual : multilingual_statement"
        p[0] = p[1]

    @staticmethod
    def p_multilingual_lemmas(p):
        "multilingual : multilingual lemma_statement "
        p[0] = p[1]
        p[0].lemmas = p[2]

    @staticmethod
    def p_multilingual_note(p):
        "multilingual : multilingual note_statement "
        p[0] = p[1]
        p[0].notes.append(p[2])

    @staticmethod
    def p_multilingual_link(p):
        "multilingual : multilingual link_reference_statement "
        p[0] = p[1]
        p[0].links.append(p[2])

    @staticmethod
    def p_lemma_list(p):
        "lemma_list : LEM ID"
        p[0] = [p[2]]

    @staticmethod
    def p_milestone(p):
        "milestone : milestone_name newline"
        p[0] = p[1]

    @staticmethod
    def p_milestone_name(p):
        "milestone_name : M EQUALS ID"
        p[0] = Milestone(p[3])

    @staticmethod
    def p_milestone_brief(p):
        """milestone_name : CATCHLINE
                          | COLOPHON
                          | DATE
                          | EDGE
                          | SIGNATURES
                          | SIGNATURE
                          | SUMMARY
                          | WITNESSES"""
        p[0] = Milestone(p[1])

    @staticmethod
    def p_lemma_list_lemma(p):
        "lemma_list : lemma_list lemma"
        p[0] = p[1]
        p[0].append(p[2])

    def p_lemma(self, p):
        "lemma : SEMICOLON"

    @staticmethod
    def p_lemma_id(p):
        "lemma : lemma ID"
        p[0] = p[2]

    @staticmethod
    def p_lemma_statement(p):
        "lemma_statement : lemma_list newline"
        p[0] = p[1]

    @staticmethod
    def p_ruling_statement(p):
        "ruling_statement : ruling newline"
        p[0] = p[1]

    @staticmethod
    def p_ruling(p):
        """ruling : DOLLAR SINGLE RULING
                  | DOLLAR DOUBLE RULING
                  | DOLLAR TRIPLE RULING
                  | DOLLAR SINGLE LINE RULING
                  | DOLLAR DOUBLE LINE RULING
                  | DOLLAR TRIPLE LINE RULING"""

        counts = {
            'single': 1,
            'double': 2,
            'triple': 3,
        }
        p[0] = Ruling(counts[p[2]])

    @staticmethod
    def p_uncounted_ruling(p):
        "ruling : DOLLAR RULING"
        p[0] = Ruling(1)

    @staticmethod
    def p_flagged_ruling(p):
        "ruling : ruling flag"
        p[0] = p[1]
        AtfParser.flag(p[0], p[2])

    @staticmethod
    def p_note(p):
        """note_statement : note_sequence newline"""
        p[0] = p[1]

    @staticmethod
    def p_note_sequence(p):
        """note_sequence : NOTE """
        p[0] = Note()

    @staticmethod
    def p_note_sequence_content(p):
        """note_sequence : note_sequence ID"""
        p[0] = p[1]
        p[0].content += p[2]

    @staticmethod
    def p_note_sequence_link(p):
        """note_sequence : note_sequence reference"""
        p[0] = p[1]
        p[0].references.append(p[2])

    @staticmethod
    def p_reference(p):
        "reference : HAT ID HAT"
        p[0] = p[2]

    def p_newline(self, p):
        """newline : NEWLINE
                   | newline NEWLINE"""

    @staticmethod
    def p_loose_dollar(p):
        "loose_dollar_statement : DOLLAR PARENTHETICALID newline"
        p[0] = State(loose=p[2])

    @staticmethod
    def p_strict_dollar_statement(p):
        "strict_dollar_statement : DOLLAR state_description newline"
        p[0] = p[2]

    @staticmethod
    def p_state_description(p):
        """state_description : plural_state_description
                             | singular_state_desc
                             | brief_state_desc"""
        p[0] = p[1]

    @staticmethod
    def p_simple_dollar(p):
        """simple_dollar_statement : DOLLAR ID newline
                                   | DOLLAR state newline"""
        p[0] = State(p[2])

    @staticmethod
    def p_plural_state_description(p):
        """plural_state_description : plural_quantifier plural_scope state
                                    | ID plural_scope state
                                    | ID singular_scope state
                                    | ID REFERENCE state"""
        # The singular case is an exception: "1 line broken" is semantically
        # the same as "2 lines broken"
        p[0] = State(p[3], p[2], p[1])

    @staticmethod
    def p_plural_state_description_unquantified(p):
        """plural_state_description : plural_scope state
        """
        # This should probably not be allowed but is happening in the corpus
        # i.e. ""$ columns broken"
        p[0] = State(p[2], p[1])

    @staticmethod
    def p_plural_state_description_unquantified_reverse(p):
        """plural_state_description : state plural_scope
        """
        # This should probably not be allowed but is happening in the corpus
        # i.e. ""$ blank lines"
        p[0] = State(p[1], p[2])

    @staticmethod
    def p_plural_state_range_description(p):
        """plural_state_description : ID MINUS ID plural_scope state"""
        p[0] = State(p[5], p[4], p[1] + "-" + p[3])

    @staticmethod
    def p_qualified_state_description(p):
        "plural_state_description : qualification plural_state_description"
        p[0] = p[2]
        p[0].qualification = p[1]

    @staticmethod
    def p_singular_state_desc(p):
        """singular_state_desc : singular_scope state
                               | REFERENCE state
                               | REFERENCE ID state"""
        text = list(p)
        p[0] = State(text[-1], " ".join(text[1:-1]))

    # This is reversed compared to the documentation but fairly common so
    # We have to implement it. I.e. cams/gkab/00atf/ctn_4_032.atf and others
    # http://oracc.museum.upenn.edu/doc/help/editinginatf/primer/structuretutorial/index.html
    # section $-lines
    @staticmethod
    def p_state_singular_desc(p):
        """singular_state_desc : state singular_scope"""
        text = list(p)
        p[0] = State(state=text[1], scope=" ".join(text[2:]))

    @staticmethod
    def p_singular_state_desc_brief(p):
        """brief_state_desc : brief_quantifier state"""
        text = list(p)
        p[0] = State(text[-1], None, text[1])

    @staticmethod
    def p_partial_state_description(p):
        """singular_state_desc : partial_quantifier singular_state_desc"""
        p[0] = p[2]
        p[0].extent = p[1]

    @staticmethod
    def p_state(p):
        """state : BLANK
                 | BROKEN
                 | EFFACED
                 | ILLEGIBLE
                 | MISSING
                 | TRACES"""
        p[0] = p[1]

    def p_plural_quantifier(self, p):
        """plural_quantifier : SEVERAL
                             | SOME"""

    @staticmethod
    def p_singular_scope(p):
        """singular_scope : LINE
                          | CASE
                          | SPACE"""
        p[0] = p[1]

    @staticmethod
    def p_plural_scope(p):
        """plural_scope : COLUMNS
                        | LINES
                        | CASES"""
        p[0] = p[1]

    @staticmethod
    def p_brief_quantifier(p):
        """brief_quantifier : REST
                            | START
                            | BEGINNING
                            | MIDDLE
                            | END"""
        p[0] = p[1]

    @staticmethod
    def p_partial_quantifier(p):
        """partial_quantifier : brief_quantifier OF"""
        p[0] = " ".join(p[1:])

    @staticmethod
    def p_qualification(p):
        """qualification : AT LEAST
                         | AT MOST
                         | ABOUT"""
        p[0] = " ".join(p[1:])

    @staticmethod
    def p_translation_statement(p):
        """translation_statement : TRANSLATION PARALLEL ID PROJECT newline
                                 | TRANSLATION LABELED ID PROJECT newline
        """
        p[0] = Translation()

    @staticmethod
    def p_translation(p):
        "translation : translation_statement"
        p[0] = p[1]

    @staticmethod
    def p_translation_end(p):
        "translation : translation END REFERENCE newline"
        p[0] = p[1]
        # Nothing to do; this is a legacy ATF feature

    @staticmethod
    def p_translation_surface(p):
        "translation : translation surface %prec SURFACE"
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_translation_labeledline(p):
        "translation : translation translationlabeledline %prec LINE"
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_translation_dollar(p):
        "translation : translation dollar"
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_translationlabelledline(p):
        """translationlabeledline : translationlabel NEWLINE
                                  | translationrangelabel NEWLINE
                                  | translationlabel CLOSER
                                  | translationrangelabel CLOSER
        """
        p[0] = Line(p[1])

    @staticmethod
    def p_translationlabel(p):
        """translationlabel : LABEL
                            | OPENR"""
        p[0] = LinkReference("||", None)
        if p[1][-1] == "+":
            p[0].plus = True

    @staticmethod
    def p_translationlabel_id(p):
        """translationlabel : translationlabel ID
                            | translationlabel REFERENCE"""
        p[0] = p[1]
        p[0].label.append(p[2])

    @staticmethod
    def p_translationrangelabel(p):
        "translationrangelabel : translationlabel MINUS"
        p[0] = p[1]

    @staticmethod
    def p_translationrangelabel_id(p):
        """translationrangelabel : translationrangelabel ID
                                 | translationrangelabel REFERENCE"""
        p[0] = p[1]
        p[0].rangelabel.append(p[2])

    @staticmethod
    def p_translationlabeledline_reference(p):
        """translationlabeledline : translationlabeledline reference
                                  | translationlabeledline reference newline"""
        p[0] = p[1]
        p[0].references.append(p[2])

    @staticmethod
    def p_translationlabeledline_note(p):
        "translationlabeledline : translationlabeledline note_statement"
        p[0] = p[1]
        p[0].notes.append(p[2])

    @staticmethod
    def p_translationlabelledline_content(p):
        """translationlabeledline : translationlabeledline ID
                                  | translationlabeledline ID newline"""
        p[0] = p[1]
        p[0].words.append(p[2])

    @staticmethod
    def p_linkreference(p):
        "link_reference : link_operator ID"
        p[0] = LinkReference(p[1], p[2])

    @staticmethod
    def p_linkreference_label(p):
        """link_reference : link_reference ID
                          | link_reference COMMA ID"""
        p[0] = p[1]
        p[0].label.append(list(p)[-1])

    @staticmethod
    def p_link_range_reference_label(p):
        """link_range_reference : link_range_reference ID
                                | link_range_reference COMMA ID"""
        p[0] = p[1]
        p[0].rangelabel.append(list(p)[-1])

    @staticmethod
    def p_link_range_reference(p):
        """link_range_reference : link_reference MINUS"""
        p[0] = p[1]

    @staticmethod
    def p_linkreference_statement(p):
        """link_reference_statement : link_reference newline
                                    | link_range_reference newline
        """
        p[0] = p[1]

    @staticmethod
    def p_link_operator(p):
        """link_operator : PARBAR
                         | TO
                         | FROM """
        p[0] = p[1]

    @staticmethod
    def p_comment(p):
        "comment : COMMENT ID NEWLINE"
        p[0] = Comment(p[2])

    @staticmethod
    def p_check(p):
        "comment : CHECK ID NEWLINE"
        p[0] = Comment(p[2])
        p[0].check = True

    @staticmethod
    def p_surface_comment(p):
        "surface : surface comment %prec LINE"
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_translationline_comment(p):
        "translationlabeledline : translationlabeledline comment"
        p[0] = p[1]
        p[0].notes.append(p[2])

    @staticmethod
    def p_translation_comment(p):
        "translation : translation comment %prec LINE"
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_text_comment(p):
        "text : text comment %prec SURFACE"
        p[0] = p[1]
        p[0].children.append(p[2])

    @staticmethod
    def p_line_comment(p):
        "line : line comment"
        p[0] = p[1]
        p[0].notes.append(p[2])

    @staticmethod
    def p_multilingual_comment(p):
        "multilingual : multilingual comment"
        p[0] = p[1]
        p[0].notes.append(p[2])

    @staticmethod
    def p_score(p):
        "score : SCORE ID ID NEWLINE"
        p[0] = Score(p[2], p[3])

    @staticmethod
    def p_score_word(p):
        "score : SCORE ID ID ID NEWLINE"
        p[0] = Score(p[2], p[3], True)

    @staticmethod
    def p_text_score(p):
        "text : text score"
        p[0] = p[1]
        p[0].score = p[2]

    # There is a potential shift-reduce conflict in the following sample:
    """
      @tablet
      @obverse
      @translation
      @obverse
    """
    # where (object(surface,translation(surface))) could be read as
    # object(surface,translation(),surface)
    # These need to be resolved by making surface establishment and composition
    # take precedence over the completion of a translation

    # A number of conflicts are also introduced by the default rules:

    # A text can directly contain a line (implying obverse of a tablet) etc.
    #

    precedence = (
        # LOW precedence
        ('nonassoc', 'TRANSLATIONEND'),
        ('nonassoc', 'TABLET', 'ENVELOPE', 'PRISM', 'BULLA', 'SEALINGS',
            'FRAGMENT', 'OBJECT', 'MULTI'),
        ('nonassoc', 'OBVERSE', 'REVERSE', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM',
            'FACE',
            'SURFACE', 'EDGE', 'COLUMN', 'SEAL', 'HEADING', 'LINE'),
        ('nonassoc', "LINELABEL", "DOLLAR", "LEM", "NOTE", 'COMMENT',
            'CATCHLINE', 'CHECK',
            'COLOPHON', 'DATE', 'SIGNATURES',
            'SIGNATURE', 'SUMMARY',
            'WITNESSES', "PARBAR", "TO", "FROM"),
        # HIGH precedence
    )

    @staticmethod
    def p_error(p):
        formatstring = u"PyOracc could not parse token '{}'.".format(p)
        valuestring = p.value
        if _pyversion() == 2:
            formatstring = formatstring.encode('UTF-8')
            valuestring = valuestring.encode('UTF-8')
        raise SyntaxError(formatstring,
                          (None, p.lineno, p.lexpos, valuestring))
        # All errors currently unrecoverable
        # So just throw
        # Add list of params so PyORACC users can build their own error msgs.
