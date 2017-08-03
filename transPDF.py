# for finding files
import glob
# for running poppler
import subprocess
import os
# for getting paths
from os import path
# for regexing stuff
import re
# For Cleaning up the .tmp folder
import shutil
# For better memory when gathering answers
import mmap
# Logging!
import logging
# For putting files in tmp
from shutil import copyfile, copytree
# To get the file name
from os import path, makedirs
# Searching Directories
import glob
# Pausing for files to set in
import time
# For setting the window type
import ctypes
# File chooser
from tkinter import filedialog
import tkinter
# Get OS
import platform

# Default to linux setup, but this will be overriden later on:
CONST_POPPLER_LIB = "/usr/bin/"
CONST_EXECUTABLE_EXTENSION = ""


logging.basicConfig(filename='transPDF.log', filemode='w',level=logging.DEBUG, format='[%(levelname)s] %(message)s')
def reglob(path, exp, invert=False):
    """glob.glob() style searching which uses regex

    :param exp: Regex expression for filename
    :param invert: Invert match to non matching files
    """

    m = re.compile(exp)

    if invert is False:
        res = [f for f in os.listdir(path) if m.search(f)]
    else:
        res = [f for f in os.listdir(path) if not m.search(f)]

    res = map(lambda x: "%s/%s" % (path, x, ), res)
    return res

def setupcli():
    # Makes things look spiffy for the end user.
    os.system("mode con cols=150 lines=30")
    print(r"__/\\\\\\\\\\\\\\\__________________________________________________________/\\\\\\\\\\\\\____/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\_        ".center(149, " "))
    print(r" _\///////\\\/////__________________________________________________________\/\\\/////////\\\_\/\\\////////\\\__\/\\\///////////__       ".center(149, " "))
    print(r"  _______\/\\\_______________________________________________________________\/\\\_______\/\\\_\/\\\______\//\\\_\/\\\_____________      ".center(149, " "))
    print(r"   _______\/\\\________/\\/\\\\\\\___/\\\\\\\\\_____/\\/\\\\\\____/\\\\\\\\\\_\/\\\\\\\\\\\\\/__\/\\\_______\/\\\_\/\\\\\\\\\\\_____     ".center(149, " "))
    print(r"    _______\/\\\_______\/\\\/////\\\_\////////\\\___\/\\\////\\\__\/\\\//////__\/\\\/////////____\/\\\_______\/\\\_\/\\\///////______    ".center(149, " "))
    print(r"     _______\/\\\_______\/\\\___\///____/\\\\\\\\\\__\/\\\__\//\\\_\/\\\\\\\\\\_\/\\\_____________\/\\\_______\/\\\_\/\\\_____________   ".center(149, " "))
    print(r"      _______\/\\\_______\/\\\__________/\\\/////\\\__\/\\\___\/\\\_\////////\\\_\/\\\_____________\/\\\_______/\\\__\/\\\_____________  ".center(149, " "))
    print(r"       _______\/\\\_______\/\\\_________\//\\\\\\\\/\\_\/\\\___\/\\\__/\\\\\\\\\\_\/\\\_____________\/\\\\\\\\\\\\/___\/\\\_____________ ".center(149, " "))
    print(r"        _______\///________\///___________\////////\//__\///____\///__\//////////__\///______________\////////////_____\///______________".center(149, " "))
    print(r" ".center(149, " "))
    print(r"A program by /u/HexaCubist".center(149, " "))
    print(r" ".center(149, " "))
    print(r" ".center(149, " "))

def searchfiles(loc='./.tmp/', extension='.pdf'):
    # search for files
    files = glob.glob(loc + '*' + extension)
    # detect if there are any files, then output list of files
    if not files == []:
        print("[INFO] Files found\n")
        logging.info("Files found\n")
        return files
    else:
        input("[SEVERE] No files found")
        return "Error code 01: Files not found"

# Tool for removing files in a directory
def remdir(loc):
    files = glob.glob(loc)
    for f in files:
        os.remove(f)


# Delete all temp files
def cleanup():
    shutil.rmtree(".tmp/", ignore_errors=True)


def convhtml(pdf):
    # convert each file to html
    print("[INFO] Converting to html")
    logging.info("Converting to html")
    for file in pdf:
        execloc = path.relpath(CONST_POPPLER_LIB + "pdftohtml" + CONST_EXECUTABLE_EXTENSION)
        startloc = path.relpath(file)
        endloc = path.relpath(".tmp/html/" + file[7:])
        with open(os.devnull, "w") as f:
            subprocess.call([execloc, "-noframes", "-c", "-s", "-i",
                             startloc, endloc], stdout=f)
    # Get files just generated
    html_docs = glob.glob('./.tmp/html/*.html')
    logging.debug(html_docs)
    return html_docs


