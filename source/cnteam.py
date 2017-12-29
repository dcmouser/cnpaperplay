# !/usr/bin/python

# cnteam
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
    print "Hello from cnpaperplay utility, running cnteam.py " + cno.CnGame.getVersionNumber() + ' - ' + cno.CnGame.getVersionDate()

    # get commandline args

    # using argparse
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    # options
    parser.add_argument('--language', help='language name (specifies a subdirectory of the data directory where wordfile and templates will be looked for)', action="store", dest="option_language", default="english")
    parser.add_argument('--wordfile', help='filename (word list text file to user; should not include subdirectory; will be looked for in data/language and then data/ directories) (each word should be on its own line)', action="store", dest="option_wordfile", default="wordfile_default.txt")
    #parser.add_argument('--wordfile_encoding', help='iso-8859-1 by default but try utf8 for non-english', action="store", dest="option_wordfile_encoding", default="iso-8859-1")
    parser.add_argument('--patternfile', help='filename (optionally with path) of card coloring pattern data (each line is a triple specifying cardcount, player1color, player2color); just base name no subdir', action="store", dest="option_patternfile", default="patternfile_team_default.txt")
    parser.add_argument('--outpath', help='path to save output files', action="store", dest="option_outpath", default="out")
    parser.add_argument('--seedstart', type=int, help='starting seed number to use', action="store", dest="option_seedstart", default=1)
    parser.add_argument('--gamecount', type=int, help='number of games to generate', action="store", dest="option_gamecount", default=10)
    parser.add_argument('--bookname', help='base name of book output files', action="store", dest="option_bookname", default='cnteam')
    parser.add_argument('--format', help='final output format (should be html or pdf)', choices=['html', 'pdf'], action="store", dest="option_format", default='pdf')

    # parse options (this will exit here if user requests --help)
    args = parser.parse_args()
    #
    option_datadir = 'data';
    option_language = args.option_language
    option_wordfile = args.option_wordfile
    option_wordfile_encoding = cno.CnGame.fileInLangDirectoryContents(option_datadir,option_language,'encoding.txt');
    option_patternfile = args.option_patternfile
    option_outpath = args.option_outpath
    option_seedstart = int(args.option_seedstart)
    option_gamecount = int(args.option_gamecount)
    option_format = args.option_format
    option_bookname = args.option_bookname
    if (option_language != 'english'):
        option_bookname += '_' + option_language

    # base filename
    basefilename = option_bookname + '_' + str(option_seedstart) + '-' + str(option_seedstart+option_gamecount-1)

    # create the cduet game manager
    game = cno.CnGameTeam(option_wordfile, option_wordfile_encoding, option_patternfile, option_datadir, option_language)

    # templater for instructions page
    stemplate = dcstrtemplate.DcStrTemplate()
    stemplate.loadFromFile(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_intropage.html'));
    #
    stemplate.setField('{BOOKNAME}', basefilename);
    stemplate.setField('{VERSION_NUMBER}', cno.CnGame.getVersionNumber());
    stemplate.setField('{VERSION_DATE}', cno.CnGame.getVersionDate());
    stemplate.setField('{DATADIR}', option_datadir);
    stemplate.setField('{LANGUAGE}', option_language);
    stemplate.setField('{WKHTMLEXE}', 'lib/wkhtmltopdf' + cno.CnGame.getPlatformExeExtension())

    # create output pdf files and start them off
    teamcolor1 = game.getColorIndex(0);
    pdfout_player1 = dcpdfer.Dcpdfer(option_outpath, basefilename+"_leader_"+teamcolor1)
    stemplate.setField('{PLAYERBOOKID}', teamcolor1 + ' Leader');
    pdfout_player1.addHtmlPagedata(stemplate.retrieveText())
    #
    teamcolor2 = game.getColorIndex(1);
    pdfout_player2 = dcpdfer.Dcpdfer(option_outpath, basefilename+"_leader_"+teamcolor2)
    stemplate.setField('{PLAYERBOOKID}', teamcolor2 + ' Leader');
    pdfout_player2.addHtmlPagedata(stemplate.retrieveText())
    #
    pdfout_guesser = dcpdfer.Dcpdfer(option_outpath, basefilename+"_guessers")
    stemplate.setField('{PLAYERBOOKID}', 'Guessers');
    pdfout_guesser.addHtmlPagedata(stemplate.retrieveText())


    # now loop and build games
    for seed in range(option_seedstart, option_seedstart+option_gamecount):
        print " Generating game #" + str(seed)
        # generate the game (assign labels to cards, etc.)
        game.generateGame(seed)
        # render html
        html_player1 = game.render(1)
        html_player2 = game.render(2)
        html_guesser = game.render(3)
        # now add those html contents to the output pdf
        pdfout_player1.addHtmlPagedata(html_player1)
        pdfout_player2.addHtmlPagedata(html_player2)
        pdfout_guesser.addHtmlPagedata(html_guesser)

    # end pages
    pdfout_player1.addHtmlPagedataFromFile(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_endbook.html'),stemplate)
    pdfout_player2.addHtmlPagedataFromFile(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_endbook.html'),stemplate)
    pdfout_guesser.addHtmlPagedataFromFile(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_endbook.html'),stemplate)

    # write out final HTML files
    pdfout_player1.writeAndCloseFile()
    pdfout_player2.writeAndCloseFile()
    pdfout_guesser.writeAndCloseFile()

    # if they want pdf try that now
    if (option_format == 'pdf'):
        pdfout_player1.convertToPdf(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_leader_commandline_pdfconvert.txt'),stemplate)
        pdfout_player2.convertToPdf(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_leader_commandline_pdfconvert.txt'),stemplate)
        pdfout_guesser.convertToPdf(cno.CnGame.fileInLangDirectory(option_datadir,option_language,'template_team_guesser_commandline_pdfconvert.txt'),stemplate)

    # say goodbye
    print "Exiting."

# -----------------------------------------------------------



# -----------------------------------------------------------
# invoked if script is run as standalne
if __name__ == "__main__":
    main()
# -----------------------------------------------------------

