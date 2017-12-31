# !/usr/bin/python

# cduet
# version 2.0, 10/14/17
# (c) mouser@donationcoder.com

"""
Commandline Use:
  -h, --help            show this help message and exit
"""

# -----------------------------------------------------------
# cduet objects
import cno
# pdf helpers
import dcpdfer
# string template helper
import dcstrtemplate

# for argument parsing:
import argparse
# -----------------------------------------------------------








# -----------------------------------------------------------
# invoked if script is run as standalne
def main():
    """Main function"""

    # say hello
    print "Hello from cnpaperplay utility, running cnduet.py " + cno.CnGame.getVersionNumber() + ' - ' + cno.CnGame.getVersionDate()

    # get commandline args

    # using argparse
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    # options
    parser.add_argument('--wordfile', help='filename (optionally with path) of worsd list text file to read (each word should be on its own line)', action="store", dest="option_wordfile", default="data/wordfile_default.txt")
    parser.add_argument('--wordfile_encoding', help='iso-8859-1 by default', action="store", dest="option_wordfile_encoding", default="iso-8859-1")
    parser.add_argument('--patternfile', help='filename (optionally with path) of card coloring pattern data (each line is a triple specifying cardcount, player1color, player2color)', action="store", dest="option_patternfile", default="data/patternfile_duet_default.txt")
    parser.add_argument('--outpath', help='path to save output files', action="store", dest="option_outpath", default="out")
    parser.add_argument('--turncount', type=int, help='number of turns per game', action="store", dest="option_turncount", default=9)
    parser.add_argument('--mistakecount', type=int, help='number of mistakes allowed per game', action="store", dest="option_mistakecount", default=5)
    parser.add_argument('--goalcount', type=int, help='number of goals needed to win game)', action="store", dest="option_goalcount", default=15)
    parser.add_argument('--seedstart', type=int, help='starting seed number to use', action="store", dest="option_seedstart", default=1)
    parser.add_argument('--gamecount', type=int, help='number of games to generate', action="store", dest="option_gamecount", default=10)
    parser.add_argument('--bookname', help='base name of book output files', action="store", dest="option_bookname", default='cnduet')
    parser.add_argument('--format', help='final output format (should be html or pdf)', choices=['html', 'pdf'], action="store", dest="option_format", default='pdf')
    parser.add_argument('--templatedir', help='directory where template files are', action="store", dest="option_templatedir", default = 'templates')

    # parse options (this will exit here if user requests --help)
    args = parser.parse_args()
    #
    option_wordfile = args.option_wordfile
    option_wordfile_encoding = args.option_wordfile_encoding
    option_patternfile = args.option_patternfile
    option_outpath = args.option_outpath
    option_turncount = int(args.option_turncount)
    option_mistakecount = int(args.option_mistakecount)
    option_goalcount = int(args.option_goalcount)
    option_seedstart = int(args.option_seedstart)
    option_gamecount = int(args.option_gamecount)
    option_bookname = args.option_bookname
    option_format = args.option_format
    option_templatedir = args.option_templatedir

    # base filename
    basefilename = option_bookname + '_' + str(option_seedstart) + '-' + str(option_seedstart+option_gamecount-1)

    # create the cduet game manager
    game = cno.CnGameDuet(option_wordfile, option_wordfile_encoding, option_patternfile, option_templatedir, option_turncount, option_mistakecount, option_goalcount)

    # templater for instructions page
    stemplate = dcstrtemplate.DcStrTemplate()
    stemplate.loadFromFile(cno.CnGame.fileInDirectory(option_templatedir,'template_duet_intropage.html'));
    #
    stemplate.setField('{BOOKNAME}', basefilename);
    stemplate.setField('{VERSION_NUMBER}', cno.CnGame.getVersionNumber());
    stemplate.setField('{VERSION_DATE}', cno.CnGame.getVersionDate());
    stemplate.setField('{TEMPLATEDIR}', option_templatedir);
    stemplate.setField('{ABSTEMPLATEDIR}', cno.CnGame.absPath(option_templatedir));

    # create output pdf files and start them off
    pdfout_player1 = dcpdfer.Dcpdfer(option_outpath, basefilename+"_p1")
    stemplate.setField('{PLAYERID}', '1 of 2');
    pdfout_player1.addHtmlPagedata(stemplate.retrieveText())
    #
    pdfout_player2 = dcpdfer.Dcpdfer(option_outpath, basefilename+"_p2")
    stemplate.setField('{PLAYERID}', '2 of 2');
    pdfout_player2.addHtmlPagedata(stemplate.retrieveText())


    # now loop and build games
    for seed in range(option_seedstart, option_seedstart+option_gamecount):
        print " Generating game #" + str(seed)
        # generate the game (assign labels to cards, etc.)
        game.generateGame(seed)
        # render html
        html_player1 = game.render(1)
        html_player2 = game.render(2)
        # now add those html contents to the output pdf
        pdfout_player1.addHtmlPagedata(html_player1)
        pdfout_player2.addHtmlPagedata(html_player2)

    # end pages
    pdfout_player1.addHtmlPagedataFromFile(cno.CnGame.fileInDirectory(option_templatedir,'template_duet_endbook.html'), stemplate)
    pdfout_player2.addHtmlPagedataFromFile(cno.CnGame.fileInDirectory(option_templatedir,'template_duet_endbook.html'), stemplate)

    # write out final HTML files
    pdfout_player1.writeAndCloseFile()
    pdfout_player2.writeAndCloseFile()

    # if they want pdf try that now
    if (option_format == 'pdf'):
        pdfout_player1.convertToPdf(cno.CnGame.fileInDirectory(option_templatedir,'template_duet_commandline_pdfconvert.txt'))
        pdfout_player2.convertToPdf(cno.CnGame.fileInDirectory(option_templatedir,'template_duet_commandline_pdfconvert.txt'))

    # say goodbye
    print "Exiting."

# -----------------------------------------------------------



# -----------------------------------------------------------
# invoked if script is run as standalne
if __name__ == "__main__":
    main()
# -----------------------------------------------------------

