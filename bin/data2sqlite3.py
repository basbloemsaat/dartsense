#!/usr/bin/env python

import getopt
import sys
import os

import sqlite3

from pprint import pprint
from dumper import dump
import openpyxl

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
import dartsense
import dartsense.player
import dartsense.event
import dartsense.match
import dartsense.competition


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

        # every sheet is a competition, add a new competition, name is the filename
        comp = dartsense.competition.Competition(name = file_name)
        comp.save()

        exit()

        for ws in wb.worksheets:
            rowdata = []
            header = [cell.value for cell in ws[1]]
            # print(header)

            iter_rows = ws.rows
            next(iter_rows)

            for row in iter_rows:
                # values = []
                # for col in range(1,len(colnames)+1):
                #     cell = ws.cell(column=col, row=row)
                #     values.append(cell.value if cell.value else '')

                rowdict = dict(zip(header, map(lambda x: x.value, row)))

                # print(rowdict)

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