def genPDF(pdf, startpg, endpg, outname=""):
    # convert each file to html
    print("[INFO] Making new PDFs")
    logging.info("Making new PDFs")
    for file in pdf:
        if outname == "":
            outname = pdf
        execloc = path.relpath(CONST_POPPLER_LIB + "pdftocairo" + CONST_EXECUTABLE_EXTENSION)
        startloc = path.relpath(".tmp/" + file)
        endloc = path.relpath(".tmp/output/" + outname)
        command = [execloc, "-pdf", "-f", str(startpg), "-l", str(endpg), startloc, endloc]
        print(command)
        with open(os.devnull, "w") as f:
            # subprocess.call([execloc, "-pdf", "-f " + str(startpg), "-l " + str(endpg),
                             # startloc, endloc], stdout=f)
            subprocess.call(command, stdout=f)
    # Get files just generated
    pdf_outputs = glob.glob('./.tmp/output/*.pdf')
    logging.debug(pdf_outputs)
    return pdf_outputs



# -------------------------------------------------
# 
# Proccess begins here!
# 
# -------------------------------------------------

# First, let's initialize our command line:
setupcli()

# Check if we're on linux or windows:
if(platform.system() == "Windows"):
    # And set the title using windows DLL:
    ctypes.windll.kernel32.SetConsoleTitleA(b"TransPDF")
    # Set path constants
    CONST_POPPLER_LIB = "libs/poppler/bin/"
    CONST_EXECUTABLE_EXTENSION = ".exe"
else:
    # Probably linux or something! Let's hope the person used our install.sh or installed poppler-utils themselves.
    CONST_POPPLER_LIB = ""
    CONST_EXECUTABLE_EXTENSION = ""

# Get list of files
input("We are now going to ask for the files you wish to convert. Press ENTER to continue")
root = tkinter.Tk()
root.withdraw()
importfiles = filedialog.askopenfilenames(filetypes=[("pdf files", "*.pdf")])

# Where do we want to store when done?
input("When completed, where do you want to store the resulting split PDFs?. Press ENTER to continue")
saveloc = filedialog.askdirectory(mustexist=True)

# Make temp folders
def makedirif(dir):
    tmpdir = path.relpath(dir)

    if not path.exists(tmpdir):
        makedirs(tmpdir)

makedirif(".tmp/")
makedirif(".tmp/html/")
makedirif(".tmp/output/")

# Move files to TMP folder
for file in importfiles:
    finallocation = path.relpath(".tmp/" + path.basename(file))
    copyfile(file, finallocation)

# Search for copied files
files = searchfiles()

# Convert copied files into HTML for searching
html_docs = convhtml(files)

# Next comes the "fun" part - getting the IDs from the HTML and splitting the original PDFs.
splits = []
for doc in html_docs:
    splitdoc = []
    # Format for ease of splitting later:
    # [{
    #   "filename": docname,
    #   "start": 1,
    #   "end": 2,
    #   "id": "NHD14_P_KBR_SI10211"
    # }]
    file = path.relpath(doc)
    docname = path.basename(file)
    docname = path.splitext(docname)[0]
    with open(file, encoding="utf8") as f:
        contents = f.read()
        # Regex should be read as XXX|YYY where XXX is the regex to find the name of the section, and YYY is a fairly standard query to find the page divider (should be static, based off of poppler HTML output)
        IDlist = re.findall("ID<\/p>\n<p style=\".+\">(.+)<\/p>|page(\d+)-div", contents)
        # print(IDlist)
        pagenum = 0
        for item in IDlist:
            # If it's ('', 'XXX') then we know it's a page header
            if item[0] == '':
                pagenum += 1
            # If it's ('XXX', '') then we know it's an ID location
            if item[1] == '':
                # Check to see if we need to add the end page to the previous item
                if len(splitdoc) > 0:
                    splitdoc[-1]["end"] = pagenum-1
                # Add new ID
                splitdoc.append({
                    "filename": docname,
                    "start": pagenum,
                    "end": -1,
                    "ID": item[0]
                    })
            print(pagenum)
        # Once we reach the end, set the last ID to end at the last page, just to close things off.
        if len(splitdoc) > 0:
            splitdoc[-1]["end"] = pagenum
    # Append splitdoc to splits as a new file
    splits.append(splitdoc)

# Now let's feed this into our PDF gen utility to get files back out
for file in splits:
    for idset in file:
        print(idset)
        output = genPDF([idset["filename"]], idset["start"], idset["end"], outname=(idset["ID"] + ".pdf"))
        for file in output:
            finallocation = path.relpath(saveloc + "/" + path.basename(file))
            copyfile(file, finallocation)

print("[SUCCESS] Job finished, cleaning up")
# cleanup
cleanup()

input("[SUCCESS] Clean up finished, Press ENTER to close")
