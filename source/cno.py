# !/usr/bin/python

# cduet
# version 3.0, 10/14/17
# (c) mouser@donationcoder.com

"""
cduet helper object class
"""


# -----------------------------------------------------------
# libraries uses
import random
import os
import io
import platform

# string template helper
import dcstrtemplate
# -----------------------------------------------------------



















class CnCard:
    """
    Cduet card class
    """

    def __init__(self, word, colors):
        self.word = word
        self.colors = colors

    def getColor(self, playerid):
        return self.colors[playerid-1]

    def getWord(self):
        return self.word

    def createCopy(self, word):
        """Create a copy of this card with the new word; used for templates."""
        card = CnCard(word, list(self.colors))
        return card


    def matchesColorForPlayer(self, colorname, playerid):
        if (colorname.upper() == self.colors[playerid-1].upper()):
            return True
        return False

    def replaceColor(self, colorindex, ifcolor, newcolor):
        """Function to replace a color if found with a new one, used in team game for the starting team card."""
        if (self.colors[colorindex]==ifcolor):
            self.colors[colorindex]=newcolor























class CnGame:
    """
    CnGame game class
    """

    @staticmethod
    def getVersionNumber(): return 'v3.0'
    @staticmethod
    def getVersionDate(): return 'Dec 30, 2017'
    @staticmethod
    def fileInDirectory(dirpart, filepart):
        """Helper to make full filepath"""
        return dirpart + "/" + filepart
    @staticmethod
    def fileInLangDirectory(dirpart, lang, filepart):
        """Helper to make full filepath
        Search first for dirpart/lang/filepart
        and if not found fall back to dirpart/filepart
        """
        fpath = dirpart + "/" + lang + "/" + filepart
        if (not os.path.isfile(fpath)):
            fpath = dirpart + "/" + filepart
        if (not os.path.isfile(fpath)):
            raise ValueError('Could not find file in language subdirectory (' +  dirpart + '/' + lang + filepart + ') or in main directory: ' + fpath)
            #raise IOError(ENOENT, 'Could not find file in language subdirectory or in main directory', fpath)
        return fpath

    @staticmethod
    def fileInLangDirectoryContents(dirpart, lang, filepart):
        """Helper to load file contents and return as string."""
        filepath = CnGame.fileInLangDirectory(dirpart, lang, filepart)
        # open file and read contents
        with open(filepath, 'r') as myfile:
            contents=myfile.read()
        contents = contents.strip();
        return contents

    @staticmethod
    def absPath(filepath):
        """Make filepath an absolute path if it isn't already."""
        if (filepath[0]=='/' or ":" in filepath):
            return filepath
        if (len(filepath)>=2):
            if (filepath[0:2]=="./" or filepath[0:2]==".\\"):
                filepath = filepath[2:]
        return os.path.dirname(os.path.realpath(__file__)) + "/" + filepath

    @staticmethod
    def getPlatformExeExtension():
        if (platform.system()=='Linux'):
            return ''
        else:
            return '.exe'

    def __init__(self, option_wordfile, option_wordfile_encoding, option_patternfile, option_datadir, option_language):
        # data dir and language
        self.option_datadir = option_datadir;
        self.option_language = option_language
        # load word file
        self.option_wordfile = self.fileInLangDirectory(self.option_datadir, self.option_language, option_wordfile)
        self.option_wordfile_encoding = option_wordfile_encoding
        self.loadWordFile()
        # load pattern file
        self.option_patternfile = self.fileInLangDirectory(self.option_datadir, self.option_language,option_patternfile)
        self.loadPatternFile()


    def getColorIndex(self, colorindex):
        return self.colorlist[colorindex]


    def calcGameId(self):
        """String defining the game -- mainly its the seed."""
        return str(self.seed);


    def loadFileAsString(self, filename):
        """Helper to load file into string."""
        # open file and read contents
        with open(filename, 'r') as myfile:
            txt=myfile.read()
        return txt.strip()



    def setSeedAndRandomize(self, seed):
        self.seed = seed
        random.seed(self.seed)


    def loadWordFile(self):
        """Load the wordfile into memory."""
        self.wordlist = list()
        # read file as a list of lines
        # with io.open(self.option_wordfile, 'r', encoding='utf-8') as myfile:
        with io.open(self.option_wordfile, 'r', encoding=self.option_wordfile_encoding) as myfile:
        #with open(self.option_wordfile, 'r') as myfile:
            wordlist=myfile.readlines()
            # now lets walk them and strip and remove any blank or starting with / and uppercase, etc
            for word in wordlist:
                #word = word.encode('utf-8', 'ignore')
                #word = word.decode('iso-8859-1').encode('utf8')
                word = word.strip().upper()
                word = word.encode('utf-8')
                word = word.strip().upper()
                if (len(word)==0 or word[0]=='/' or word[0]=='#'):
                    continue
                self.wordlist.append(word)
            #print self.wordlist




    def loadPatternFile(self):
        """Load the pattern file triples."""
        # total cards in a game is based on the patterns
        self.cardtemplates = list()
        # read file as a list of lines
        with open(self.option_patternfile, 'r') as myfile:
            patternlist=myfile.readlines()
            # loop rest of pattern lines
            patternindex = 0
            for pattern in patternlist:
                pattern = pattern.strip()
                if (pattern == '' or pattern[0]=='/' or pattern[0]=='#'):
                    continue
                linelist = pattern.split(',')
                linelist = [ x.strip() for x in linelist ]
                if (patternindex == 0):
                    # first line is list of colors (colorlist)
                    self.colorlist = linelist
                else:
                    # parse the pattern line
                    # we now support arbitrary number player color assignments
                    #if (len(linelist)!=3):
                    #    raise ValueError('Pattern file contains a pattern that is not a comma separated triplet: ' + pattern)
                    # first number is the # of cards with this color pattern
                    cardcount = int(linelist[0])
                    colorassignments = linelist[1:]
                    # create a number of template cards based on cardcount, so we will have 1 cardtemplate for every physical card that would be in game
                    for i in range(1, cardcount+1):
                        # create blank card for this labeling
                        card = CnCard('', colorassignments)
                        # and add it to our template list
                        self.cardtemplates.append(card)
                patternindex += 1


    def getColorCountString(self, playerid):
        """Build a nice simple list of how many of each color there are."""
        # init
        colorcounts = dict()
        for colorname in self.colorlist:
            colorcounts[colorname.upper()] = 0
        # now walk cards and count colors
        for card in self.gamecards:
            colorname = card.getColor(playerid)
            colorcounts[colorname.upper()] += 1
        # ok now built the report string
        hretv = ''
        for colorname in self.colorlist:
            if (hretv!=''):
                hretv += ' | '
            hretv += str(colorcounts[colorname.upper()]) + ' ' + colorname
        return hretv





    def renderTrackBoxes(self, boxcount):
        """Render some unicode checkboxes."""
        hretv = '<cspan class="cdboxes">'
        xcount = 0
        xspacer = 3
        for i in range(0,boxcount):
            hretv += '&#10066;'
            xcount += 1
            if (xcount == xspacer):
                hretv += ' '
                xcount = 0
        hretv += '</span>'
        return hretv






    def renderAllWordList(self):
        """Ok the upper list is just the entire list of words formatted into a grid."""
        # sorted list of gamewords
        gamewords = sorted(list(self.gamewords))
        # generic table formatter
        hretv = ''
        hretv += '<table class="cdwordlist cdwordlist_upper" width="100%">' + "\n"
        hretv += self.renderTableRows(gamewords, 5, '', True)
        hretv += "</table>\n"
        return hretv



    def renderColorGroupedWordList(self, playerid):
        """Lower list is 3 sections organized by color, and the gridding is more complicated"""
        hretv = ''
        colcount = 3;

        hretv += '<table class="cdwordlist cdwordlist_lower" width="100%">' + "\n"
        index = 0
        for colorname in self.colorlist:
            # get list of words of this color
            wordlist = sorted(list(self.findWordsMatchingColorForPlayer(colorname, playerid)))
            if (len(wordlist)==0):
                # kludge for an empty wordlist
                wordlist = [ " " ]
            if (index>0):
                # spacer line
                hretv += '  <tr> <td colspan="' + str(colcount+1) + '">&nbsp;</td> </tr>' + "\n"
            hretv += self.renderTableRows(wordlist, colcount, colorname, True)
            index +=1

        hretv += "</table>\n"
        return hretv




    def findWordsMatchingColorForPlayer(self, colorname, playerid):
        """Walk through all labeled cards, find any which match this color for this player."""
        wordlist = list()
        for card in self.gamecards:
            if (card.matchesColorForPlayer(colorname, playerid)):
                wordlist.append(card.getWord())
        return wordlist





    def renderTableRows(self, wordlist, colcount, headerlabel, flag_centerlast):
        """make table rows."""
        hretv = ''
        xcount = 0
        ycount = 0
        wordindex = 0
        wordcount = len(wordlist)
        for word in wordlist:
            if (xcount==colcount):
                hretv += "  </tr>\n"
                xcount = 0
                ycount += 1
            if (xcount == 0):
                hretv += "  <tr> "
                # header column
                if (headerlabel != ''):
                    hretv += '<td align="left"><b>'
                    if (ycount==0):
                        hretv += headerlabel
                    else:
                        hretv += '&nbsp;'
                    hretv += '</b></td> '
            if (flag_centerlast and xcount == 0 and wordindex == wordcount-1 and colcount%2==1):
                # last word, its also first word of row, we have option to center it
                while xcount < colcount/2:
                    hretv += '<td>&nbsp;</td>';
                    xcount += 1
                hretv += '<td align="center">' + word + '</td> '
                #hretv += '<td colspan="' + str(colcount-xcount) + '" align="center">' + word + '</td> '
                #xcount = colcount-1
            else:
                hretv += '<td align="center">' + word + '</td> '
            wordindex += 1
            xcount += 1
        if (wordcount>0):
            while xcount < colcount:
                hretv += '<td>&nbsp;</td>';
                xcount += 1
            hretv += " </tr>\n"
        return hretv






    def generateGame(self, seed):
        """Create the game by picking random words and assigning labels to cards, etc."""

        # randomize with seed
        self.setSeedAndRandomize(seed)

        # pick all the words we need for the game
        gamecardcount = len(self.cardtemplates)
        self.gamewords = random.sample(self.wordlist, gamecardcount)

        # now walk through the pattern card templates and instantiate game cards
        self.gamecards = list()
        index = 0
        for templatecard in self.cardtemplates:
            gamecard = templatecard.createCopy(self.gamewords[index])
            self.gamecards.append(gamecard)
            index += 1
        # it's just that simple!



































