# TransPDF
Python utility for splitting PDF files by a regex pattern using Poppler Libs. Working on Windows &amp; Linux

Current use case is to split pdf with multiple sub sections into multiple PDFs each named after the section.

## WARNING
This tool will overwrite any existing files, and saves all working files in a .tmp folder in the same directory as the script. it will delete this folder and *everything* in it once the script completes. Multiple files with the same section names will overwrite each other, but it should be fairly minimal work to fix this if it's an issue for anyone.

## WINDOWS USERS
If you're going to run this on windows, download the latest binaries from http://blog.alivate.com.au/poppler-windows/ and place it in a folder called libs in the same directory of the script so that the binaries are located at libs/poppler/bin/*

## LINUX USERS
If you're going to run this on linux, take a look at install.sh then run or modify as needed so that you have the required tools.

In the end, this was made as a one-off script for an internet stranger, and published here in the hopes that it helps someone else too. Code has been commented to a basic degree, but could do with some cleanup work. This tool uses a gui for selection of inputs and outputs, but if you can't bear the sight of that it should be simple to cut it out as needed.

## Usage
Run this transPDF.py using Python3 on Windows or Linux after setting up as described above. If all is well, you should see this screen:
![](http://i.imgur.com/XN8iId9.png)

Press `ENTER` and choose one or more files anywhere on the system, then press `ENTER` again to choose a folder to put the output files in. The current version of the software uses a fixed REGEX query to find the ID from a PDF provided by said internet stranger.
