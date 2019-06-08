#! python3
# Subtitle to text convertor
# Converts popular subtitle file extensions .srt and .vtt to .txt format.
# Allows a single file conversion
# and allows multiple file conversion by selection of a folder

import glob, sys, re, os
from argparse import ArgumentParser


def parse_args():
    """
    Parse command line arguments and format arguments containing paths.
    :return: tuple of (ArgumentParser, Namespace). Parser itself and all arguments.
    """
    parser = ArgumentParser(description='Convert a single subtitle file OR '
                                        'Enter a folder path to convert all subtitles in it ')
    parser.add_argument('-s','--file', help='Complete Filepath and filename',type=str)
    parser.add_argument('-f','--folder',help='Folder/Directory/ Location of subtitle files', type=str)
    args = parser.parse_args()
    if isinstance(args.file, str):
        args.file = os.path.normpath(args.file.strip())
    if isinstance(args.folder, str):
        args.folder = os.path.normpath(args.folder.strip())
    return parser, args

def check_for_errors(filename, folder):
    """
    Check for errors, return corresponding
    error statement if any errors occurred.
    Otherwise return None.
    :param filename: str. Subtitle file path.
    :param folder: str. Folder path containing subtitles.
    :return: str or NoneType. Error statement or None.
    """
    if filename != None and folder != None:
        if not os.path.exists(filename) or not os.path.exists(folder):
            message = f'Error: path does not exist.'
        elif filename[-4:] != '.srt' or filename[-4:] != '.vtt':
            message = f'Error: The subtitle extension must be either .srt or .vtt.'
    elif filename == None and folder == None:
        message = 'Error: You must provide either filepathname or folder path.'
    else:
        message = None
    return message

def create_newFile(oriname,exten):
    """
    Creates file of another type with same name.
    Gets the source name, parses it and return the string (output name same as the source name) with .txt extension.
    :param oriname: str. Filename
    :param exten: str. Output extension.
    :return: str. Same Filename with new file extension
    """
    na = re.sub(r"\[.*?\]",'',oriname)
    na1 = na.rstrip()
    namm = na1[:len(na1)-4] + exten
    return namm

def parse_clean_text(te):
    """
    Parses and cleans the text extracted from the subtitle file.
    The subtitle file contains timestamps or html tags so this removes them to make the text readable.

    :param te: str, Text extracted from subtitle
    :return: str, new text
    """

    re1 = r'<.*?>'
    re2 = r'[0-9]+\n.+:.+:.+,.+-->.+:.+:.+,.+'
    re3 = r'.+:.+:.+\..+'
    re4 = 'WEBVTT'

    re_list = [re1, re2, re3, re4]
    generic_re = re.compile( '|'.join( re_list) )
    newText = re.sub(generic_re,'',te)
    newT = ' '.join(newText.split())
    return newT

def read_convert_singleFile(filename):
    """
    Reads a single subtitle file, extracts text from it, cleans it and then converts it into new text file.
    :param filename: str, File path and filename
    :return: None
    """
    te = open(filename)
    text = te.read().strip()
    nammm = create_newFile(filename,'.txt')
    with open(nammm, 'w') as t1:
        newText = parse_clean_text(text)
        t1.write(newText)

def convert_folder(folder):
    """
    Gets a list of files with required subtitle extension(srt and vtt) and performs read_convert_singleFile on each file.
    :param folder: str, Folder/location containing the subtitle files
    :return: None
    """
    files = []
    for ext in ('*.srt', '*.vtt'):
        files.extend(glob.glob(os.path.join(folder, ext)))
    for f in files:
        read_convert_singleFile(f)

if __name__ == '__main__':
    parser, args = parse_args()
    filename = args.file
    folder = args.folder
    # checking for errors
    error = check_for_errors(filename,folder)
    if error:
        sys.exit(error)
    if filename != None:
        read_convert_singleFile(filename)
    elif folder != None:
        convert_folder(folder)
    print("Conversion Completed!!")


