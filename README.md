# subtitle2textConverter

Command line application that converts subtitle formats (.srt and .vtt) to text files after parse and removing timestamps and html tags if present.
Allows single file conversion and conversion of all subtitle files in a folder/directory.

Usage:


    sub2text.py [-h] fileLocation [-d DEST] 

    Convert a single subtitle file OR Enter a folder path to convert all subtitles
    in it

    positional arguments:
    fileLocation          Complete FileDirectory/Folder or a single filename,(Enclose it inside
                          quotations " ")

    optional arguments:
    -h, --help            show this help message and exit
    -d DEST, --dest DEST  File location for output files (Enclose it inside
                          quotations " ")
