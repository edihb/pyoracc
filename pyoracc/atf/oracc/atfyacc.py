from pyoracc.atf.common.atfyacc import AtfBaseParser


class AtfOraccParser(AtfBaseParser):
    def __init__(self, tabmodule='pyoracc.atf.parsetab'):
        super(AtfOraccParser, self).__init__(tabmodule)

    # These MUST be kept as a separate parse rule,
    # as the same keywords also occur
    # in strict dollar lines

    # This is reversed compared to the documentation but fairly common so
    # We have to implement it. I.e. cams/gkab/00atf/ctn_4_032.atf and others
    # http://oracc.museum.upenn.edu/doc/help/editinginatf/primer/structuretutorial/index.html
    # section $-lines

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