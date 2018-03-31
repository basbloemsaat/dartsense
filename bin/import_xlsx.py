#!/usr/bin/env python3

import getopt
import inspect
import json
import ntpath
import os
import re
import sys
import time

from pprint import pprint
from dumper import dump

import openpyxl
import dateutil.parser

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))


print(os.path.dirname(__file__))

import dartsense
import dartsense.player
import dartsense.event

players = {}

def find_player(player_name, competition_id):
    speler = None
    if player_name in players:
        speler = players[player_name]
    else:
        player_list = dartsense.player.PlayerList(
            filters={'competition': competition_id},
            search=player_name
        )

        # dump(player_list)

        if len(player_list) == 1:
            speler = players[player_name] = player_list[0]
    return speler


def main(argv):
    parameters = {
        'filename': '',
        'competition_id': 0,
    }

    try:
        opts, args = getopt.getopt(
            argv, "hsp:v:",
            ["help", "file=", "competition="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ("-f", "--file"):
            parameters['filename'] = arg
        elif opt in ("-c", "--competition"):
            print('comp')
            competition_id = int(arg)

    pprint(competition_id)

    if not parameters['filename'] or not competition_id:
        usage()

    wb = openpyxl.load_workbook(parameters['filename'], read_only=True)
    # pprint(wb)

    for sheet in wb.worksheets:
        # pprint(sheet)
        # print(sheet.title)
        title_list = sheet.title.split()


        date_avond = dateutil.parser.parse(title_list[-1])
        if len(title_list) > 1:
            type_avond = title_list[0].lower()
            event = dartsense.event.LeagueAdjust()
        else:
            type_avond = "regulier"
            event = dartsense.event.LeagueRound()

        # print(date_avond, type_avond)
        # print(type_avond)

        header = [cell.value for cell in sheet[1]]

        # pprint(header)
        iter_rows = sheet.rows
        next(iter_rows)
        for row in iter_rows:
            values = {}
            for key, cell in zip(header, row):
                # pass
                values[key] = cell.value
            # pprint(values)
            speler1 = find_player(values['Speler1'], competition_id)
            speler2 = find_player(values['Speler2'], competition_id)



def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
