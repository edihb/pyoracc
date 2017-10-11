"""
This file serves as common token lexicon for usage.
"""


class AtfLexicon(object):

    T_EQUALS = "\="
    T_PARBAR = "\|\|"
    T_COMMA = "\,"
    T_TO = "\>\>"
    T_FROM = "\<\<"
    T_MINUS = "\-"
    T_DOLLAR = "\$"
    T_STAR = "\*"
    T_QUERY = "\?"
    T_EXCLAIM = "\!"
    T_HASH = "\#"
    T_AMPERSAND = "\&"

    STRUCTURES = ['TABLET', 'ENVELOPE', 'PRISM', 'BULLA', 'OBVERSE', 'REVERSE', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM',
                  'CATCHLINE', 'COLOPHON', 'DATE', 'SIGNATURES', 'SIGNATURE', 'SUMMARY', 'FACE', 'EDGE', 'COLUMN',
                  'SEAL', 'SEALINGS', 'WITNESSES', 'TRANSLATION', 'NOTE', 'M', 'COMPOSITE', 'LABEL', 'INCLUDE', 'SCORE']
    LONG_ARGUMENT_STRUCTURES = ['OBJECT', 'SURFACE', 'FRAGMENT', 'HEADING']
    PROTOCOLS = ['ATF', 'LEM', 'PROJECT', 'NOTE', "LINK", "KEY", "BIB", "TR", 'CHECK', 'LEMMATIZER', 'VERSION', 'VAR']
    PROTOCOL_KEYWORDS = ['LANG', 'USE', 'MATH', 'LEGACY', 'MYLINES', 'LEXICAL', 'UNICODE', 'DEF', "SOURCE"]
    DOLLAR_KEYWORDS = ['MOST', 'LEAST', 'ABOUT', 'SEVERAL', 'SOME', 'REST', 'OF', 'START', 'BEGINNING', 'MIDDLE',
                       'END', 'COLUMNS', 'LINE', 'LINES', 'CASE', 'CASES', 'SURFACE', 'SPACE', 'BLANK', 'BROKEN',
                       'EFFACED', 'ILLEGIBLE', 'MISSING', 'TRACES', 'RULING', 'SINGLE', 'DOUBLE', 'TRIPLE', 'AT']
    TRANSLATION_KEYWORDS = ['PARALLEL', 'PROJECT', "LABELED"]

    KEYWORD_TOKENS = sorted(list(set(
        STRUCTURES + LONG_ARGUMENT_STRUCTURES + PROTOCOLS + PROTOCOL_KEYWORDS + DOLLAR_KEYWORDS + TRANSLATION_KEYWORDS)))
    BASE_TOKENS = ['AMPERSAND', 'LINELABEL', 'SCORELABEL', 'ID', 'DOLLAR', 'PARENTHETICALID', 'HAT', 'SEMICOLON',
                   'EQUALS',
                   'MULTILINGUAL', 'LSQUARE', 'RSQUARE', 'EXCLAIM', 'QUERY', 'STAR', 'RANGE', 'HASH', 'NEWLINE',
                   'REFERENCE', 'MINUS', 'FROM', 'TO', 'PARBAR', 'OPENR', 'CLOSER', 'COMMA', 'COMMENT', 'EQUALBRACE']
    TOKENS = sorted(list(set(KEYWORD_TOKENS + BASE_TOKENS)))

    INCLUSIVE_STATE_NAMES = ['score']
    EXCLUSIVE_STATE_NAMES = [
        'flagged',
        'text',
        'lemmatize',
        'nonequals',
        'parallel',  # translation
        'labeled',  # translation
        'interlinear',  # translation
        'transctrl',
        'para',
        'absorb'
    ]
    INC_STATES = [(state, 'inclusive') for state in INCLUSIVE_STATE_NAMES]
    EXC_STATES = [(state, 'exclusive') for state in EXCLUSIVE_STATE_NAMES]
    STATES = EXC_STATES + INC_STATES
