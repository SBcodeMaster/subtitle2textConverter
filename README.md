# subtitle2textConverter

Command line application that converts subtitle formats (.srt and .vtt) to text files after parse and removing timestamps and html tags if present.
Allows single file conversion and conversion of all subtitle files in a folder/directory.

Usage:


    sub2text.py [-h] [-s FILE] [-f FOLDER]

    Convert a single subtitle file OR Enter a folder path to convert all subtitles in it

    optional arguments:

    -h, --help                  show this help message and exit  
    -s FILE, --file FILE        Complete Filepath and filename  
    -f FOLDER, --folder FOLDER   Folder/Directory/ Location of subtitle files
