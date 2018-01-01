# !/usr/bin/python

# dcpdfer.py
# version 2.0, 10/14/17
# (c) mouser@donationcoder.com

"""
pdf helper object class
"""


# -----------------------------------------------------------
#libs
import os
import io

# string template helper
import dcstrtemplate
# commandline shelling
from subprocess import check_output
# -----------------------------------------------------------



class Dcpdfer:
    """
    helper class for creating pdf files
    """
    def __init__(self, filedir, filename):
        """initialize it."""
        self.htmlout = ''
        self.setFileName(filedir,filename)


    def setFileName(self, filedir, filename):
        self.filedir = filedir
        self.filename = filename
        #
        self.fullpath = self.filedir
        if (len(self.fullpath)>0 and not self.fullpath.endswith('/') and not self.fullpath.endswith('\\')):
            self.fullpath += '/';
        self.fullpath += self.filename


    def addHtmlPagedata(self, pagehtml):
        """Add some html to the file and it should be a page break from next content."""
        # ATTN: UNFINISHED
        self.htmlout += pagehtml

    def addHtmlPagedataFromFile(self, htmlfilepath, stemplate, option_encoding):
        """Add contents of file as html."""
        if (stemplate == None):
            # open file and read contents
            #with open(htmlfilepath, 'r') as myfile:
            with io.open(htmlfilepath, 'r', encoding=option_encoding) as myfile:
                html=myfile.read()
            html = html.encode('utf-8')
        else:
            stemplate.loadFromFile(htmlfilepath, option_encoding);
            html = stemplate.retrieveText()
        # add html contents as a page
        self.addHtmlPagedata(html)

    def writeAndCloseFile(self):
        """Write out the file that we have been building, then close it."""
        # ATTN: UNFINISHED
        with open(self.fullpath + '.html', "w") as myfile:
            myfile.write(self.htmlout)



    def convertToPdf(self, commandlinetemplatefile, stemplate, option_encoding):
        """The file has already been written to self.fullpath; now try to invoke converter on it."""
        # load the command to run from a template file
        inputfilename = self.fullpath + '.html'
        outputfilename = self.fullpath + '.pdf'
        #stemplate = dcstrtemplate.DcStrTemplate()
        stemplate.loadFromFile(commandlinetemplatefile, option_encoding);
        stemplate.setField('{INPUTFILE}', inputfilename);
        stemplate.setField('{OUTPUTFILE}', outputfilename);
        commandline = stemplate.retrieveText()
        # linux / in commandline have to be changed to directory separator
        if (os.sep == "\\"):
            commandline = commandline.replace("/",os.sep)
        print 'Attempting to convert "' + inputfilename + '" to "' + outputfilename + '":'
        #print 'shelling: ' + commandline
        resultout = check_output(commandline, shell=True)
        #print resultout