class CnGameDuet(CnGame):
    """
    CnGameDuet for duet game class
    """

    def __init__(self, option_wordfile, option_wordfile_encoding, option_patternfile, option_datadir, option_language, option_turncount, option_mistakecount, option_goalcount):
        """Initialize the game manager with files to use, etc."""
        #
        # base class init
        CnGame.__init__(self, option_wordfile, option_wordfile_encoding, option_patternfile, option_datadir, option_language)
        #
        self.option_turncount = option_turncount
        self.option_mistakecount = option_mistakecount
        self.option_goalcount = option_goalcount
        #
        # load template for game html, we will use this when outputting
        self.gamepageStemplate = dcstrtemplate.DcStrTemplate()
        self.gamepageStemplate.loadFromFile(CnGame.fileInLangDirectory(self.option_datadir, self.option_language,'template_duet_gamepage.html'));




    def generateGame(self, seed):
        """Create the game by picking random words and assigning labels to cards, etc."""
        # just call base parent function to generate game
        CnGame.generateGame(self,seed)



    def render(self, playerid):
        """Render the html for the current game, from the standpoint of player #playerid."""

        # we use a template system; we have already loaded template self.gamepageStemplate

        # now we need to fill in fields to replace in rendering
        self.gamepageStemplate.setField('{GAMEID}', self.calcGameId())
        self.gamepageStemplate.setField('{PLAYERID}', str(playerid) + " of 2")

        self.gamepageStemplate.setField('{TURNCOUNT}', str(self.option_turncount))
        self.gamepageStemplate.setField('{MISTAKECOUNT}', str(self.option_mistakecount))
        self.gamepageStemplate.setField('{GOALCOUNT}', str(self.option_goalcount))

        self.gamepageStemplate.setField('{TURNTRACK}', self.renderTrackBoxes(self.option_turncount))
        self.gamepageStemplate.setField('{MISTAKETRACK}', self.renderTrackBoxes(self.option_mistakecount))
        self.gamepageStemplate.setField('{GOALTRACK}', self.renderTrackBoxes(self.option_goalcount))

        self.gamepageStemplate.setField('{UPPERLIST}', self.renderAllWordList())
        self.gamepageStemplate.setField('{LOWERLIST}', self.renderColorGroupedWordList(playerid))

        # now render it replacing fields above
        hretv = self.gamepageStemplate.retrieveText()

        return hretv








































