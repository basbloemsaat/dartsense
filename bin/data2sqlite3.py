#!/usr/bin/env python

import getopt
import sys
import os

import sqlite3

from pprint import pprint
from dumper import dump
import openpyxl


def main(argv):

    data_files = [
        'Austerlitz_seizoen_2016-2017.xlsx',
        'Austerlitz_seizoen_2017-2018.xlsx',
        'Austerlitz_seizoen_2018-2019.xlsx',
    ]

    data_dir = os.path.join(os.path.dirname(__file__), '../data')

    for file_name in data_files:
        # pprint(file_name)
        wb = openpyxl.load_workbook(
            "%s/%s" % (data_dir, file_name), read_only=True)

        sheetnames = wb.sheetnames

        for sheetname in wb.sheetnames:
            colnames = []
            rowdata = []
            ws = wb[sheetname]
            for col in range(1, 20):
                cell = ws.cell(column=col, row=1)
                if cell.value:
                    colnames.append(cell.value)

            # print(colnames)

            for row in range(2, 50):
                values = []
                for col in range(1,len(colnames)+1):
                    cell = ws.cell(column=col, row=row)
                    values.append(cell.value if cell.value else '')

                rowdict = dict(zip(colnames, values))
                if 'Speler' in rowdict and not rowdict['Speler']:
                    continue
                if 'Speler1' in rowdict and not rowdict['Speler1']:
                    continue
                if 'Speler2' in rowdict and not rowdict['Speler2']:
                    continue

                rowdata.append(rowdict)

            # print(rowdata)



def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
