import re

from ply import lex as lex

from pyoracc.atf.common.atfbaselex import AtfBaseLexer


class AtfOraccLexer(AtfBaseLexer):

    # In the base state, a newline doesn't change state

    # In the flagged, text, transctrl and lemmatize states,
    # one or more newlines returns to the base state
    # In several of the files such as bb_2_006.atf the blank line contains tab
    # or other trailing whitespace

    # --- RULES FOR THE TRANSLATION STATES ---
    # In this state, the base state is free text
    # And certain tokens deviate from that, rather
    # than the other way round as for base state

    # Unicode 2019 is right single quotation
    # Unicode 02cCA is MODIFIER LETTER ACUTE ACCENT
    # Unicode 2032  is PRIME
    # All of these could be used as prime

    # In parallel states, a newline doesn't change state
    # A newline followed by a space gives continuation

    # In interlinear states, a newline which is not continuation leaves state
    # A newline followed by a space gives continuation

    # In labeled translation, a newline doesn't change state
    # A newline just passed through

    # Flag characters (#! etc ) don't apply in translations
    # But reference anchors ^1^ etc do.
    # lines beginning with a space are continuations
    # translation_regex1 and translation_regex2 are identical appart from the
    # fact that the first character may not be a ?
    # We are looking for a string that does not start with ? it may include
    # newlines if they are followed by a whitespace.

    # This next rule should be unnecessary, as
    # paragraphs absorb multiple lines anyway
    # But because some malformed texts terminate translation blocks
    # with the next label, not a double-newline, fake labels, lines
    # which look like
    # labels, can cause apparent terminations of blocks
    # So we add this rule to accommodate these
    # --- RULES FOR THE ABSORB STATE ---
    # Used for states where only flag# characters! and ^1^ references
    # Are separately tokenised

    # --- Rules for paragaph state----------------------------------
    # Free text, ended by double new line

    # Paragraph state is ended by a double newline

    # BUT, exceptionally to fix existing bugs in active members of corpus,
    # it is also ended by an @label or an @(), or a new document,
    # Or a linelabel, or the end of the stream. Importantly it does not end
    # by @i{xxx} which is used for un translated words.
    # and these tokens are not absorbed by this token
    # Translation paragraph state is ended by a double newline

    # --- RULES FOR THE nonequals STATE -----
    # Absorb everything except an equals

    # --- RULES FOR THE absorb STATE -----
    # Absorb everything

    # --- RULES FOR THE text STATE ----

    # --- RULES FOR THE lemmatize STATE

    # Error handling rule

    def __init__(self, skipinvalid=False, debug=0):
        super(AtfOraccLexer, self).__init__(skipinvalid)
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)