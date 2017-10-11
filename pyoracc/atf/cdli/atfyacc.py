from pyoracc.atf.common.atfyacc import AtfBaseParser


class AtfCDLIParser(AtfBaseParser):
    def __init__(self, tabmodule='pyoracc.atf.parsetab'):
        super(AtfCDLIParser, self).__init__(tabmodule)