#!/usr/bin/env python

import getopt
import sys

import sqlite3

from pprint import pprint
from dumper import dump
import openpyxl

def main(argv):
    data_files = [
        'Austerlitz_seizoen_2016-2017.xlsx',
        'Austerlitz_seizoen_2017-2018.xlsx',
    ]

    data_dir = '/home/bas/src/dartsense/data'

    for file_name in data_files:
        pprint(file_name)
        wb = openpyxl.load_workbook("%s/%s" % (data_dir, file_name), read_only=True)



    
def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
