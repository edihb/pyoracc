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


from __future__ import print_function
import sys
import os
import codecs
from ..atf.atffile import AtfFile


class Corpus(object):
    def __init__(self, pattern="*.atf", **kwargs):
        self.texts = []
        self.failures = 0
        self.successes = 0
        if 'source' in kwargs:
            for dirpath, _, files in os.walk(kwargs['source']):
                for file in files:
                    if file.endswith('.atf'):
                        try:
                            path = os.path.join(dirpath, file)
                            print("Parsing file", path, "... ", end="")
                            content = codecs.open(path,
                                                  encoding='utf-8-sig',errors='ignore').read()
                            self.texts.append(AtfFile(content))

                            self.successes += 1
                            print("OK")
                        except (SyntaxError, IndexError, AttributeError,
                                UnicodeDecodeError) as e:
                            self.texts.append(None)
                            self.failures += 1
                            print("Failed with message: '{}'".format(e))


if __name__ == '__main__':
    corpus = Corpus(source=sys.argv[1])
    print()
    print("Failed with ", corpus.failures, " out of ",
          corpus.failures + corpus.successes, "(",
          corpus.failures * 100.0 / (corpus.failures + corpus.successes),
          "%)")
