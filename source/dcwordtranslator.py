# !/usr/bin/python

# dcwordtranslator.py
# version 2.0, 1/1/18
# (c) mouser@donationcoder.com

"""
simple helper class for translating some extra words
"""

import io

class DcWordTranslator:
    """
    helper class for handling some extra simple word translations
    """

    def __init__(self):
        self.words = dict()

    def loadFromFile(self, filepath, option_encoding):
        """Load a file that has WORD = TRANSLATEDWORD pairs on each line"""
        # open file and read contents
        #with open(filepath, 'r') as myfile:
        #print "DcWordTranslator LOADING "+filepath+" USING ENCODING "+option_encoding
        with io.open(filepath, 'r', encoding=option_encoding) as myfile:
            text = myfile.read()
            #python3 7/7/23
            #text = text.encode('utf-8')
            lines = text.split("\n")

        # now split into pairs
        for line in lines:
            pattern = line.strip()
            if (pattern == '' or pattern[0]=='/' or pattern[0]=='#' or len(pattern)<2):
                continue
            # split it up at the =
            worditems = pattern.split(' = ')
            worditems = [ x.strip() for x in worditems ]
            if (len(worditems)!=2):
                # error
                raise ValueError('Syntax error in word translation file ' + filepath + '.  lines should be of the form WORD = WORDTRANSLATION. Found line was:' + pattern)
            word = worditems[0]
            translatedword = worditems[1]
            # convert to unicode
            #word = word.encode('utf-8')
            #translatedword = translatedword.encode('utf-8')
            # store it
            self.words[word] = translatedword
            #print "TRANSLATING STORED: "+word


    def translateWord(self, word):
        if (word in self.words):
            return self.words[word]
        return word

