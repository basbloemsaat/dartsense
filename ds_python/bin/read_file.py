#!/usr/bin/env python3

import argparse
from openpyxl import load_workbook
from pprint import pprint

parser = argparse.ArgumentParser()


parser.add_argument("--file", help="filename")
args = parser.parse_args()
pprint(args.file)

wb = load_workbook(filename=args.file, read_only=True)
pprint(wb)

ws = wb.active
# sheet_ranges = wb['range names']

pprint(ws)

for sheet in wb.worksheets:
    print (sheet.title)