class CnGameTeam(CnGame):
    """
    CnGameTeam for team game class
    """

    def __init__(self, option_wordfile, option_wordfile_encoding, option_patternfile, option_datadir, option_language):
        """Initialize the game manager with files to use, etc."""
        CnGame.__init__(self, option_wordfile, option_wordfile_encoding, option_patternfile, option_datadir, option_language)
        # load template for game html, we will use this when outputting
        self.leaderPageStemplate = dcstrtemplate.DcStrTemplate()
        self.leaderPageStemplate.loadFromFile(CnGame.fileInLangDirectory(self.option_datadir, self.option_language,'template_team_leaderpage.html'));
        self.guesserPageStemplate = dcstrtemplate.DcStrTemplate()
        self.guesserPageStemplate.loadFromFile(CnGame.fileInLangDirectory(self.option_datadir, self.option_language,'template_team_guesserpage.html'));


    def generateGame(self, seed):
        """Create the game by picking random words and assigning labels to cards, etc."""
        # just call base parent function to generate game
        CnGame.generateGame(self,seed)
        # determine starting player (team)
        self.startingPlayer = seed % 2
        # now replace {STARTINGPLAYERCOLOR} for in card color with game's starting player
        colorlabel_startingplayer = self.getColorIndex(self.startingPlayer)
        for card in self.gamecards:
            card.replaceColor(0, '{STARTINGPLAYERCOLOR}', colorlabel_startingplayer)






    def render(self, playerid):
        if (playerid==1 or playerid==2):
            # determine players color and other stuff
            colorindex_player = playerid-1
            colorindex_opponent = (1-colorindex_player);
            colorlabel_player = self.getColorIndex(colorindex_player)
            colorlabel_startingplayer = self.getColorIndex(self.startingPlayer)
            self.leaderPageStemplate.setField('{GAMEID}', self.calcGameId())
            self.leaderPageStemplate.setField('{PLAYERID}', colorlabel_player + " Leader")
            self.leaderPageStemplate.setField('{STARTINGPLAYERCOLOR}', colorlabel_startingplayer)
            # now render word tables
            coloredwordtable = self.renderTeamColorGroupedWordList(playerid)
            self.leaderPageStemplate.setField('{COLOREDWORDTABLE}', coloredwordtable)
            # now render it replacing fields above
            hretv = self.leaderPageStemplate.retrieveText()
        elif (playerid==3):
            # game id and other stuff
            self.guesserPageStemplate.setField('{GAMEID}', self.calcGameId())
            self.guesserPageStemplate.setField('{COLORCOUNTS}', self.getColorCountString(0))
            # render all words
            allwordtable = self.renderAllWordList()
            self.guesserPageStemplate.setField('{ALLWORDTABLE}', allwordtable)
            # now render it replacing fields above
            hretv = self.guesserPageStemplate.retrieveText()
        else:
            raise ValueError('Playerid in CnGameTeam render should be from [1,2,3]: ' + playerid)
        #
        return hretv






    def renderTeamColorGroupedWordList(self, playerid):
        """Team color list is like duet color list but order is different and labeling is different"""
        hretv = ''
        colcount = 3;
        flag_adjustfirst = False

        hretv += '<table class="cdwordlist cdwordlist_lower" width="100%">' + "\n"
        index = 0
        colorcount = len(self.colorlist)
        for i in range(0, colorcount):
            if (i==0):
                # first always display current player teams color
                colorname = self.colorlist[playerid-1]
                if (flag_adjustfirst):
                    colcount = 2
            elif (i==1):
                # next display opponent color
                colorname = self.colorlist[2-playerid]
                if (flag_adjustfirst):
                    colcount = 3
            else:
                # other colors in order given in colorlist
                colorname = self.colorlist[i]
                if (flag_adjustfirst):
                    colcount = 3
            # get list of words of this color
            wordlist = sorted(list(self.findWordsMatchingColorForPlayer(colorname, 1)))
            if (len(wordlist)==0):
                # kludge for an empty wordlist
                wordlist = [ " " ]
            if (index>0):
                # spacer line
                hretv += '  <tr> <td colspan="' + str(colcount+1) + '">&nbsp;</td> </tr>' + "\n"
            hretv += self.renderTableRows(wordlist, colcount, colorname, False)
            if (flag_adjustfirst and index==0):
                # dif # of columns means it needs a dif table
                hretv += "</table>\n"
                hretv += '<table class="cdwordlist cdwordlist_lower" width="100%">' + "\n"
            index +=1


        hretv += "</table>\n"
        return hretv