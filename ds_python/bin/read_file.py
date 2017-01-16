#!/usr/bin/env python3

import getopt
import inspect
import os
import sys
import time

from pprint import pprint

import openpyxl


def main(argv):
    parameters = {
        'filename': '',
    }

    try:
        opts, args = getopt.getopt(
            argv, "hsp:v:",
            [
                "help", "file="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ("-f", "--file"):
            parameters['filename'] = arg

    pprint(parameters)

    wb = openpyxl.load_workbook(parameters['filename'], read_only=True)
    # pprint(wb)

    for sheet in wb.worksheets:
        pprint(sheet)
        print(sheet.title)


def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
