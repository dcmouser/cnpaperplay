When you pass a language to the commandline tool (e.g. --language japanese), the program will first look inside data/language subdirectory for each of the word files and template files it uses.
Only if a language-specific file is not found in that subdirectory will it use the files here in the base data directory.

Word files can be in utf or iso-8859-1 format;  the encoding.txt file specifies what format the word files are in for any given language.  It will default to iso-8859-1.
