//---------------------------------------------------------------------------
IMPORTANT NOTE FOR LINUX USERS:

This distribution comes with prebuilt binaries of wkthmltopdf for windows and linux x64.
To run on linux you will have to chmod +x the wkhtmltopdf file in the lib directory.

If this executable does not run on your linux or other platform you will have to get or
build an alternative executable for wkhtmltopdf
//---------------------------------------------------------------------------





//---------------------------------------------------------------------------
usage: cnduet.py [-h] [--language OPTION_LANGUAGE]
                 [--wordfile OPTION_WORDFILE]
                 [--patternfile OPTION_PATTERNFILE] [--outpath OPTION_OUTPATH]
                 [--turncount OPTION_TURNCOUNT]
                 [--mistakecount OPTION_MISTAKECOUNT]
                 [--goalcount OPTION_GOALCOUNT] [--seedstart OPTION_SEEDSTART]
                 [--gamecount OPTION_GAMECOUNT] [--bookname OPTION_BOOKNAME]
                 [--format {html,pdf}]

optional arguments:
  -h, --help            show this help message and exit
  --language OPTION_LANGUAGE
                        language name (specifies a subdirectory of the data
                        directory where wordfile and templates will be looked
                        for)
  --wordfile OPTION_WORDFILE
                        filename (word list text file to user; should not
                        include subdirectory; will be looked for in
                        data/language and then data/ directories) (each word
                        should be on its own line)
  --patternfile OPTION_PATTERNFILE
                        filename (optionally with path) of card coloring
                        pattern data (each line is a triple specifying
                        cardcount, player1color, player2color); just base name
                        no subdir
  --outpath OPTION_OUTPATH
                        path to save output files
  --turncount OPTION_TURNCOUNT
                        number of turns per game
  --mistakecount OPTION_MISTAKECOUNT
                        number of mistakes allowed per game
  --goalcount OPTION_GOALCOUNT
                        number of goals needed to win game)
  --seedstart OPTION_SEEDSTART
                        starting seed number to use
  --gamecount OPTION_GAMECOUNT
                        number of games to generate
  --bookname OPTION_BOOKNAME
                        base name of book output files
  --format {html,pdf}   final output format (should be html or pdf)

E:\MyDocs\Programming\Python\cnpaperplay\source>

//---------------------------------------------------------------------------




//---------------------------------------------------------------------------
usage: cnteam.py [-h] [--language OPTION_LANGUAGE]
                 [--wordfile OPTION_WORDFILE]
                 [--patternfile OPTION_PATTERNFILE] [--outpath OPTION_OUTPATH]
                 [--seedstart OPTION_SEEDSTART] [--gamecount OPTION_GAMECOUNT]
                 [--bookname OPTION_BOOKNAME] [--format {html,pdf}]

optional arguments:
  -h, --help            show this help message and exit
  --language OPTION_LANGUAGE
                        language name (specifies a subdirectory of the data
                        directory where wordfile and templates will be looked
                        for)
  --wordfile OPTION_WORDFILE
                        filename (word list text file to user; should not
                        include subdirectory; will be looked for in
                        data/language and then data/ directories) (each word
                        should be on its own line)
  --patternfile OPTION_PATTERNFILE
                        filename (optionally with path) of card coloring
                        pattern data (each line is a triple specifying
                        cardcount, player1color, player2color); just base name
                        no subdir
  --outpath OPTION_OUTPATH
                        path to save output files
  --seedstart OPTION_SEEDSTART
                        starting seed number to use
  --gamecount OPTION_GAMECOUNT
                        number of games to generate
  --bookname OPTION_BOOKNAME
                        base name of book output files
  --format {html,pdf}   final output format (should be html or pdf)
//---------------------------------------------------------------------------
