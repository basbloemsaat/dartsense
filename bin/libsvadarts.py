

# import inspect
import json
# import ntpath
# import os
# import re

# import time

import dateutil.parser
import openpyxl
from pprint import pprint


def load_xlsx(filename):
    wb = openpyxl.load_workbook(filename, read_only=True)
    sheet_data = []
    for sheet in wb.worksheets:
        title_list = sheet.title.split()

        date_avond = dateutil.parser.parse(title_list[-1])
        if len(title_list) > 1:
            type_avond = title_list[0].lower()
        else:
            type_avond = "regulier"

        header = [cell.value for cell in sheet[1]]

        # pprint(header)
        iter_rows = sheet.rows
        next(iter_rows)
        for row in iter_rows:
            values = {
                "Date": date_avond.strftime('%Y-%m-%d'),
                "Type": type_avond
            }
            for key, cell in zip(header, row):
                values[key] = cell.value
                if values[key] == None:
                    values[key] = 0

            sheet_data.append(values)

    return sheet_data


def save_data_to_json(data, filename):
    pprint(filename)
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


