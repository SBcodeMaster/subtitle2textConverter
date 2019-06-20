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
    parser.add_argument('fileLocation', help='Complete FileDirectory or filename,(Enclose it inside quotations " ")',type=str)
    parser.add_argument('-d','--dest',help='File location for output files (Enclose it inside quotations " ")',type=str)
    args = parser.parse_args()
    if isinstance(args.fileLocation, str):
        args.fileLocation = os.path.normpath(args.fileLocation.strip())
    return parser, args

def check_for_errors(filesource):
    """
    Check for errors, return corresponding
    error statement if any errors occurred.
    Otherwise return None.
    :param filename: str. Subtitle file path.
    :param folder: str. Folder path containing subtitles.
    :return: str or NoneType. Error statement or None.
    """
    message = None
    if filesource != None:
        if not os.path.exists(filesource):
            message = 'Error: path does not exist.'
        if os.path.isfile(filesource) and not (filesource[-4:] == '.srt' or filesource[-4:] == '.vtt'):
            message = f'Error: The subtitle extension must be either .srt or .vtt.'
    elif filesource is None:
        message = 'Error: You must provide either filepathname or folder path.'
    else:
        message = None
    return message

def create_newFile(location,oriname,exten):
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
    if not location is False:
        namm = os.path.join(os.path.abspath(location),os.path.basename(namm))
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
    generic_re = re.compile('|'.join(re_list))
    newText = re.sub(generic_re,'',te)
    newT = ' '.join(newText.split())
    return newT

def read_convert_singleFile(filename,location):
    """
    Reads a single subtitle file, extracts text from it, cleans it and then converts it into new text file.
    :param filename: str, File path and filename
    :return: None
    """
    te = open(filename)
    text = te.read().strip()
    nammm = create_newFile(location,filename,'.txt')

    with open(nammm, 'w') as t1:
        newText = parse_clean_text(text)
        t1.write(newText)

def convert_folder(folder,location):
    """
    Gets a list of files with required subtitle extension(srt and vtt) and performs read_convert_singleFile on each file.
    :param folder: str, Folder/location containing the subtitle files
    :return: None
    """
    files = []
    for ext in ('*.srt', '*.vtt'):
        files.extend(glob.glob(os.path.join(folder, ext)))
    for f in files:
        read_convert_singleFile(f,location)



def select_destination(args):
    """
    Check if the destination path is in the command line arguments,
    if not destination path will be source path
    If the destination path in arguments does not exist create it.
    :param args: Namespace. Command line arguments.
    :return: str. Destination folder path.
    """
    if args.dest is None:
        destination = None
    else:
        destination = args.dest
        if not os.path.exists(destination):
            os.makedirs(destination)
    return destination

if __name__ == '__main__':
    parser, args = parse_args()
    src = args.fileLocation
    to_folder = select_destination(args)
    # checking for errors
    error = check_for_errors(src)
    if error:
        sys.exit(error)
    if os.path.isfile(src):
        read_convert_singleFile(src,to_folder)
    elif os.path.isdir(src):
        convert_folder(src,to_folder)
    print("Conversion Completed!!")


